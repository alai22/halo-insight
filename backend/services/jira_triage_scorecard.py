"""
Deterministic Jira triage scorecard: parse LLM rubric JSON, compute implied priority, emit Raise/Lower rows.

Used when JIRA_TRIAGE_SCORECARD_ENABLED; keeps markdown table output compatible with _validate_reprioritization_rows.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

SCORECARD_SCHEMA_VERSION = "1"

# Jira ladder: index 0 = highest
_PRIORITY_ORDER: Tuple[str, ...] = (
    "blocker",
    "critical",
    "major",
    "normal",
    "minor",
    "trivial",
)

_PRIORITY_ALIASES = {
    "highest": "blocker",
    "high": "major",
    "medium": "normal",
    "low": "minor",
    "lowest": "trivial",
}


def normalize_jira_priority_label(value: Any) -> Optional[str]:
    """Match backend/api/routes/jira_routes ladder names."""
    raw = str(value or "").strip().lower()
    if not raw:
        return None
    key = raw.replace(" ", "")
    if key in _PRIORITY_ALIASES:
        key = _PRIORITY_ALIASES[key]
    if key in _PRIORITY_ORDER:
        return key
    return None

_DIMS: Tuple[str, ...] = (
    "severity",
    "frequency",
    "customer_impact",
    "scope",
    "release_risk",
    "confidence",
)


def priority_rank(name: Optional[str]) -> Optional[int]:
    if not name:
        return None
    n = str(name).strip().lower()
    try:
        return _PRIORITY_ORDER.index(n)
    except ValueError:
        return None


class ScorecardWeights(BaseModel):
    severity: float = 1.0
    frequency: float = 1.0
    customer_impact: float = 1.0
    scope: float = 0.8
    release_risk: float = 1.0
    confidence: float = 0.5

    def as_tuple(self) -> Tuple[float, ...]:
        return tuple(getattr(self, d) for d in _DIMS)


class ScorecardBreakpoints(BaseModel):
    """Higher min_score → more severe implied priority. First matching row wins (list must be sorted desc by min_score)."""

    breakpoints: List[Dict[str, Any]] = Field(
        default_factory=lambda: [
            {"min_score": 88.0, "priority": "blocker"},
            {"min_score": 72.0, "priority": "critical"},
            {"min_score": 58.0, "priority": "major"},
            {"min_score": 44.0, "priority": "normal"},
            {"min_score": 30.0, "priority": "minor"},
            {"min_score": 0.0, "priority": "trivial"},
        ]
    )

    @field_validator("breakpoints")
    @classmethod
    def sort_breakpoints(cls, v: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out = []
        for row in v:
            if not isinstance(row, dict):
                continue
            ms = row.get("min_score")
            pr = row.get("priority")
            if ms is None or pr is None:
                continue
            try:
                ms_f = float(ms)
            except (TypeError, ValueError):
                continue
            p = str(pr).strip().lower()
            if priority_rank(p) is None:
                continue
            out.append({"min_score": ms_f, "priority": p})
        out.sort(key=lambda x: -x["min_score"])
        if not out:
            return [
                {"min_score": 88.0, "priority": "blocker"},
                {"min_score": 72.0, "priority": "critical"},
                {"min_score": 58.0, "priority": "major"},
                {"min_score": 44.0, "priority": "normal"},
                {"min_score": 30.0, "priority": "minor"},
                {"min_score": 0.0, "priority": "trivial"},
            ]
        return out


class ScorecardRowIn(BaseModel):
    key: str
    severity: int = Field(ge=1, le=5)
    frequency: int = Field(ge=1, le=5)
    customer_impact: int = Field(ge=1, le=5)
    scope: int = Field(ge=1, le=5)
    release_risk: int = Field(ge=1, le=5)
    confidence: int = Field(ge=1, le=5)
    notes: Optional[Dict[str, str]] = None

    @field_validator("key")
    @classmethod
    def key_upper(cls, v: str) -> str:
        return (v or "").strip().upper()


class ScorecardBatchIn(BaseModel):
    version: str = SCORECARD_SCHEMA_VERSION
    rows: List[ScorecardRowIn] = Field(default_factory=list)


def weights_config_hash(weights: ScorecardWeights, breakpoints: ScorecardBreakpoints) -> str:
    payload = json.dumps(
        {"w": weights.model_dump(), "b": breakpoints.model_dump()},
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _clamp_int(v: Any, lo: int = 1, hi: int = 5) -> int:
    try:
        x = int(v)
    except (TypeError, ValueError):
        return lo
    return max(lo, min(hi, x))


def parse_scorecard_json(raw: str) -> Tuple[Optional[ScorecardBatchIn], List[str]]:
    """
    Parse model output: strip optional ```json fences, validate rows.
    Returns (batch, error_messages).
    """
    if not raw or not raw.strip():
        return None, ["empty response"]
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return None, [f"invalid json: {e}"]

    if not isinstance(data, dict):
        return None, ["root must be object"]
    rows_in = data.get("rows")
    if not isinstance(rows_in, list):
        return None, ["rows must be array"]

    parsed_rows: List[ScorecardRowIn] = []
    errors: List[str] = []
    seen: set = set()

    for i, item in enumerate(rows_in):
        if not isinstance(item, dict):
            errors.append(f"row {i}: not an object")
            continue
        key = str(item.get("key", "")).strip().upper()
        if not key:
            errors.append(f"row {i}: missing key")
            continue
        if key in seen:
            errors.append(f"duplicate key {key}")
            continue
        seen.add(key)
        try:
            row = ScorecardRowIn(
                key=key,
                severity=_clamp_int(item.get("severity")),
                frequency=_clamp_int(item.get("frequency")),
                customer_impact=_clamp_int(item.get("customer_impact")),
                scope=_clamp_int(item.get("scope")),
                release_risk=_clamp_int(item.get("release_risk")),
                confidence=_clamp_int(item.get("confidence")),
                notes=item.get("notes") if isinstance(item.get("notes"), dict) else None,
            )
            parsed_rows.append(row)
        except Exception as e:
            errors.append(f"row {key}: {e}")

    ver = str(data.get("version", SCORECARD_SCHEMA_VERSION))
    batch = ScorecardBatchIn(version=ver, rows=parsed_rows)
    return batch, errors


def parse_shortlist_keys_json(raw: str, valid_keys: set, max_keys: int) -> Tuple[List[str], List[str]]:
    """Parse {"keys":["PROJ-1",...]} from model; filter to valid_keys, cap length."""
    errors: List[str] = []
    if not raw or not raw.strip():
        return [], ["empty shortlist response"]
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return [], [f"shortlist invalid json: {e}"]
    if not isinstance(data, dict):
        return [], ["shortlist root must be object"]
    keys_raw = data.get("keys")
    if not isinstance(keys_raw, list):
        return [], ["shortlist keys must be array"]

    out: List[str] = []
    seen = set()
    for x in keys_raw:
        k = str(x).strip().upper()
        if not k or k not in valid_keys or k in seen:
            continue
        seen.add(k)
        out.append(k)
        if len(out) >= max_keys:
            break
    return out, errors


def composite_score(row: ScorecardRowIn, weights: ScorecardWeights) -> float:
    """0–100: weighted average of dimensions mapped linearly from 1..5."""
    w = weights.as_tuple()
    vals = (
        row.severity,
        row.frequency,
        row.customer_impact,
        row.scope,
        row.release_risk,
        row.confidence,
    )
    tw = sum(w)
    if tw <= 0:
        return 0.0
    acc = 0.0
    for vi, wi in zip(vals, w):
        acc += wi * (vi - 1) / 4.0 * 100.0
    return acc / tw


def implied_priority_from_score(score: float, breakpoints: ScorecardBreakpoints) -> str:
    for row in breakpoints.breakpoints:
        if score >= row["min_score"]:
            return str(row["priority"])
    return "trivial"


def merge_scorecard_to_recommendation(
    row: ScorecardRowIn,
    current_priority: str,
    weights: ScorecardWeights,
    breakpoints: ScorecardBreakpoints,
    min_confidence: int,
    min_delta_ranks: int,
) -> Optional[Dict[str, Any]]:
    """
    If confidence and rank delta vs Jira pass thresholds, return dict with action, target, reason, metadata.
    """
    if row.confidence < min_confidence:
        return None
    cur_label = normalize_jira_priority_label(current_priority)
    cur = priority_rank(cur_label)
    if cur is None:
        return None
    sc = composite_score(row, weights)
    implied = implied_priority_from_score(sc, breakpoints)
    imp = priority_rank(implied)
    if imp is None:
        return None
    delta = abs(imp - cur)
    if delta < min_delta_ranks:
        return None
    if imp < cur:
        action = "raise"
        target = implied
    elif imp > cur:
        action = "lower"
        target = implied
    else:
        return None

    notes = row.notes or {}
    note_bits = [f"{k}={getattr(row, k)}" for k in _DIMS if k != "confidence"]
    note_bits.append(f"conf={row.confidence}")
    reason = (
        f"Scorecard {sc:.0f}/100 → {implied}; "
        + ", ".join(note_bits[:4])
        + ("…" if len(note_bits) > 4 else "")
    )
    if len(reason) > 200:
        reason = reason[:197] + "…"

    return {
        "action": action,
        "target": target,
        "reason": reason,
        "computed_score": round(sc, 2),
        "implied_priority": implied,
        "current_priority_normalized": _PRIORITY_ORDER[cur],
    }


def build_scorecards_by_key_meta(
    batch: ScorecardBatchIn,
    source_by_key: Dict[str, Dict[str, str]],
    weights: ScorecardWeights,
    breakpoints: ScorecardBreakpoints,
    min_confidence: int,
    min_delta_ranks: int,
) -> Dict[str, Any]:
    """Structured meta for UI: every scored key, with optional recommendation."""
    out: Dict[str, Any] = {}
    for row in batch.rows:
        key = row.key
        src = source_by_key.get(key) or {}
        cur_p = src.get("priority") or ""
        sc = composite_score(row, weights)
        implied = implied_priority_from_score(sc, breakpoints)
        rec = merge_scorecard_to_recommendation(
            row,
            cur_p,
            weights,
            breakpoints,
            min_confidence=min_confidence,
            min_delta_ranks=min_delta_ranks,
        )
        entry: Dict[str, Any] = {
            "severity": row.severity,
            "frequency": row.frequency,
            "customer_impact": row.customer_impact,
            "scope": row.scope,
            "release_risk": row.release_risk,
            "confidence": row.confidence,
            "computed_score": round(sc, 2),
            "implied_priority": implied,
            "notes": row.notes or {},
        }
        if rec:
            entry["recommendation"] = {
                "action": rec["action"],
                "target": rec["target"],
                "reason": rec["reason"],
            }
        else:
            entry["recommendation"] = None
        out[key] = entry
    return out


def recommendations_to_reprioritization_markdown(
    batch: ScorecardBatchIn,
    source_by_key: Dict[str, Dict[str, str]],
    weights: ScorecardWeights,
    breakpoints: ScorecardBreakpoints,
    min_confidence: int,
    min_delta_ranks: int,
) -> str:
    """
    Build ### Recommended Jira priority changes section (table or prose-only).
    """
    lines: List[str] = ["### Recommended Jira priority changes", ""]
    table_rows: List[Tuple[str, str, str, str, str]] = []

    for row in batch.rows:
        key = row.key
        src = source_by_key.get(key)
        if not src:
            continue
        title = (src.get("title") or "")[:120]
        cur_display = (src.get("priority") or "").strip()
        rec = merge_scorecard_to_recommendation(
            row,
            cur_display,
            weights,
            breakpoints,
            min_confidence=min_confidence,
            min_delta_ranks=min_delta_ranks,
        )
        if not rec:
            continue
        action = rec["action"]
        target = rec["target"]
        target_title = target[:1].upper() + target[1:] if target else target
        verb = "Raise to" if action == "raise" else "Lower to"
        rec_cell = f"{verb} {target_title}"
        table_rows.append(
            (key, title, cur_display, rec_cell, rec["reason"]),
        )

    if not table_rows:
        lines.append(
            "*No Jira priority changes recommended by the scorecard thresholds "
            "(confidence floor, rank delta vs current priority, or scores aligned with current priority).*"
        )
        return "\n".join(lines)

    lines.append("| Ticket | Title | Current priority | Jira priority recommendation | Reason |")
    lines.append("|---|---|---|---|---|")
    for ticket, title, curp, rec_cell, reason in table_rows:
        safe_title = title.replace("|", "\\|")
        safe_cur = curp.replace("|", "\\|")
        safe_rec = rec_cell.replace("|", "\\|")
        safe_reason = reason.replace("|", "\\|")
        lines.append(f"| {ticket} | {safe_title} | {safe_cur} | {safe_rec} | {safe_reason} |")
    return "\n".join(lines)


def union_shortlist_with_ga_blockers(
    shortlist: List[str],
    issues: List[Dict[str, Any]],
    max_keys: int,
) -> List[str]:
    """Prepend GA blocker keys from issues, then shortlist, dedupe, cap."""
    blockers: List[str] = []
    for issue in issues:
        if issue.get("gaBlocker") is True:
            k = str(issue.get("key", "")).strip().upper()
            if k:
                blockers.append(k)
    seen = set()
    out: List[str] = []
    for k in blockers + shortlist:
        if k in seen:
            continue
        seen.add(k)
        out.append(k)
        if len(out) >= max_keys:
            break
    return out
