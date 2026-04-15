"""
Deterministic Jira triage scorecard (v2): parse LLM rubric JSON (14-point additive rubric),
compute GA verdict + implied Jira priority on the server, emit Raise/Lower rows.

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

SCORECARD_SCHEMA_VERSION = "2"

# Legacy wide reprioritization table (13 cols); regroup fallback only.
SCORECARD_REPRIORITIZATION_NUM_COLUMNS = 13

# Narrow scorecard metrics table (no Title) after the main 5-col reprioritization table.
SCORECARD_METRICS_NUM_COLUMNS = 9


def scorecard_reprioritization_header_line() -> str:
    """Legacy 13-column header; regroup fallback for old cached markdown."""
    return (
        "| Ticket | Title | Current priority | Jira priority recommendation | Reason | "
        "Total | FI | R | TS | WQ | RR | GA verdict | Block GA |"
    )


def scorecard_reprioritization_separator_line() -> str:
    return "|" + "|".join(["---"] * SCORECARD_REPRIORITIZATION_NUM_COLUMNS) + "|"


def scorecard_metrics_header_line() -> str:
    return (
        "| Ticket | Total | FI | R | TS | WQ | RR | GA verdict | Block GA |"
    )


def scorecard_metrics_separator_line() -> str:
    return "|" + "|".join(["---"] * SCORECARD_METRICS_NUM_COLUMNS) + "|"


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


def priority_rank(name: Optional[str]) -> Optional[int]:
    if not name:
        return None
    n = str(name).strip().lower()
    try:
        return _PRIORITY_ORDER.index(n)
    except ValueError:
        return None


def scorecard_framework_config_hash() -> str:
    """Stable id for audit when using fixed v2 rules (no env weights/thresholds)."""
    payload = json.dumps(
        {"framework": "jira_triage_scorecard_v2", "schema": SCORECARD_SCHEMA_VERSION},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _clamp_int(v: Any, lo: int, hi: int) -> int:
    try:
        x = int(v)
    except (TypeError, ValueError):
        return lo
    return max(lo, min(hi, x))


class ScorecardRowIn(BaseModel):
    key: str
    feature_importance: int = Field(ge=0, le=4)
    reach: int = Field(ge=0, le=3)
    technical_severity: int = Field(ge=0, le=3)
    workaround_quality: int = Field(ge=0, le=2)
    regression_risk: int = Field(ge=0, le=2)
    raw_total: Optional[int] = None  # LLM advisory; server uses sum(dimensions)
    ga_verdict: Optional[str] = None
    jira_priority: Optional[str] = None
    notes: Optional[Dict[str, str]] = None

    @field_validator("key")
    @classmethod
    def key_upper(cls, v: str) -> str:
        return (v or "").strip().upper()


class ScorecardBatchIn(BaseModel):
    version: str = SCORECARD_SCHEMA_VERSION
    rows: List[ScorecardRowIn] = Field(default_factory=list)


def raw_total_from_row(row: ScorecardRowIn) -> int:
    return (
        row.feature_importance
        + row.reach
        + row.technical_severity
        + row.workaround_quality
        + row.regression_risk
    )


def ga_verdict_from_total(total: int) -> str:
    if total >= 10:
        return "Block GA"
    if total >= 6:
        return "Fix if capacity"
    return "PostGA"


def reprioritization_reason_short(row: ScorecardRowIn, implied: str, total: int) -> str:
    """One-line hint for the Reason column (dimensions live in dedicated columns)."""
    safety = row.feature_importance == 4 and (row.technical_severity >= 2 or row.workaround_quality >= 1)
    if safety and implied == "blocker" and total < 10:
        return "Safety override (fi=4, ts≥2 or wq≥1)"
    if total >= 10:
        return "total ≥10"
    return f"Scorecard → {implied}"


def implied_jira_priority_from_row(row: ScorecardRowIn) -> str:
    """
    Server-side Jira priority from dimensions + raw total (not LLM jira_priority).
    Order: safety Blocker override, then total bands.
    """
    total = raw_total_from_row(row)
    fi = row.feature_importance
    ts = row.technical_severity
    wq = row.workaround_quality

    if total >= 10 or (fi == 4 and (ts >= 2 or wq >= 1)):
        return "blocker"
    if 8 <= total <= 9:
        return "critical"
    if 6 <= total <= 7:
        return "major"
    if 4 <= total <= 5:
        return "normal"
    return "minor"


def parse_scorecard_json(raw: str) -> Tuple[Optional[ScorecardBatchIn], List[str]]:
    """
    Parse model output: strip optional ```json fences, validate rows (schema v2 only).
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
    ver = str(data.get("version", "")).strip()
    if ver != SCORECARD_SCHEMA_VERSION:
        return None, [f'root "version" must be "{SCORECARD_SCHEMA_VERSION}" (got {ver!r})']
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
            rt = item.get("raw_total")
            raw_total_llm = _clamp_int(rt, 0, 14) if rt is not None else None
            gv = item.get("ga_verdict")
            ga_verdict_llm = str(gv).strip() if gv is not None and str(gv).strip() else None
            jp = item.get("jira_priority")
            jira_priority_llm = str(jp).strip() if jp is not None and str(jp).strip() else None
            row = ScorecardRowIn(
                key=key,
                feature_importance=_clamp_int(item.get("feature_importance"), 0, 4),
                reach=_clamp_int(item.get("reach"), 0, 3),
                technical_severity=_clamp_int(item.get("technical_severity"), 0, 3),
                workaround_quality=_clamp_int(item.get("workaround_quality"), 0, 2),
                regression_risk=_clamp_int(item.get("regression_risk"), 0, 2),
                raw_total=raw_total_llm,
                ga_verdict=ga_verdict_llm,
                jira_priority=jira_priority_llm,
                notes=item.get("notes") if isinstance(item.get("notes"), dict) else None,
            )
            parsed_rows.append(row)
        except Exception as e:
            errors.append(f"row {key}: {e}")

    batch = ScorecardBatchIn(version=SCORECARD_SCHEMA_VERSION, rows=parsed_rows)
    return batch, errors


def scorecard_row_mismatch_warnings(row: ScorecardRowIn) -> List[str]:
    """Non-fatal checks: LLM totals vs server sum."""
    out: List[str] = []
    computed = raw_total_from_row(row)
    if row.raw_total is not None and row.raw_total != computed:
        out.append(f"{row.key}: raw_total LLM={row.raw_total} != sum(dimensions)={computed}")
    if row.ga_verdict:
        server_gv = ga_verdict_from_total(computed)
        gv = row.ga_verdict.strip()
        if gv != server_gv:
            out.append(f"{row.key}: ga_verdict LLM={gv!r} != server={server_gv!r} (from total {computed})")
    if row.jira_priority:
        implied = implied_jira_priority_from_row(row)
        jp = normalize_jira_priority_label(row.jira_priority)
        if jp and jp != implied:
            out.append(
                f"{row.key}: jira_priority LLM={row.jira_priority!r} != server implied={implied} "
                f"(total {computed})"
            )
    return out


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


def merge_scorecard_to_recommendation(
    row: ScorecardRowIn,
    current_priority: str,
    min_delta_ranks: int,
) -> Optional[Dict[str, Any]]:
    """
    If rank delta vs Jira passes threshold, return dict with action, target, reason, metadata.
    Schema v2: no confidence gate.
    """
    cur_label = normalize_jira_priority_label(current_priority)
    cur = priority_rank(cur_label)
    if cur is None:
        return None
    total = raw_total_from_row(row)
    implied = implied_jira_priority_from_row(row)
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

    reason = reprioritization_reason_short(row, implied, total)

    return {
        "action": action,
        "target": target,
        "reason": reason,
        "raw_total": total,
        "implied_priority": implied,
        "current_priority_normalized": _PRIORITY_ORDER[cur],
    }


def build_scorecards_by_key_meta(
    batch: ScorecardBatchIn,
    source_by_key: Dict[str, Dict[str, str]],
    min_delta_ranks: int,
) -> Dict[str, Any]:
    """Structured meta for UI: every scored key, with optional recommendation."""
    out: Dict[str, Any] = {}
    for row in batch.rows:
        key = row.key
        src = source_by_key.get(key) or {}
        cur_p = src.get("priority") or ""
        total = raw_total_from_row(row)
        implied = implied_jira_priority_from_row(row)
        ga = ga_verdict_from_total(total)
        rec = merge_scorecard_to_recommendation(row, cur_p, min_delta_ranks=min_delta_ranks)
        entry: Dict[str, Any] = {
            "feature_importance": row.feature_importance,
            "reach": row.reach,
            "technical_severity": row.technical_severity,
            "workaround_quality": row.workaround_quality,
            "regression_risk": row.regression_risk,
            "raw_total": total,
            "ga_verdict": ga,
            "implied_priority": implied,
            "llm_raw_total": row.raw_total,
            "llm_ga_verdict": row.ga_verdict,
            "llm_jira_priority": row.jira_priority,
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
    min_delta_ranks: int,
) -> str:
    """
    Build ### Recommended Jira priority changes section (table or prose-only).
    """
    lines: List[str] = ["### Recommended Jira priority changes", ""]
    table_rows: List[Tuple[ScorecardRowIn, str, str, str, str, str]] = []

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
            min_delta_ranks=min_delta_ranks,
        )
        if not rec:
            continue
        action = rec["action"]
        target = rec["target"]
        target_title = target[:1].upper() + target[1:] if target else target
        verb = "Raise to" if action == "raise" else "Lower to"
        rec_cell = f"{verb} {target_title}"
        table_rows.append((row, key, title, cur_display, rec_cell, rec["reason"]))

    if not table_rows:
        lines.append(
            "*No Jira priority changes recommended by the scorecard thresholds "
            "(rank delta vs current priority, or scores aligned with current priority).*"
        )
        return "\n".join(lines)

    lines.append("| Ticket | Title | Current priority | Jira priority recommendation | Reason |")
    lines.append("|---|---|---|---|---|")
    for srow, ticket, title, curp, rec_cell, reason in table_rows:
        safe_title = title.replace("|", "\\|")
        safe_cur = curp.replace("|", "\\|")
        safe_rec = rec_cell.replace("|", "\\|")
        safe_reason = reason.replace("|", "\\|")
        lines.append(f"| {ticket} | {safe_title} | {safe_cur} | {safe_rec} | {safe_reason} |")

    lines.append("")
    lines.append("#### Scorecard (14-point)")
    lines.append("")
    lines.append(scorecard_metrics_header_line())
    lines.append(scorecard_metrics_separator_line())
    for srow, ticket, _title, _curp, _rec_cell, _reason in table_rows:
        total = raw_total_from_row(srow)
        ga = ga_verdict_from_total(total)
        block_ga = "Yes" if ga == "Block GA" else "No"
        safe_ga = ga.replace("|", "\\|")
        lines.append(
            f"| {ticket} | {total}/14 | {srow.feature_importance} | {srow.reach} | "
            f"{srow.technical_severity} | {srow.workaround_quality} | {srow.regression_risk} | "
            f"{safe_ga} | {block_ga} |"
        )
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
