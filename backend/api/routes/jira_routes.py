"""
Jira API Routes for Bug Triage Copilot

Provides issue list, status, OAuth 2.0 (3LO) connect flow, and AI backlog overview.
"""

import json
import logging
import re
import secrets
from collections import Counter
from typing import Any, Dict, Iterator, List, Optional, Tuple

from flask import Blueprint, Response, g, jsonify, redirect, request, session, stream_with_context
import requests

from backend.core.exceptions import AppException, ClaudeAPIError, RateLimitError
from backend.core.exceptions import TimeoutError as AppTimeoutError
from backend.services.jira_client import JiraClient
from backend.services import jira_oauth
from backend.services.jira_triage_scorecard import (
    SCORECARD_REPRIORITIZATION_NUM_COLUMNS,
    SCORECARD_SCHEMA_VERSION,
    build_scorecards_by_key_meta,
    parse_scorecard_json,
    parse_shortlist_keys_json,
    recommendations_to_reprioritization_markdown,
    scorecard_framework_config_hash,
    scorecard_reprioritization_header_line,
    scorecard_reprioritization_separator_line,
    scorecard_row_mismatch_warnings,
    scorecard_threshold_reference_lines,
    union_shortlist_with_ga_blockers,
)
from backend.utils.config import Config
from backend.utils.pii_protection import create_pii_protector

logger = logging.getLogger(__name__)

# Max chars of response body to include in error_details (avoid huge payloads)
JIRA_ERROR_SNIPPET_MAX = 800


def _jira_http_error_response(e: requests.HTTPError, fallback_message: str):
    """Build (message, error_details, status_code) from a requests HTTPError for Jira API."""
    status_code = e.response.status_code if e.response is not None else 500
    message_parts = [f"Jira returned {status_code}"]
    response_snippet = None
    try:
        if e.response is not None and e.response.text:
            response_snippet = (e.response.text or "")[:JIRA_ERROR_SNIPPET_MAX]
            if e.response.headers.get("content-type", "").startswith("application/json"):
                body = e.response.json()
                if isinstance(body, dict):
                    if body.get("errorMessages"):
                        message_parts.append("; ".join(body["errorMessages"]))
                    if body.get("errors") and isinstance(body["errors"], dict):
                        for k, v in body["errors"].items():
                            message_parts.append(f"{k}: {v}")
                    elif body.get("errors"):
                        message_parts.append(str(body["errors"]))
    except Exception:
        pass
    message = " — ".join(message_parts) if len(message_parts) > 1 else (message_parts[0] if message_parts else fallback_message)
    error_details = {"status_code": status_code}
    if response_snippet:
        error_details["response_snippet"] = response_snippet
    return message, error_details, min(status_code, 599)

jira_bp = Blueprint('jira', __name__, url_prefix='/api/jira')

# OAuth state key in session
JIRA_OAUTH_STATE_KEY = 'jira_oauth_state'

# POST /backlog-overview: allowed issue keys from client; max issues and title/description length for prompt size
_OVERVIEW_ALLOWED_KEYS = frozenset({
    'key', 'title', 'priority', 'status', 'issuetype', 'component', 'components', 'labels',
    'parentKey', 'parentSummary', 'epicKey', 'epicSummary', 'sprint', 'gaBlocker', 'needsMoreInfo',
    'description',
})
_OVERVIEW_MAX_ISSUES = 450
_OVERVIEW_MAX_TITLE_LEN = 240
_OVERVIEW_MAX_DESCRIPTION_LEN = 2000
_OVERVIEW_DESCRIPTION_EXCERPT_LEN = 800
_OVERVIEW_MAX_LABELS = 20
_OVERVIEW_MAX_COMPONENTS = 15

# Post-process model output: deterministically validate reprioritization rows.
_RE_MD_TABLE_ROW = re.compile(r'^\s*\|(.+)\|\s*$')
_RE_RAISE = re.compile(r'raise', re.IGNORECASE)
_RE_BLOCKER = re.compile(r'\bblocker\b', re.IGNORECASE)
_RE_HEADER_SEP = re.compile(r'^[\s\-:|]+$')
_RE_TICKET_KEY_CELL = re.compile(r'^[A-Za-z][A-Za-z0-9]{1,19}-\d+$')
_RE_RECOMMENDATION_TARGET = re.compile(r'\b(raise|lower)\s+to\s+([A-Za-z]+)\b', re.IGNORECASE)
_RE_ANY_TICKET_KEY = re.compile(r'\b([A-Za-z][A-Za-z0-9]{1,19}-\d+)\b')

_PRIORITY_RANKS = {
    'blocker': 0,
    'critical': 1,
    'major': 2,
    'normal': 3,
    'minor': 4,
    'trivial': 5,
}
_PRIORITY_ALIASES = {
    'highest': 'blocker',
    'high': 'major',
    'medium': 'normal',
    'low': 'minor',
    'lowest': 'trivial',
}


def _issue_has_parent_context(issue: Dict[str, Any]) -> bool:
    """Keep issue when it belongs to a parent/epic context."""
    parent_key = str(issue.get('parentKey') or '').strip()
    epic_key = str(issue.get('epicKey') or '').strip()
    return bool(parent_key or epic_key)


def _markdown_table_row_cells(line: str) -> Optional[List[str]]:
    """Parse a pipe table row into stripped cells, or None if not a table row."""
    m = _RE_MD_TABLE_ROW.match(line)
    if not m:
        return None
    inner = m.group(1)
    cells = [c.strip() for c in inner.split('|')]
    return cells if len(cells) >= 4 else None


def _current_priority_is_blocker(cell: str) -> bool:
    t = (cell or '').strip().lower()
    return t == 'blocker' or t.startswith('blocker ')


def _recommendation_is_raise_to_blocker(cell: str) -> bool:
    c = cell or ''
    return bool(_RE_RAISE.search(c) and _RE_BLOCKER.search(c))


def _normalize_priority_label(value: Any) -> Optional[str]:
    raw = str(value or '').strip().lower()
    if not raw:
        return None
    key = raw.replace(' ', '')
    if key in _PRIORITY_ALIASES:
        key = _PRIORITY_ALIASES[key]
    if key in _PRIORITY_RANKS:
        return key
    return None


def _parse_recommendation_action_and_target(cell: str) -> Optional[Tuple[str, str]]:
    raw = (cell or '').strip()
    if not raw:
        return None
    m = _RE_RECOMMENDATION_TARGET.search(raw)
    if not m:
        return None
    action = m.group(1).lower()
    target = _normalize_priority_label(m.group(2))
    if action not in ('raise', 'lower') or target is None:
        return None
    return action, target


def _repr_row_current_and_recommendation(cells: List[str]) -> Optional[Tuple[str, str]]:
    """(current_priority_cell, recommendation_cell) for reprioritization data rows; supports 4- or 5-column tables."""
    if not cells:
        return None
    n = len(cells)
    if n >= 5:
        return cells[2], cells[3]
    if n == 4:
        return cells[1], cells[2]
    return None


def _validate_reprioritization_rows(
    markdown: str,
    source_priorities: Optional[Dict[str, str]] = None,
) -> Tuple[str, Dict[str, int]]:
    """
    Deterministically validate reprioritization rows.
    Drops rows that violate ladder directionality or mismatch source-of-truth current priorities.
    Only applies between ### Recommended Jira priority changes and the next ## section.
    """
    if not markdown or 'Recommended Jira priority changes' not in markdown:
        return markdown, {'invalid': 0, 'mismatch': 0}

    lines = markdown.split('\n')
    out: List[str] = []
    in_repr = False
    dropped_invalid = 0
    dropped_mismatch = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('### Recommended Jira priority changes'):
            in_repr = True
            out.append(line)
            continue
        if in_repr and stripped.startswith('## ') and not stripped.startswith('###'):
            in_repr = False
        if not in_repr:
            out.append(line)
            continue

        # Inside reprioritization section
        cells = _markdown_table_row_cells(line)
        if not cells:
            out.append(line)
            continue
        if cells[0].lower().startswith('ticket') or _RE_HEADER_SEP.match(cells[0]):
            out.append(line)
            continue

        cur_rec = _repr_row_current_and_recommendation(cells)
        if cur_rec is None:
            dropped_invalid += 1
            continue

        ticket = (cells[0] or '').strip().upper()
        current_raw, rec_raw = cur_rec
        current = _normalize_priority_label(current_raw)
        parsed = _parse_recommendation_action_and_target(rec_raw)
        if current is None or parsed is None:
            # Not a primary reprior row (e.g. scorecard metrics table); keep line.
            out.append(line)
            continue

        action, target = parsed
        current_rank = _PRIORITY_RANKS[current]
        target_rank = _PRIORITY_RANKS[target]
        is_valid_direction = (
            (action == 'raise' and target_rank < current_rank)
            or (action == 'lower' and target_rank > current_rank)
        )
        if not is_valid_direction:
            dropped_invalid += 1
            logger.info(
                'backlog-overview: dropped invalid repr direction ticket=%s current=%s recommendation=%s',
                ticket[:32],
                current,
                (rec_raw or '')[:64],
            )
            continue

        if source_priorities and _RE_TICKET_KEY_CELL.match(ticket):
            expected = source_priorities.get(ticket)
            if expected and expected != current:
                dropped_mismatch += 1
                logger.info(
                    'backlog-overview: dropped repr row priority mismatch ticket=%s current_cell=%s expected=%s',
                    ticket[:32],
                    current,
                    expected,
                )
                continue
        out.append(line)

    if dropped_invalid or dropped_mismatch:
        logger.info(
            'backlog-overview: dropped rows invalid=%s mismatch=%s',
            dropped_invalid,
            dropped_mismatch,
        )
    return '\n'.join(out), {'invalid': dropped_invalid, 'mismatch': dropped_mismatch}


_REPR_SECTION_HEADING = '### Recommended Jira priority changes'
_REPR_BUCKET_ORDER: Tuple[Tuple[str, str], ...] = (
    ('ios', '#### iOS'),
    ('android', '#### Android'),
    ('both', '#### iOS and Android'),
    ('other', '#### Other components'),
)


def _issue_component_names(issue: Dict[str, Any]) -> List[str]:
    """Jira component display names for an issue (same aggregation as overview TSV)."""
    if not issue:
        return []
    comps = issue.get('components')
    if isinstance(comps, list):
        out = [str(c).strip() for c in comps if c is not None and str(c).strip()]
        if out:
            return out
    c = issue.get('component')
    if c is None:
        return []
    s = str(c).strip()
    return [s] if s else []


def _component_bucket_from_issue(issue: Dict[str, Any]) -> str:
    """Partition key for reprioritization rows: ios | android | both | other."""
    names = _issue_component_names(issue)
    has_ios = any(n.lower() == 'ios' for n in names)
    has_android = any(n.lower() == 'android' for n in names)
    if has_ios and has_android:
        return 'both'
    if has_ios:
        return 'ios'
    if has_android:
        return 'android'
    return 'other'


def _regroup_reprioritization_section_by_component(
    markdown: str,
    issues: List[Dict[str, Any]],
) -> str:
    """
    After validation, split the reprioritization pipe table into per-platform tables using
    Jira components from the same issue batch (#### subheadings only—pass2b key extraction).
    Prose-only sections (no data rows) are left unchanged.
    """
    if not markdown or _REPR_SECTION_HEADING not in markdown:
        return markdown

    issues_by_key = {
        str(i.get('key', '')).strip().upper(): i
        for i in issues
        if i.get('key')
    }

    lines = markdown.split('\n')
    start: Optional[int] = None
    for idx, line in enumerate(lines):
        if line.strip().startswith(_REPR_SECTION_HEADING):
            start = idx
            break
    if start is None:
        return markdown

    end = len(lines)
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if s.startswith('## ') and not s.startswith('###'):
            end = j
            break

    body = lines[start + 1 : end]
    leading_prose: List[str] = []
    header_line: Optional[str] = None
    sep_line: Optional[str] = None
    rows_by_bucket: Dict[str, List[str]] = {bid: [] for bid, _ in _REPR_BUCKET_ORDER}
    suffix_lines: List[str] = []
    primary_data_started = False

    i = 0
    while i < len(body):
        line = body[i]
        cells = _markdown_table_row_cells(line)
        if cells is None:
            if header_line is None:
                leading_prose.append(line)
            elif sep_line is not None:
                if not primary_data_started and not line.strip():
                    pass  # blank lines between separator and first data row
                else:
                    suffix_lines = body[i:]
                    break
            i += 1
            continue

        c0 = (cells[0] or '').strip()
        c0l = c0.lower()
        if c0l.startswith('ticket'):
            header_line = line
            i += 1
            if i < len(body):
                nxt_cells = _markdown_table_row_cells(body[i])
                if nxt_cells and _RE_HEADER_SEP.match((nxt_cells[0] or '').strip()):
                    sep_line = body[i]
                    i += 1
            continue

        if sep_line is None and header_line is not None and _RE_HEADER_SEP.match(c0):
            sep_line = line
            i += 1
            continue

        if _RE_HEADER_SEP.match(c0):
            i += 1
            continue

        cur_rec = _repr_row_current_and_recommendation(cells)
        ticket = (cells[0] or '').strip().upper()
        if cur_rec and _RE_TICKET_KEY_CELL.match(ticket):
            primary_data_started = True
            b = _component_bucket_from_issue(issues_by_key.get(ticket, {}))
            rows_by_bucket[b].append(line)
        elif sep_line is not None:
            suffix_lines = body[i:]
            break
        i += 1

    total_rows = sum(len(v) for v in rows_by_bucket.values())
    if total_rows == 0:
        return markdown

    if header_line is None or sep_line is None:
        sample: Optional[str] = None
        for bid, _ in _REPR_BUCKET_ORDER:
            if rows_by_bucket[bid]:
                sample = rows_by_bucket[bid][0]
                break
        sc = _markdown_table_row_cells(sample) if sample else None
        ncol = len(sc) if sc else 5
        if ncol >= SCORECARD_REPRIORITIZATION_NUM_COLUMNS:
            header_line = scorecard_reprioritization_header_line()
            sep_line = scorecard_reprioritization_separator_line()
        elif ncol >= 5:
            header_line = '| Ticket | Title | Current priority | Recommended priority | Reason |'
            sep_line = '|---|---|---|---|---|'
        else:
            header_line = '| Ticket | Current priority | Recommended priority | Reason |'
            sep_line = '|---|---|---|---|'

    while leading_prose and not leading_prose[-1].strip():
        leading_prose.pop()

    out_section: List[str] = [lines[start].rstrip()]
    if leading_prose:
        out_section.append('')
        out_section.extend(leading_prose)

    first_bucket_out = True
    for bid, h4 in _REPR_BUCKET_ORDER:
        b_rows = rows_by_bucket[bid]
        if not b_rows:
            continue
        if first_bucket_out:
            out_section.append('')
            first_bucket_out = False
        else:
            out_section.append('')
        out_section.append(h4)
        out_section.append('')
        out_section.append(header_line.rstrip())
        out_section.append(sep_line.rstrip())
        out_section.extend(b_rows)

    if suffix_lines:
        out_section.append('')
        out_section.extend(s.rstrip() for s in suffix_lines)

    new_section = '\n'.join(out_section).rstrip()
    return '\n'.join(lines[:start] + [new_section] + lines[end:])


def _extract_reprioritization_keys(markdown: str) -> List[str]:
    """
    Parse issue keys from the pipe table under ### Recommended Jira priority changes.
    Preserves row order; dedupes while keeping first occurrence.
    """
    if not markdown or 'Recommended Jira priority changes' not in markdown:
        return []
    lines = markdown.split('\n')
    in_section = False
    keys: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('### Recommended Jira priority changes'):
            in_section = True
            continue
        if not in_section:
            continue
        if stripped.startswith('## ') and not stripped.startswith('###'):
            break
        if stripped.startswith('### ') and not stripped.startswith('### Recommended Jira priority changes'):
            break
        cells = _markdown_table_row_cells(line)
        if not cells or len(cells) < 4:
            continue
        cur_rec = _repr_row_current_and_recommendation(cells)
        if cur_rec is None:
            continue
        current_raw, rec_raw = cur_rec
        if _normalize_priority_label(current_raw) is None or _parse_recommendation_action_and_target(rec_raw) is None:
            continue
        k = (cells[0] or '').strip()
        if not k or k.lower() == 'ticket':
            continue
        if _RE_HEADER_SEP.match(k):
            continue
        if not _RE_TICKET_KEY_CELL.match(k):
            continue
        keys.append(k.upper())
    return list(dict.fromkeys(keys))


def _extract_title_rewrite_keys(text: str, valid_keys: List[str], max_keys: int) -> List[str]:
    """Parse candidate keys from model output (JSON-ish or free text), preserving order."""
    if not text:
        return []
    valid = {k.upper() for k in valid_keys}
    out: List[str] = []
    seen = set()
    for m in _RE_ANY_TICKET_KEY.finditer(text):
        k = m.group(1).upper()
        if k not in valid or k in seen:
            continue
        out.append(k)
        seen.add(k)
        if len(out) >= max_keys:
            break
    return out


def _normalize_title_for_compare(title: str) -> str:
    s = (title or '').strip().lower().replace('…', '...')
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\.\.\.$', '', s).strip()
    return s


def _titles_equivalent(a: str, b: str) -> bool:
    na = _normalize_title_for_compare(a)
    nb = _normalize_title_for_compare(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    # Allow conservative truncation equivalence from markdown table cells.
    if len(na) >= 20 and nb.startswith(na):
        return True
    if len(nb) >= 20 and na.startswith(nb):
        return True
    return False


def _validate_title_rewrite_rows(
    markdown: str,
    source_by_key: Dict[str, Dict[str, str]],
    max_rows: int,
) -> Tuple[str, Dict[str, int]]:
    """
    Keep only valid rows under ### Title clarity suggestions.
    Returns (section_markdown_or_empty, counters).
    """
    if not markdown or 'Title clarity suggestions' not in markdown:
        return '', {'kept': 0, 'dropped': 0}
    lines = markdown.split('\n')
    out: List[str] = []
    in_section = False
    dropped = 0
    kept = 0
    wrote_header = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('### Title clarity suggestions'):
            in_section = True
            if not wrote_header:
                out.append('### Title clarity suggestions')
                out.append('| Ticket | Current priority | Current title | Proposed title |')
                out.append('|---|---|---|---|')
                wrote_header = True
            continue
        if in_section and stripped.startswith('## ') and not stripped.startswith('###'):
            break
        if in_section and stripped.startswith('### ') and not stripped.startswith('### Title clarity suggestions'):
            break
        if not in_section:
            continue
        cells = _markdown_table_row_cells(line)
        if not cells:
            continue
        ticket = (cells[0] or '').strip().upper()
        if ticket.lower() == 'ticket' or _RE_HEADER_SEP.match(ticket):
            continue
        if len(cells) < 4 or ticket not in source_by_key:
            dropped += 1
            continue
        src = source_by_key[ticket]
        current_priority = _normalize_priority_label(cells[1] if len(cells) > 1 else '')
        expected_priority = _normalize_priority_label(src.get('priority') or '')
        current_title = (cells[2] if len(cells) > 2 else '').strip()
        proposed_title = (cells[3] if len(cells) > 3 else '').strip()
        if not current_priority or not expected_priority or current_priority != expected_priority:
            dropped += 1
            continue
        if not _titles_equivalent(current_title, src.get('title') or ''):
            dropped += 1
            continue
        if not proposed_title:
            dropped += 1
            continue
        if _titles_equivalent(proposed_title, src.get('title') or '') or _titles_equivalent(proposed_title, current_title):
            dropped += 1
            continue
        if kept >= max_rows:
            dropped += 1
            continue
        out.append(
            f"| {_md_pipe_cell(ticket)} | {_md_pipe_cell(src.get('priority') or '')} | {_md_pipe_cell(src.get('title') or '', 180)} | {_md_pipe_cell(proposed_title, 180)} |"
        )
        kept += 1
    if kept == 0:
        return '', {'kept': 0, 'dropped': dropped}
    return '\n'.join(out).strip(), {'kept': kept, 'dropped': dropped}


# Pass 1: themes, clarification, duplicates—no Priority review (that is pass 2 for output budget).
# max_tokens per pass come from Config (default 4096; >4096 often 400 Bad Request on Haiku).

_BACKLOG_OVERVIEW_SYSTEM_PASS1 = """You are an engineering lead helping triage a Jira bug backlog for **Halo Collar** (pet GPS / smart collar; mobile apps for pet tracking, maps, geofences, device pairing, etc.). You receive issues as **TAB-separated** lines (see user message header row for column order—**priority** is the 4th column).

**Important:** Do **not** output a `## Priority review` section. Priority review is generated in a separate step; including it here is **forbidden**.

Write a markdown overview for the team. Use these sections only (omit a section if nothing substantive to say). **When multiple sections apply, keep this `##` order** so the recap reads top-down: **themes and unclear tickets before duplicate clusters** (this block is shown **after** `## Priority review` in the UI, which covers Jira priority recommendations first).

## Critical / high-risk themes
(Themes and risk—**not** the Jira priority name "Critical".)
## Needs clarification
Tickets that look vague, blocked, or missing context based on titles/metadata.

**Format (required when this section is non-empty):** Use a **markdown bullet list**. Put **exactly one issue key per bullet**—never one paragraph or run-on sentence listing multiple keys. Each bullet must look like: `- **HALO-123** — short reason (why it needs clarification).` You may add **one** optional intro sentence *before* the list; the list must follow. Do **not** concatenate several keys into a single line without list markers.
## Duplicates or related clusters
When this section has content: put **at least one sentence of prose** on the line(s) immediately after this `##` heading **before** any `###` subheading (do **not** jump straight from `## Duplicates or related clusters` to `###` with nothing in between—that reads as a broken outline).
Then use **two subheadings** when applicable (omit empty subheadings):
### Likely duplicate candidates
Only when titles/metadata strongly suggest the **same user-visible bug** or **same root cause** (e.g. duplicate report of the identical failure). State briefly why. Cite keys.
### Shared root-cause investigation (optional)
Only when you believe **one fix or one investigation thread** could reasonably address **multiple keys** together—not merely that they touch the same screen family. Name the **hypothesized shared cause** in one short phrase. Cite keys.

**iOS vs Android:** If tickets clearly target **different platforms** (e.g. `[iOS]` vs `[Android]` / `[R][Android]` in titles, or obvious platform in summary), treat them as **separate bugs by default**—different native codepaths. **Do not** list them under **Likely duplicate candidates** or claim "**the same underlying issue**" or a **single shared investigation** unless you name a **specific shared layer** (e.g. backend API, contract, shared SDK)—not merely the same button label or flow name. You may note **same feature area** and that teams could **compare notes**; phrase that differently from asserting one root cause.

**Product context:** Map UI, pet pins, follow mode, pet card, multi-pet map behavior, geofences/fences, and collar/API updates are **different flows** in this product. **Do not** cluster tickets together only because they mention the same surface keywords (map, location, GPS, pet, collar) or only because both are mobile—surface overlap is normal, not evidence of duplication.

## Other notes
Non-obvious risks or cross-cutting patterns only. Omit this section entirely if everything important is already covered above.

Rules:
- Cite issue keys (e.g. PROJ-123) when you reference specific tickets.
- Do not invent facts; only infer from the provided list.
- **Duplicates / clusters:** Prefer **no entry** in this section over weak grouping. If you are unsure, omit or mention uncertainty briefly rather than listing loosely related tickets. **iOS + Android pairs** are not duplicates unless a **shared non-client** cause is explicit in the data.
- **No filler or throat-clearing.** Do not state the obvious unless you tie it to a **specific triage implication** with cited keys.
- Do not open with generic scene-setting. Prefer leading with concrete findings.
- **Length:** Use up to roughly **2000 words** for these sections combined. If you must shorten, trim "Other notes" and prose before dropping concrete duplicate or clarification citations.

**Forbidden:** Any heading `## Priority review` or discussion of Jira priority raise/lower recommendations (that is handled elsewhere)."""


# Pass-2 only: what “important” means for Halo when recommending Jira Raise/Lower. Append bullets here as norms evolve.
_HALO_PRODUCT_PRIORITY_CONTEXT_FOR_REVIEW = """
**Halo product context (use when judging Raise / Lower—extend this block over time with PM/engineering):**
- **Primary mission:** **Protect dogs** via **virtual GPS fences**, **reliable geofence / containment behavior**, and **accurate collar-reported location** when that affects safety. **Critical** and **Blocker** in Jira should align with **core** risk in this space—not every title that sounds severe.
- **Often non-core (do not over-escalate):** **Pet profile** and **profile photo** flows, **optional onboarding** polish, and similar **peripheral** UX. Example: a **Major** bug on **Add Photo** / profile setup (e.g. bottom sheet loop, user must force-kill) **does not** by itself justify **Raise to Critical** if **fence setup**, **live tracking for containment**, and **location correctness for geofences** are **not** impaired—**Major** can remain appropriate.
- **Stronger Raise signals:** Widespread **production** impact; **wrong or unusable location** affecting **fences**; **geofence** arming/disarming or containment logic broken; collar **offline** in ways that block **safety-relevant** use; inability to complete **collar pairing** or **fence configuration** **without** a reasonable workaround. When recommending **Raise**, tie the **Reason** to **core vs peripheral** impact when it helps the team.

"""


_BACKLOG_OVERVIEW_SYSTEM_PASS2 = (
    """You are an engineering lead helping triage a Jira bug backlog for **Halo Collar** (pet GPS / smart collar; mobile apps for pet tracking, maps, geofences, device pairing, etc.). You receive issues as **TAB-separated** lines (not pipe `|` tables). The user message has a header row naming columns: **key, title, type, priority, status, …** — the **priority** value is always the **4th field** on each line.

**Canonical Jira priority:** For every ticket, the **only** source of truth for its current Jira priority is that **priority** field. **Never** infer or override it from the title (e.g. words like "GA", "critical", "blocker" in the summary are **not** the Jira priority unless they appear in the **priority** column). In `### Recommended Jira priority changes`, the **Current priority** cell (the column **after** Ticket and Title) must **exactly match** the priority field from the input line for that issue key.

**HALO Jira priority field (highest → lowest):** Blocker → Critical → Major → Normal → Minor → Trivial. Match the **priority** column case-insensitively to these names (or treat unknown values conservatively).

**Ladder for comparisons (memorize):** Blocker is **#1 (top—cannot go higher)**. Then Critical, Major, Normal, Minor, Trivial. A valid **Raise** means moving **up** this list (e.g. Critical→Blocker). A valid **Lower** means moving **down**.

"""
    + _HALO_PRODUCT_PRIORITY_CONTEXT_FOR_REVIEW
    + """**Output:** Produce **only** the markdown subsection starting with `### Recommended Jira priority changes` (see Format below). Do **not** output `## Priority review`—the application prepends backlog statistics. Do **not** output an aggregate “count by priority” table; a snapshot is injected for you. No preamble, no other `##` sections, no themes or duplicates here. The app may regroup your **single** reprioritization table by Jira component (e.g. iOS vs Android) for display—still output **one** table here, not multiple.

Assess **every** issue in the table for Jira priority vs title/metadata. **Only tabulate** tickets where you recommend changing the Jira priority field in the reprioritization table.

**Coverage (mandatory):** Pay deliberate attention to **Major**, **Normal**, and **Minor** tickets—not only Blocker/Critical. Many mis-prioritizations appear as severe user impact in the title while priority is still Normal or Major. Scan those tiers before concluding.

**Do not pad:** Only include tickets where a Raise/Lower change is clearly justified; omit weak or uncertain rows. If none apply, state that in one sentence under the subheading (no table).

For tickets in the reprioritization table, use this **exact vocabulary** for the Jira **priority field** only:
- **Raise Jira priority** — move **up** the ladder. State the **target** level (e.g. "Raise to Blocker").
- **Lower Jira priority** — move **down** the ladder. State the target when clear.
- **No Jira priority change** — appropriate as-is (counting only—**never** a row in the reprioritization table).

**Ceiling (hard rule):** **Blocker** is the maximum. Tickets whose **Current priority** is **Blocker** **must not** appear in `### Recommended Jira priority changes` with **Raise** or **Raise to Blocker**. Severity in the title does **not** override already-Blocker in Jira.

**Never duplicate the current level as the target:** **Raise to X** / **Lower to X** requires Current **strictly below** / **strictly above** X on the ladder, respectively.

**Before output, self-check each reprioritization row:** (1) **Raise to** implies Current is strictly below target. (2) Current **Blocker** → never **Raise**. (3) Drop invalid rows. (4) For **Raise** on **Major** issues in **profile / photo / optional setup** flows, confirm **core fence or location-for-containment** risk—not bad UX alone.

**Avoid confusion:** Do not use **escalate** for Jira priority in the table—use **Raise** / **Lower** wording.

**Format (required):**

**Reprioritization (only if any):** Start with subheading `### Recommended Jira priority changes` then a GitHub-flavored pipe table `|---|---|---|---|---|`:

| Ticket | Title | Current priority | Recommended priority | Reason |

- **Title:** Copy the issue **summary/title** from the input data for that key (same wording as the `title` field in the tab-separated issue list; truncate with `…` if needed so the row stays readable, e.g. roughly **120 characters** max in the cell).
- Recommendation column: only **Raise to …** or **Lower to …** (never “No change” rows—omit tickets that need no change). **Reason:** keep to **one short line** per row when possible so more tickets fit.
- If you recommend **no** priority changes at all, output the subheading `### Recommended Jira priority changes` and a single line of prose stating that (no table).

**Length:** This fragment may use up to roughly **3500 words** if needed. Prefer terse reasons over omitting justified Major/Normal/Minor candidates.

Rules:
- Never **escalate/de-escalate** as verbs for the priority field in the table.
- **Blocker** current → never **Raise** / **Raise to Blocker** in the reprioritization table.
- Do not invent facts."""
)

_BACKLOG_OVERVIEW_PASS2B_EXTRA = """

**Second pass (description-enriched):** The user message has the same **metadata table** for every issue, then a line containing only `---`, then a **description_excerpts** block: each row is `key<TAB>description_excerpt` (plain text, may be truncated).
- For any issue **whose key appears in description_excerpts**, you **must** use that excerpt together with the title and metadata when deciding Raise/Lower and when writing **Reason**. You may **omit** a Raise/Lower row if the excerpt shows impact is **peripheral** (per Halo product context above—e.g. optional profile/photo UX) and **Major** or current priority is appropriate.
- For issues **not** listed in description_excerpts, judge from the metadata table only (same as a title-only pass).
- Output **only** the same fragment as pass 2: starting with `### Recommended Jira priority changes` (no `## Priority review`, no aggregate snapshot tables—the app prepends statistics)."""

_BACKLOG_OVERVIEW_SYSTEM_PASS2B = _BACKLOG_OVERVIEW_SYSTEM_PASS2 + _BACKLOG_OVERVIEW_PASS2B_EXTRA

_BACKLOG_OVERVIEW_SYSTEM_TITLE_SCAN = """You identify Jira tickets whose titles are unclear and should be rewritten.
Output JSON only:
{"keys":["HALO-123","HALO-456"]}
Rules:
- Use only keys from input.
- Return at most 20 keys.
- Prefer keys where the title is vague, generic, missing platform or repro context, or ambiguous—when in doubt between listing and omitting, include the key if it would help a reader.
- No markdown, no prose."""

_BACKLOG_OVERVIEW_SYSTEM_TITLE_REWRITE = """You rewrite unclear Jira titles into clearer, specific titles using metadata and description excerpts.
Output only:
### Title clarity suggestions
| Ticket | Current priority | Current title | Proposed title |
|---|---|---|---|
Rules:
- Ticket key must be from input.
- Current priority must match input.
- Current title should reflect input title.
- Proposed title must be materially clearer and concise.
- No extra sections or prose."""

_SCORECARD_RUBRIC_INSTRUCTIONS = """
**14-point scorecard (five dimensions — integers only, ranges as given):**

**A) feature_importance** (0–4) — product area (Confluence-aligned; infer from title/labels/component/description):
- **4** — Safety-critical / containment promise: fence setup & containment, escape prevention, safety alerts; anything that could show a dog as safe/contained when they are not, or blocks core safety actions.
- **3** — Daily-use / primary flows: walk, onboarding, other high-frequency broadly used flows.
- **2** — Supporting platform / account & commerce: devices, account, login, subscriptions, billing.
- **1** — Edge / niche: beacons, remotes, analytics, low-adoption power-user utilities.
- **0** — Unreleased / N/A.

**B) reach** (0–3) — unique users/week (Amplitude + sanity; infer from ticket or use 0 if no data):
- **3** — > 5,000 / week
- **2** — 1,000–5,000
- **1** — 100–1,000
- **0** — < 100 OR no Amplitude data.

**C) technical_severity** (0–3) — Jira / QA:
- **3** — Blocker/Critical in spirit: crash, data loss.
- **2** — Major: feature broken, no output.
- **1** — Minor: degraded UX, partial failure.
- **0** — Trivial: cosmetic only.

**D) workaround_quality** (0–2) — QA/manual:
- **2** — No workaround; user is stuck.
- **1** — Workaround exists but non-obvious or costly.
- **0** — Easy workaround; user likely will not notice.

**E) regression_risk** (0–2) — Jira + manual:
- **2** — Worked in RC1, broke in RC2.
- **1** — Intermittent or environment-specific.
- **0** — Never worked / new feature gap.

**Required per row (exact keys):**
- The five scores above: `feature_importance`, `reach`, `technical_severity`, `workaround_quality`, `regression_risk`.
- `raw_total` — must equal the sum of the five scores (max **14**).
- `ga_verdict` — exactly one of: **Block GA** | **Fix if capacity** | **PostGA** (use thresholds below).
- `jira_priority` — exactly one of: **Blocker** | **Critical** | **Major** | **Normal** | **Minor** (use mapping below).

**GA verdict thresholds (from raw_total):**
- raw_total **≥ 10** → `ga_verdict`: **Block GA**
- raw_total **6–9** → **Fix if capacity**
- raw_total **≤ 5** → **PostGA**

**Jira priority mapping (same raw_total + safety override):**
- **Blocker** if raw_total ≥ **10** OR (feature_importance == **4** AND (technical_severity ≥ **2** OR workaround_quality ≥ **1**))
- **Critical** if raw_total **8–9** (and not Blocker by the line above)
- **Major** if raw_total **6–7**
- **Normal** if raw_total **4–5**
- **Minor** if raw_total **≤ 3**

Output **JSON only** (no markdown fences):
{"version":"2","rows":[{"key":"PROJ-123","feature_importance":3,"reach":2,"technical_severity":2,"workaround_quality":1,"regression_risk":0,"raw_total":8,"ga_verdict":"Fix if capacity","jira_priority":"Critical","notes":{"reach":"inferred from crash rate"}}]}

Rules:
- Root **version** must be **"2"**.
- Exactly **one** row per issue key in the user message (same keys; preserve order if possible).
- **notes** optional object; short strings per field (≤120 chars each).
- Use only keys from the input; do not invent keys.
"""

_BACKLOG_OVERVIEW_SYSTEM_PASS2_SHORTLIST = (
    """You are an engineering lead triaging a Jira bug backlog for **Halo Collar** (pet GPS / smart collar; mobile apps for pet tracking, maps, geofences, device pairing, etc.). You receive the **full** backlog as **TAB-separated** lines; **priority** is the 4th column (authoritative Jira priority—not inferred from the title text).

"""
    + _HALO_PRODUCT_PRIORITY_CONTEXT_FOR_REVIEW
    + """
**Task:** Pick issue keys that most deserve **follow-up structured priority scoring** (likely mis-prioritized, high user-visible impact vs current Major/Normal/Minor, **GA-blocker** flag, or core safety/geofence/location flows).

Output **JSON only**:
{"keys":["PROJ-1","PROJ-2"]}

Rules:
- Keys must appear in the input; order by **descending** triage urgency (most important first).
- The user message states a **shortlist cap**—return **at most** that many keys.
- **Do not pad:** include only keys that justify scoring; fewer is fine.
- No markdown fences, no prose outside JSON.
"""
)

_BACKLOG_OVERVIEW_SYSTEM_PASS2_SCORECARD = (
    """You are an engineering lead scoring Jira bugs for **Halo Collar** (pet GPS / smart collar). You receive **TAB-separated** metadata for a **subset** of issues (priority = 4th column; authoritative).

"""
    + _HALO_PRODUCT_PRIORITY_CONTEXT_FOR_REVIEW
    + _SCORECARD_RUBRIC_INSTRUCTIONS
)

_BACKLOG_OVERVIEW_SCORECARD_PASS2B_EXTRA = """

**Second pass (description-enriched):** After a line containing only `---`, **description_excerpts** rows are `key<TAB>excerpt`. For keys listed there, you **must** use the excerpt with title/metadata when scoring. For keys not listed, use metadata only. Re-output the **same JSON shape** (full rows for every key in the metadata table)—do not switch to markdown."""

_BACKLOG_OVERVIEW_SYSTEM_PASS2B_SCORECARD = (
    _BACKLOG_OVERVIEW_SYSTEM_PASS2_SCORECARD + _BACKLOG_OVERVIEW_SCORECARD_PASS2B_EXTRA
)


def _sanitize_overview_issue(raw: Any) -> Optional[Dict[str, Any]]:
    """Keep only allowed keys with safe primitive/list values."""
    if not isinstance(raw, dict):
        return None
    key = raw.get('key')
    if not key or not isinstance(key, str):
        return None
    key = key.strip()[:32]
    if not key:
        return None
    out: Dict[str, Any] = {'key': key}
    title = raw.get('title')
    if isinstance(title, str):
        t = title.strip()
        if t:
            out['title'] = t[:_OVERVIEW_MAX_TITLE_LEN]

    def _str_field(name: str, max_len: int = 120):
        v = raw.get(name)
        if isinstance(v, str) and v.strip():
            out[name] = v.strip()[:max_len]

    for name in ('priority', 'status', 'issuetype', 'component', 'parentKey', 'parentSummary', 'epicKey', 'epicSummary', 'sprint'):
        if name in _OVERVIEW_ALLOWED_KEYS:
            _str_field(name, 200 if name in ('parentSummary', 'epicSummary') else 80)

    labels = raw.get('labels')
    if isinstance(labels, list):
        cleaned = []
        for x in labels[:_OVERVIEW_MAX_LABELS]:
            if isinstance(x, str) and x.strip():
                cleaned.append(x.strip()[:80])
        if cleaned:
            out['labels'] = cleaned

    components = raw.get('components')
    if isinstance(components, list):
        cleaned = []
        for x in components[:_OVERVIEW_MAX_COMPONENTS]:
            if isinstance(x, str) and x.strip():
                cleaned.append(x.strip()[:80])
        if cleaned:
            out['components'] = cleaned

    if raw.get('gaBlocker') is True:
        out['gaBlocker'] = True
    if raw.get('needsMoreInfo') is True:
        out['needsMoreInfo'] = True

    desc = raw.get('description')
    if isinstance(desc, str) and desc.strip():
        out['description'] = desc.strip()[:_OVERVIEW_MAX_DESCRIPTION_LEN]

    return out


def _overview_tsv_field(val: Any, max_len: Optional[int] = None) -> str:
    """One cell for tab-separated overview lines; remove chars that break column alignment."""
    if val is None:
        s = ''
    elif isinstance(val, (int, float)):
        s = str(val)
    else:
        s = str(val).replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
        s = ' '.join(s.split())
    if max_len is not None and len(s) > max_len:
        s = s[:max_len]
    return s


def _md_pipe_cell(val: Any, max_len: Optional[int] = None) -> str:
    """Escape for markdown pipe tables."""
    return _overview_tsv_field(val, max_len).replace('|', '\\|')


_HALO_PRIORITY_SNAPSHOT_ORDER = (
    'Blocker',
    'Critical',
    'Major',
    'Normal',
    'Minor',
    'Trivial',
)
_STATUS_SNAPSHOT_MAX_ROWS = 12


def _overview_issue_priority_label(issue: Dict[str, Any]) -> str:
    p = issue.get('priority')
    if isinstance(p, str) and p.strip():
        return p.strip()
    return '(none)'


def _overview_issue_status_label(issue: Dict[str, Any]) -> str:
    s = issue.get('status')
    if isinstance(s, str) and s.strip():
        return s.strip()
    return '(No status)'


def _compute_backlog_snapshot_stats(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(issues)
    by_pri = Counter(_overview_issue_priority_label(i) for i in issues)
    by_st = Counter(_overview_issue_status_label(i) for i in issues)
    return {
        'total': total,
        'by_priority': dict(by_pri),
        'by_status': dict(by_st),
    }


def _render_backlog_snapshot_markdown(issues: List[Dict[str, Any]]) -> str:
    """Deterministic ### Backlog snapshot + ### By status (no LLM)."""
    stats = _compute_backlog_snapshot_stats(issues)
    total = stats['total']
    denom = total if total > 0 else 1
    lines: List[str] = []
    lines.append('### Backlog snapshot')
    lines.append('')
    lines.append('Counts are from the **filtered backlog** in this overview (same issues the model triages).')
    lines.append('')
    lines.append('| Priority | Count | % |')
    lines.append('|---:|---:|---:|')
    by_p = stats['by_priority']
    known = frozenset(_HALO_PRIORITY_SNAPSHOT_ORDER)
    ordered_pri: List[str] = [k for k in _HALO_PRIORITY_SNAPSHOT_ORDER if by_p.get(k, 0) > 0]
    for k in sorted(kk for kk in by_p if kk not in known and by_p[kk] > 0):
        ordered_pri.append(k)
    for label in ordered_pri:
        c = by_p[label]
        pct = round(100.0 * c / denom, 1)
        lines.append(f'| {_md_pipe_cell(label)} | {c} | {pct} |')
    if total > 0:
        lines.append(f'| **Total** | {total} | 100 |')
    lines.append('')
    lines.append('### By status')
    lines.append('')
    lines.append('| Status | Count | % |')
    lines.append('|---:|---:|---:|')
    by_s = sorted(stats['by_status'].items(), key=lambda x: (-x[1], x[0]))
    top = by_s[:_STATUS_SNAPSHOT_MAX_ROWS]
    other = sum(c for _, c in by_s[_STATUS_SNAPSHOT_MAX_ROWS:])
    for label, c in top:
        pct = round(100.0 * c / denom, 1)
        lines.append(f'| {_md_pipe_cell(label, 160)} | {c} | {pct} |')
    if other > 0:
        rest_n = len(by_s) - _STATUS_SNAPSHOT_MAX_ROWS
        lbl = f'Other ({rest_n} other statuses)' if rest_n != 1 else 'Other (1 other status)'
        pct = round(100.0 * other / denom, 1)
        lines.append(f'| {_md_pipe_cell(lbl)} | {other} | {pct} |')
    return '\n'.join(lines)


def _strip_leading_h2_priority_review(markdown: str) -> str:
    """Remove a leading ## Priority review block so server can prepend snapshot + same H2."""
    if not markdown:
        return ''
    lines = markdown.split('\n')
    i = 0
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    if i < len(lines) and lines[i].strip() == '## Priority review':
        i += 1
        while i < len(lines) and lines[i].strip() == '':
            i += 1
        return '\n'.join(lines[i:]).strip()
    return markdown.strip()


def _assemble_priority_review_with_snapshot(issues: List[Dict[str, Any]], llm_fragment: str) -> str:
    snapshot = _render_backlog_snapshot_markdown(issues)
    body = _strip_leading_h2_priority_review(llm_fragment)
    parts = ['## Priority review', '', snapshot]
    if body:
        parts.extend(['', body])
    return '\n'.join(parts).strip()


def _format_issues_for_overview_prompt(
    issues: List[Dict[str, Any]],
    truncated: bool,
    total_submitted: int,
    *,
    prompt_variant: str = 'pass1',
    description_keys_ordered: Optional[List[str]] = None,
    keys_filter_ordered: Optional[List[str]] = None,
    shortlist_cap: Optional[int] = None,
) -> str:
    """Build user message text for Claude (pass1 / pass2 / pass2b / title_scan / title_rewrite / scorecard variants)."""
    by_key_upper = {
        str(i.get('key', '')).strip().upper(): i
        for i in issues
        if i.get('key')
    }
    if keys_filter_ordered:
        issue_list: List[Dict[str, Any]] = []
        for k in keys_filter_ordered:
            u = (k or '').strip().upper()
            if u in by_key_upper:
                issue_list.append(by_key_upper[u])
    else:
        issue_list = list(issues)

    if prompt_variant == 'pass2b':
        lines = [
            f"The following {len(issue_list)} issues: first block is metadata for **every** issue (tab-separated). "
            f"After a line that is only `---`, **description_excerpts** rows apply **only** to those keys—use them for Raise/Lower per system prompt.",
        ]
    elif prompt_variant == 'title_rewrite':
        lines = [
            f"The following {len(issue_list)} issues: first block is metadata for **every** issue (tab-separated). "
            f"After a line that is only `---`, **description_excerpts** rows apply **only** to those keys—use them when rewriting titles.",
        ]
    elif prompt_variant == 'pass2_shortlist':
        cap = int(shortlist_cap) if shortlist_cap is not None else 40
        lines = [
            f"The following {len(issue_list)} issues are the current filtered backlog (metadata only).",
            f"**Shortlist cap:** return at most **{cap}** keys in the JSON array.",
        ]
    elif prompt_variant in ('pass2_score', 'pass2b_score'):
        lines = [
            f"The following {len(issue_list)} issues are the **scoring subset** (tab-separated metadata). "
            f"You must output one scorecard row per key in this list.",
        ]
        if prompt_variant == 'pass2b_score':
            lines.append(
                "After `---`, **description_excerpts** apply only to listed keys—use them when scoring those keys."
            )
    else:
        lines = [
            f"The following {len(issue_list)} issues are the current filtered backlog (metadata only).",
        ]
    if truncated:
        lines.append(f"Note: Analyzing first {len(issues)} of {total_submitted} issues submitted (cap for context size).")
    lines.append('')
    if prompt_variant == 'pass1':
        lines.append(
            'Your task for this message: themes, needs clarification, duplicates/clusters, and other notes only. '
            'Do **not** output ## Priority review or Jira priority recommendations.'
        )
    elif prompt_variant == 'title_scan':
        lines.append(
            'Your task for this message: return only JSON {"keys":[...]} with issue keys whose current titles should be rewritten for clarity. '
            'No markdown, no prose.'
        )
    elif prompt_variant == 'title_rewrite':
        lines.append(
            'Your task for this message: output only the `### Title clarity suggestions` markdown table. '
            'Use description_excerpts after `---` for listed keys.'
        )
    elif prompt_variant == 'pass2b':
        lines.append(
            'Your task for this message: output **only** the `### Recommended Jira priority changes` subsection (and its table when applicable)—do **not** output `## Priority review` or aggregate snapshot tables. '
            'HALO Jira priority order (highest first): Blocker > Critical > Major > Normal > Minor > Trivial. '
            'For each issue key, **Current priority** in your output must match the **priority** column (4th tab-separated field) in the main table—not the title. '
            'List Raise/Lower only in the reprioritization table; omit tickets that need no change. '
            '**Hard rule:** Never a row with Current priority Blocker and Raise/Raise to Blocker. '
            'Raise to Blocker only when Current is Critical or lower. Self-check: target must not equal Current. '
            'For keys present in **description_excerpts** after `---`, you **must** incorporate those excerpts into judgment and Reason.'
        )
    elif prompt_variant == 'pass2_shortlist':
        lines.append(
            'Your task for this message: return **only** JSON `{"keys":["PROJ-1",...]}` per the system prompt (shortlist for scoring). '
            'No markdown, no prose.'
        )
    elif prompt_variant == 'pass2_score':
        lines.append(
            'Your task for this message: return **only** the JSON scorecard object per the system prompt (one row per issue key in the table). '
            'No markdown tables, no `## Priority review`.'
        )
    elif prompt_variant == 'pass2b_score':
        lines.append(
            'Your task for this message: return **only** the JSON scorecard object (description-enriched pass). '
            'One row per key in the metadata table; incorporate **description_excerpts** where provided.'
        )
    else:
        lines.append(
            'Your task for this message: output **only** the `### Recommended Jira priority changes` subsection (and its table when applicable)—do **not** output `## Priority review` or aggregate snapshot tables. '
            'HALO Jira priority order (highest first): Blocker > Critical > Major > Normal > Minor > Trivial. '
            'For each issue key, **Current priority** in your output must match the **priority** column (4th tab-separated field) in the data below—not the title. '
            'List Raise/Lower only in the reprioritization table; omit tickets that need no change. '
            '**Hard rule:** Never a row with Current priority Blocker and Raise/Raise to Blocker. '
            'Raise to Blocker only when Current is Critical or lower. Self-check: target must not equal Current.'
        )
    lines.append('')
    lines.append(
        'Issues below: each line is TAB-separated (use the tab character as delimiter only—do not parse as pipe `|`). '
        'Columns: key, title, type, priority, status, components, labels, parent, epic, flags. '
        'The **priority** column (4th) is the authoritative Jira priority for that key.'
    )
    lines.append(
        '\t'.join(
            ['key', 'title', 'type', 'priority', 'status', 'components', 'labels', 'parent', 'epic', 'flags']
        )
    )
    for i in issue_list:
        comps = i.get('components') or ([] if not i.get('component') else [i['component']])
        comp_s = ','.join(comps) if comps else ''
        labels = ','.join(i.get('labels') or [])
        flags = []
        if i.get('gaBlocker'):
            flags.append('GA-blocker')
        if i.get('needsMoreInfo'):
            flags.append('needs-info')
        flag_s = ','.join(flags)
        parent = i.get('parentKey') or ''
        if i.get('parentSummary'):
            ps = (i.get('parentSummary') or '')[:60]
            parent = f"{parent} ({ps})" if parent else ps
        epic = i.get('epicKey') or ''
        if i.get('epicSummary'):
            es = (i.get('epicSummary') or '')[:40]
            epic = f"{epic} ({es})" if epic else es
        row = [
            _overview_tsv_field(i.get('key')),
            _overview_tsv_field((i.get('title') or ''), _OVERVIEW_MAX_TITLE_LEN),
            _overview_tsv_field(i.get('issuetype') or ''),
            _overview_tsv_field(i.get('priority') or ''),
            _overview_tsv_field(i.get('status') or ''),
            _overview_tsv_field(comp_s, 240),
            _overview_tsv_field(labels, 400),
            _overview_tsv_field(parent, 140),
            _overview_tsv_field(epic, 120),
            _overview_tsv_field(flag_s),
        ]
        lines.append('\t'.join(row))

    if description_keys_ordered:
        lines.append('')
        lines.append('---')
        lines.append(
            'description_excerpts (tab-separated: key, description_excerpt). '
            'Truncated plain text; use for Jira priority judgment for these keys only.'
        )
        lines.append('\t'.join(['key', 'description_excerpt']))
        for dk in description_keys_ordered:
            issue = by_key_upper.get((dk or '').strip().upper())
            key_field = _overview_tsv_field(dk)
            if not issue:
                lines.append(
                    '\t'.join([key_field, _overview_tsv_field('(issue not in backlog batch)', 80)])
                )
                continue
            raw_desc = issue.get('description')
            if isinstance(raw_desc, str) and raw_desc.strip():
                excerpt = _overview_tsv_field(raw_desc, _OVERVIEW_DESCRIPTION_EXCERPT_LEN)
            else:
                excerpt = _overview_tsv_field('(no description provided)', 80)
            lines.append('\t'.join([key_field, excerpt]))

    lines.append('')
    if prompt_variant == 'pass1':
        lines.append('Produce the markdown overview as instructed in the system prompt (no ## Priority review).')
    elif prompt_variant == 'title_scan':
        lines.append('Return only JSON: {"keys":[...]}')
    elif prompt_variant == 'title_rewrite':
        lines.append('Produce only the `### Title clarity suggestions` fragment.')
    elif prompt_variant == 'pass2b':
        lines.append(
            'Produce **only** the `### Recommended Jira priority changes` fragment as instructed (second pass / description excerpts).'
        )
    elif prompt_variant == 'pass2_shortlist':
        lines.append('Return only JSON: {"keys":[...]} matching the shortlist cap.')
    elif prompt_variant == 'pass2_score':
        lines.append('Return only the JSON scorecard object (version + rows) as instructed.')
    elif prompt_variant == 'pass2b_score':
        lines.append('Return only the JSON scorecard object (description-enriched pass).')
    else:
        lines.append(
            'Produce **only** the `### Recommended Jira priority changes` fragment as instructed in the system prompt.'
        )
    return '\n'.join(lines)


def _basic_auth_configured() -> bool:
    return bool(Config.JIRA_BASE_URL and Config.JIRA_EMAIL and Config.JIRA_API_TOKEN)


def _oauth_configured() -> bool:
    return bool(
        Config.JIRA_CLIENT_ID and Config.JIRA_CLIENT_SECRET and Config.JIRA_BASE_URL
    )


def _jira_configured() -> bool:
    """True if we can call Jira (Basic auth or OAuth with tokens)."""
    if _basic_auth_configured():
        return True
    if _oauth_configured() and jira_oauth.get_valid_access_token():
        return True
    return False


@jira_bp.route('/status', methods=['GET'])
def get_jira_status():
    """Return whether Jira is configured and how (Basic preferred over OAuth when both set)."""
    basic = _basic_auth_configured()
    oauth_has_tokens = _oauth_configured() and bool(jira_oauth.get_valid_access_token())
    return jsonify({
        'configured': basic or oauth_has_tokens,
        'base_url': Config.JIRA_BASE_URL or None,
        'auth_type': 'basic' if basic else ('oauth' if oauth_has_tokens else None),
        'oauth_can_connect': _oauth_configured() and bool(Config.APP_BASE_URL),
        'oauth_connected': oauth_has_tokens,
    })


@jira_bp.route('/oauth/authorize', methods=['GET'])
def oauth_authorize():
    """Redirect user to Atlassian to authorize the app. Requires JIRA_CLIENT_ID, JIRA_CLIENT_SECRET, APP_BASE_URL."""
    if not _oauth_configured():
        return jsonify({
            'status': 'error',
            'message': 'Jira OAuth not configured. Set JIRA_CLIENT_ID, JIRA_CLIENT_SECRET, APP_BASE_URL.',
        }), 400
    callback = jira_oauth.get_callback_url(request.url_root.rstrip('/'))
    if not callback:
        return jsonify({
            'status': 'error',
            'message': 'APP_BASE_URL must be set for OAuth callback (e.g. https://insight.halocollar.com).',
        }), 400
    state = secrets.token_urlsafe(24)
    session[JIRA_OAUTH_STATE_KEY] = state
    url = jira_oauth.build_authorize_url(state, request.url_root.rstrip('/'))
    if not url:
        return jsonify({'status': 'error', 'message': 'Could not build authorize URL'}), 400
    return redirect(url)


@jira_bp.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    """Handle redirect from Atlassian: exchange code for tokens, then redirect to frontend."""
    code = request.args.get('code')
    state = request.args.get('state')
    if not code:
        return redirect(_frontend_redirect(error='missing_code'))
    if state != session.get(JIRA_OAUTH_STATE_KEY):
        return redirect(_frontend_redirect(error='invalid_state'))
    session.pop(JIRA_OAUTH_STATE_KEY, None)
    callback = jira_oauth.get_callback_url(request.url_root.rstrip('/'))
    if not callback:
        return redirect(_frontend_redirect(error='no_callback'))
    try:
        result = jira_oauth.exchange_code_for_tokens(code, callback)
        jira_oauth.save_tokens(
            result['access_token'],
            result['refresh_token'],
            result['expires_in'],
        )
        return redirect(_frontend_redirect(connected='1'))
    except Exception as e:
        logger.exception("Jira OAuth token exchange failed: %s", e)
        return redirect(_frontend_redirect(error='exchange_failed'))


@jira_bp.route('/oauth/disconnect', methods=['POST'])
def oauth_disconnect():
    """Clear stored OAuth tokens so user can reconnect or use Basic auth."""
    jira_oauth.clear_tokens()
    return jsonify({'status': 'success', 'message': 'Jira OAuth disconnected'}), 200


def _frontend_redirect(connected: str = None, error: str = None) -> str:
    """Build redirect URL to frontend Jira status view."""
    base = (Config.APP_BASE_URL or '').strip().rstrip('/')
    if not base:
        base = '/'
    path = '/'
    params = ['mode=jira-status']
    if connected:
        params.append('connected=1')
    if error:
        params.append(f'oauth_error={error}')
    return f"{base}{path}?{'&'.join(params)}"


@jira_bp.route('/projects', methods=['GET'])
def get_projects():
    """
    List projects visible to the configured Jira user (API token or OAuth).
    Use this to verify access and see exact project keys (e.g. for Bug Triage).
    """
    if not _jira_configured():
        return jsonify({
            'status': 'error',
            'message': 'Jira is not connected. Configure Basic auth or OAuth first.',
        }), 503

    try:
        client = JiraClient()
        projects = client.get_projects()
        # Normalize to list of { id, key, name }
        out = []
        for p in projects:
            out.append({
                'id': p.get('id'),
                'key': p.get('key'),
                'name': p.get('name'),
            })
        return jsonify({
            'status': 'success',
            'data': out,
            'count': len(out),
        })
    except requests.exceptions.HTTPError as e:
        logger.warning("Jira projects HTTP error: %s %s", e.response.status_code if e.response else None, getattr(e.response, 'text', '')[:200])
        message, error_details, status_code = _jira_http_error_response(e, 'Failed to fetch projects from Jira')
        return jsonify({
            'status': 'error',
            'message': message,
            'error_details': error_details,
        }), status_code if 400 <= status_code < 600 else 500
    except Exception as e:
        logger.exception("Jira projects fetch failed")
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to fetch projects from Jira',
        }), 500


@jira_bp.route('/myself', methods=['GET'])
def get_myself():
    """Return current Jira user (validates auth)."""
    if not _jira_configured():
        return jsonify({
            'status': 'error',
            'message': 'Jira is not connected.',
        }), 503

    try:
        client = JiraClient()
        me = client.get_myself()
        return jsonify({
            'status': 'success',
            'data': {
                'accountId': me.get('accountId'),
                'displayName': me.get('displayName'),
                'emailAddress': me.get('emailAddress'),
            },
        })
    except requests.exceptions.HTTPError as e:
        logger.warning("Jira myself HTTP error: %s %s", e.response.status_code if e.response else None, getattr(e.response, 'text', '')[:200])
        message, error_details, status_code = _jira_http_error_response(e, 'Failed to get current user from Jira')
        return jsonify({
            'status': 'error',
            'message': message,
            'error_details': error_details,
        }), status_code if 400 <= status_code < 600 else 500
    except Exception as e:
        logger.exception("Jira myself fetch failed")
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to get current user from Jira',
        }), 500


@jira_bp.route('/issues', methods=['GET'])
def get_issues():
    """
    Fetch issues from Jira for Bug Triage. Optional query: project (default HALO), max_results (1–1000, default 1000),
    ancestor_key (e.g. HALO-23306) to restrict to that issue and its descendants (children, grandchildren, etc.),
    issuetype (default Bug) to filter by issue type; use issuetype= or issuetype=all for all types.
    Uses Basic auth (JIRA_EMAIL + JIRA_API_TOKEN) when set; otherwise OAuth. Paginates Jira API to fetch beyond 100.
    """
    if not _jira_configured():
        return jsonify({
            'status': 'error',
            'message': 'Jira is not connected. Use email + API token in .env, or connect via OAuth (Tools → Jira connection).',
        }), 503

    try:
        project = request.args.get('project', 'HALO').strip() or 'HALO'
        max_results = min(max(int(request.args.get('max_results', 1000)), 1), 1000)  # default 1000, cap 1000
        ancestor_key = (request.args.get('ancestor_key') or request.args.get('parent_key') or '').strip() or None
        issuetype_arg = (request.args.get('issuetype') or 'Bug').strip()
        issuetype = None if issuetype_arg.lower() in ('', 'all', '*') else issuetype_arg
        require_parent_context_arg = (request.args.get('require_parent_context') or '1').strip().lower()
        require_parent_context = require_parent_context_arg not in ('0', 'false', 'no')
        client = JiraClient()
        triage_result = client.fetch_issues_for_triage(
            project=project,
            max_results=max_results,
            ancestor_key=ancestor_key,
            issuetype=issuetype,  # default from param is Bug; None means all types (e.g. ?issuetype=all)
            require_parent_context=require_parent_context,
        )
        issues = triage_result.get('issues', [])
        return jsonify({
            'status': 'success',
            'data': issues,
            'count': len(issues),
            'max_results_requested': max_results,
            'count_before_parent_filter': triage_result.get('count_before_parent_filter', len(issues)),
            'count_after_parent_filter': triage_result.get('count_after_parent_filter', len(issues)),
            'parent_filter_applied': triage_result.get('parent_filter_applied', False),
        })
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except requests.exceptions.HTTPError as e:
        logger.warning("Jira issues HTTP error: %s %s", e.response.status_code if e.response else None, getattr(e.response, 'text', '')[:200])
        message, error_details, status_code = _jira_http_error_response(e, 'Failed to fetch issues from Jira')
        return jsonify({
            'status': 'error',
            'message': message,
            'error_details': error_details,
        }), status_code if 400 <= status_code < 600 else 500
    except Exception as e:
        logger.exception("Jira fetch failed")
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to fetch issues from Jira',
        }), 500


def _overview_progress_event(step: str, phase: str, completed: List[str]) -> Dict[str, Any]:
    return {'type': 'progress', 'step': step, 'phase': phase, 'completed': list(completed)}


def _join_overview_chunks(part2: str, part1: str, title_section: str) -> str:
    """Same join order as terminal overview: part2, part1, title."""
    chunks: List[str] = []
    p2 = (part2 or '').strip()
    p1 = (part1 or '').strip()
    t = (title_section or '').strip()
    if p2:
        chunks.append(p2)
    if p1:
        chunks.append(p1)
    if t:
        chunks.append(t)
    return '\n\n'.join(chunks).strip()


def _overview_partial_event(milestone: str, markdown: str) -> Dict[str, Any]:
    return {'type': 'partial', 'milestone': milestone, 'markdown': markdown}


def _title_suggestions_no_candidates_markdown(max_keys: int) -> str:
    """Explicit markdown when the title scan returns no keys (so the overview always documents title pass)."""
    return (
        '### Title clarity suggestions\n\n'
        '*No tickets were selected for title rewrite in this run.* '
        'The title scan did not flag any issue keys as unclear enough to propose new titles '
        f'(scan cap: **{max_keys}** keys).'
    )


def _overview_error_result(
    exc: Exception,
    *,
    failed_step: str,
    completed_steps: List[str],
) -> Dict[str, Any]:
    http = 500
    error_code = 'BACKLOG_OVERVIEW_ERROR'
    details: Dict[str, Any] = {}
    if isinstance(exc, RateLimitError):
        http = exc.status_code
        error_code = exc.error_code
        details = dict(exc.details or {})
    elif isinstance(exc, AppTimeoutError):
        http = exc.status_code
        error_code = exc.error_code
        details = dict(exc.details or {})
    elif isinstance(exc, ClaudeAPIError):
        http = exc.status_code
        error_code = exc.error_code
        details = dict(exc.details or {})
    elif isinstance(exc, AppException):
        http = exc.status_code
        error_code = exc.error_code
        details = dict(exc.details or {})
    msg = getattr(exc, 'message', None) or str(exc)
    retry_after = details.get('retry_after_seconds')
    return {
        'type': 'result',
        'status': 'error',
        'http_status': http,
        'message': msg,
        'error_code': error_code,
        'failed_step': failed_step,
        'completed_steps': list(completed_steps),
        'details': details,
        'retry_after_seconds': retry_after,
    }


def _iter_backlog_overview_events(
    claude_service: Any,
    batch: List[Dict[str, Any]],
    truncated: bool,
    total_submitted: int,
    user_message_pass1: str,
    user_message_pass2: str,
    protector: Any,
    submitted_count_before_parent_filter: int,
    submitted_count_after_parent_filter: int,
    *,
    use_scorecard: bool = False,
) -> Iterator[Dict[str, Any]]:
    """
    Yields progress dicts, optional partial markdown (type=='partial'), and a terminal result (type=='result').
    On partial success after pass2, result status is 'success' with meta.overview_incomplete.
    """
    completed: List[str] = []
    overview_incomplete = False
    omitted_sections: List[str] = []
    incomplete_reasons: List[str] = []
    first_failed_optional_step: Optional[str] = None
    overview_temperature = Config.JIRA_BACKLOG_OVERVIEW_TEMPERATURE
    min_scorecard_delta = Config.JIRA_TRIAGE_SCORECARD_MIN_DELTA_RANKS
    scorecards_by_key: Dict[str, Any] = {}
    scorecard_errors: List[str] = []
    scorecard_config_hash: Optional[str] = None
    scorecard_shortlist_size = 0
    scorecard_scored_keys = 0
    scorecard_sl_keys_ordered: List[str] = []
    scorecard_scored_keys_ordered: List[str] = []

    yield _overview_progress_event('pass1', 'start', completed)
    try:
        r1 = claude_service.send_message(
            message=user_message_pass1,
            model=None,
            max_tokens=Config.JIRA_BACKLOG_OVERVIEW_PASS1_MAX_TOKENS,
            system_prompt=_BACKLOG_OVERVIEW_SYSTEM_PASS1,
            temperature=overview_temperature,
        )
    except (RateLimitError, AppTimeoutError, ClaudeAPIError, AppException) as e:
        logger.exception('backlog-overview: pass1 failed: %s', e)
        yield _overview_error_result(e, failed_step='pass1', completed_steps=completed)
        return
    except Exception as e:
        logger.exception('backlog-overview: pass1 failed: %s', e)
        yield _overview_error_result(e, failed_step='pass1', completed_steps=completed)
        return
    completed.append('pass1')
    yield _overview_progress_event('pass1', 'done', completed)

    part1 = (r1.content or '').strip()
    source_priorities = {
        str(i.get('key', '')).strip().upper(): (_normalize_priority_label(i.get('priority')) or '')
        for i in batch
        if i.get('key')
    }
    source_by_key = {
        str(i.get('key', '')).strip().upper(): {
            'priority': str(i.get('priority') or '').strip(),
            'title': str(i.get('title') or '').strip(),
            'description': str(i.get('description') or '').strip(),
        }
        for i in batch
        if i.get('key')
    }

    yield _overview_progress_event('pass2', 'start', completed)
    try:
        if use_scorecard:
            scorecard_config_hash = scorecard_framework_config_hash()
            msg_sl = _format_issues_for_overview_prompt(
                batch,
                truncated,
                total_submitted,
                prompt_variant='pass2_shortlist',
                shortlist_cap=Config.JIRA_TRIAGE_SCORECARD_MAX_KEYS,
            )
            if protector:
                msg_sl = protector.redact_text(msg_sl)
            r_sl = claude_service.send_message(
                message=msg_sl,
                model=None,
                max_tokens=Config.JIRA_TRIAGE_SCORECARD_SHORTLIST_MAX_TOKENS,
                system_prompt=_BACKLOG_OVERVIEW_SYSTEM_PASS2_SHORTLIST,
                temperature=overview_temperature,
            )
            valid_keys_set = set(source_by_key.keys())
            sl_keys, sl_errs = parse_shortlist_keys_json(
                r_sl.content or '',
                valid_keys_set,
                Config.JIRA_TRIAGE_SCORECARD_MAX_KEYS,
            )
            scorecard_errors.extend(sl_errs)
            scorecard_shortlist_size = len(sl_keys)
            if Config.JIRA_TRIAGE_SCORECARD_INCLUDE_GA_BLOCKERS:
                scored_keys = union_shortlist_with_ga_blockers(
                    sl_keys,
                    batch,
                    Config.JIRA_TRIAGE_SCORECARD_MAX_KEYS,
                )
            else:
                cap = max(0, Config.JIRA_TRIAGE_SCORECARD_MAX_KEYS)
                scored_keys = sl_keys[:cap] if cap else []
            scorecard_sl_keys_ordered = list(sl_keys)
            scorecard_scored_keys_ordered = list(scored_keys)
            scorecard_scored_keys = len(scored_keys)
            tokens_used = (getattr(r1, 'tokens_used', 0) or 0) + (getattr(r_sl, 'tokens_used', 0) or 0)
            models_used = [r1.model, r_sl.model]
            llm_rounds = 2
            if not scored_keys:
                part2_draft = (
                    '### Recommended Jira priority changes\n\n'
                    '*No keys were selected for scorecard triage in this run.*'
                )
            else:
                msg_sc = _format_issues_for_overview_prompt(
                    batch,
                    truncated,
                    total_submitted,
                    prompt_variant='pass2_score',
                    keys_filter_ordered=scored_keys,
                )
                if protector:
                    msg_sc = protector.redact_text(msg_sc)
                r_sc = claude_service.send_message(
                    message=msg_sc,
                    model=None,
                    max_tokens=Config.JIRA_BACKLOG_OVERVIEW_PASS2_MAX_TOKENS,
                    system_prompt=_BACKLOG_OVERVIEW_SYSTEM_PASS2_SCORECARD,
                    temperature=overview_temperature,
                )
                tokens_used += getattr(r_sc, 'tokens_used', 0) or 0
                models_used.append(r_sc.model)
                llm_rounds = 3
                batch_parsed, perrs = parse_scorecard_json(r_sc.content or '')
                scorecard_errors.extend(perrs)
                if batch_parsed and batch_parsed.rows:
                    for rrow in batch_parsed.rows:
                        scorecard_errors.extend(scorecard_row_mismatch_warnings(rrow))
                    part2_draft = recommendations_to_reprioritization_markdown(
                        batch_parsed,
                        source_by_key,
                        min_scorecard_delta,
                    )
                    scorecards_by_key = build_scorecards_by_key_meta(
                        batch_parsed,
                        source_by_key,
                        min_scorecard_delta,
                    )
                else:
                    part2_draft = (
                        '### Recommended Jira priority changes\n\n'
                        '*Scorecard JSON was missing, empty, or could not be parsed.*'
                    )
        else:
            r2 = claude_service.send_message(
                message=user_message_pass2,
                model=None,
                max_tokens=Config.JIRA_BACKLOG_OVERVIEW_PASS2_MAX_TOKENS,
                system_prompt=_BACKLOG_OVERVIEW_SYSTEM_PASS2,
                temperature=overview_temperature,
            )
            part2_draft = (r2.content or '').strip()
            tokens_used = (getattr(r1, 'tokens_used', 0) or 0) + (getattr(r2, 'tokens_used', 0) or 0)
            models_used = [r1.model, r2.model]
            llm_rounds = 2
    except (RateLimitError, AppTimeoutError, ClaudeAPIError, AppException) as e:
        logger.exception('backlog-overview: pass2 failed: %s', e)
        yield _overview_error_result(e, failed_step='pass2', completed_steps=completed)
        return
    except Exception as e:
        logger.exception('backlog-overview: pass2 failed: %s', e)
        yield _overview_error_result(e, failed_step='pass2', completed_steps=completed)
        return
    completed.append('pass2')
    yield _overview_progress_event('pass2', 'done', completed)

    part2_draft, dropped2 = _validate_reprioritization_rows(
        part2_draft,
        source_priorities=source_priorities,
    )
    part2_draft = _regroup_reprioritization_section_by_component(part2_draft, batch)
    part2 = _assemble_priority_review_with_snapshot(batch, part2_draft)
    yield _overview_partial_event('after_pass2', _join_overview_chunks(part2, part1, ''))
    snapshot_stats = _compute_backlog_snapshot_stats(batch)
    deep_key_count = 0
    deep_pass_applied = False
    dropped_invalid_rows = dropped2.get('invalid', 0)
    dropped_mismatch_rows = dropped2.get('mismatch', 0)
    title_rewrite_candidates = 0
    title_rewrite_rows = 0
    title_rewrite_rows_dropped = 0
    title_rewrite_pass_applied = False
    title_rewrite_no_candidates = False
    title_rewrite_section = ''

    if (
        Config.JIRA_BACKLOG_OVERVIEW_DEEP_PASS_ENABLED
        and part2_draft
        and 'Recommended Jira priority changes' in part2_draft
    ):
        deep_keys = _extract_reprioritization_keys(part2_draft)
        max_deep = max(0, Config.JIRA_BACKLOG_OVERVIEW_DEEP_MAX_KEYS)
        if deep_keys and max_deep > 0:
            if len(deep_keys) > max_deep:
                deep_keys = deep_keys[:max_deep]
            deep_key_count = len(deep_keys)
            if use_scorecard:
                user_message_pass2b = _format_issues_for_overview_prompt(
                    batch,
                    truncated,
                    total_submitted,
                    prompt_variant='pass2b_score',
                    keys_filter_ordered=deep_keys,
                    description_keys_ordered=deep_keys,
                )
                pass2b_system = _BACKLOG_OVERVIEW_SYSTEM_PASS2B_SCORECARD
            else:
                user_message_pass2b = _format_issues_for_overview_prompt(
                    batch,
                    truncated,
                    total_submitted,
                    prompt_variant='pass2b',
                    description_keys_ordered=deep_keys,
                )
                pass2b_system = _BACKLOG_OVERVIEW_SYSTEM_PASS2B
            if protector:
                user_message_pass2b = protector.redact_text(user_message_pass2b)
            yield _overview_progress_event('pass2b', 'start', completed)
            try:
                r2b = claude_service.send_message(
                    message=user_message_pass2b,
                    model=None,
                    max_tokens=Config.JIRA_BACKLOG_OVERVIEW_PASS2B_MAX_TOKENS,
                    system_prompt=pass2b_system,
                    temperature=overview_temperature,
                )
            except Exception as e:
                logger.warning('backlog-overview: pass2b failed (partial overview): %s', e)
                overview_incomplete = True
                omitted_sections.append('priority_deep_refine')
                incomplete_reasons.append(f'Deep priority refine failed: {getattr(e, "message", None) or str(e)}')
                first_failed_optional_step = first_failed_optional_step or 'pass2b'
                yield _overview_progress_event('pass2b', 'error', completed)
            else:
                if use_scorecard:
                    batch_b, perrs_b = parse_scorecard_json(r2b.content or '')
                    scorecard_errors.extend(perrs_b)
                    if batch_b and batch_b.rows:
                        for rrow in batch_b.rows:
                            scorecard_errors.extend(scorecard_row_mismatch_warnings(rrow))
                        part2b_out = recommendations_to_reprioritization_markdown(
                            batch_b,
                            source_by_key,
                            min_scorecard_delta,
                        )
                        scorecards_by_key = build_scorecards_by_key_meta(
                            batch_b,
                            source_by_key,
                            min_scorecard_delta,
                        )
                        scorecard_config_hash = scorecard_framework_config_hash()
                    else:
                        part2b_out = ''
                else:
                    part2b_out = (r2b.content or '').strip()
                part2b_out, dropped2b = _validate_reprioritization_rows(
                    part2b_out,
                    source_priorities=source_priorities,
                )
                part2b_out = _regroup_reprioritization_section_by_component(part2b_out, batch)
                tokens_used += getattr(r2b, 'tokens_used', 0) or 0
                models_used.append(r2b.model)
                llm_rounds = 3
                dropped_invalid_rows += dropped2b.get('invalid', 0)
                dropped_mismatch_rows += dropped2b.get('mismatch', 0)
                pass2b_ok = bool(part2b_out.strip()) and (
                    '### Recommended Jira priority changes' in part2b_out
                )
                if pass2b_ok:
                    part2 = _assemble_priority_review_with_snapshot(batch, part2b_out)
                    deep_pass_applied = True
                    completed.append('pass2b')
                    yield _overview_progress_event('pass2b', 'done', completed)
                    logger.info(
                        'backlog-overview: pass2b description refine issues=%s keys=%s scorecard=%s',
                        len(batch),
                        deep_key_count,
                        use_scorecard,
                    )
                else:
                    logger.warning(
                        'backlog-overview: pass2b missing valid ### Recommended Jira priority changes; keeping pass2 output keys=%s',
                        deep_key_count,
                    )
                    completed.append('pass2b')
                    yield _overview_progress_event('pass2b', 'done', completed)

    if 'pass2b' in completed:
        yield _overview_partial_event('after_pass2b', _join_overview_chunks(part2, part1, ''))

    if Config.JIRA_BACKLOG_TITLE_REWRITE_ENABLED and not Config.JIRA_BACKLOG_TITLE_REWRITE_DISABLED:
        all_keys = list(source_by_key.keys())
        max_keys = max(0, Config.JIRA_BACKLOG_TITLE_REWRITE_MAX_KEYS)
        max_rows = max(0, Config.JIRA_BACKLOG_TITLE_REWRITE_MAX_ROWS)
        if all_keys and max_keys > 0 and max_rows > 0:
            user_message_title_scan = _format_issues_for_overview_prompt(
                batch,
                truncated,
                total_submitted,
                prompt_variant='title_scan',
            )
            if protector:
                user_message_title_scan = protector.redact_text(user_message_title_scan)
            yield _overview_progress_event('title_scan', 'start', completed)
            try:
                r_title_scan = claude_service.send_message(
                    message=user_message_title_scan,
                    model=None,
                    max_tokens=min(250, max(120, Config.JIRA_BACKLOG_TITLE_REWRITE_MAX_TOKENS // 2)),
                    system_prompt=_BACKLOG_OVERVIEW_SYSTEM_TITLE_SCAN,
                    temperature=overview_temperature,
                )
            except Exception as e:
                logger.warning('backlog-overview: title_scan failed (partial overview): %s', e)
                overview_incomplete = True
                omitted_sections.append('title_suggestions')
                incomplete_reasons.append(f'Title scan failed: {getattr(e, "message", None) or str(e)}')
                first_failed_optional_step = first_failed_optional_step or 'title_scan'
                yield _overview_progress_event('title_scan', 'error', completed)
            else:
                tokens_used += getattr(r_title_scan, 'tokens_used', 0) or 0
                models_used.append(r_title_scan.model)
                llm_rounds += 1
                candidate_keys = _extract_title_rewrite_keys(
                    r_title_scan.content or '',
                    all_keys,
                    max_keys,
                )
                title_rewrite_candidates = len(candidate_keys)
                completed.append('title_scan')
                yield _overview_progress_event('title_scan', 'done', completed)
                if candidate_keys:
                    user_message_title_rewrite = _format_issues_for_overview_prompt(
                        batch,
                        truncated,
                        total_submitted,
                        prompt_variant='title_rewrite',
                        description_keys_ordered=candidate_keys,
                    )
                    if protector:
                        user_message_title_rewrite = protector.redact_text(user_message_title_rewrite)
                    yield _overview_progress_event('title_rewrite', 'start', completed)
                    try:
                        r_title_rewrite = claude_service.send_message(
                            message=user_message_title_rewrite,
                            model=None,
                            max_tokens=Config.JIRA_BACKLOG_TITLE_REWRITE_MAX_TOKENS,
                            system_prompt=_BACKLOG_OVERVIEW_SYSTEM_TITLE_REWRITE,
                            temperature=overview_temperature,
                        )
                    except Exception as e:
                        logger.warning('backlog-overview: title_rewrite failed (partial overview): %s', e)
                        overview_incomplete = True
                        omitted_sections.append('title_suggestions')
                        incomplete_reasons.append(
                            f'Title rewrite failed: {getattr(e, "message", None) or str(e)}'
                        )
                        first_failed_optional_step = first_failed_optional_step or 'title_rewrite'
                        yield _overview_progress_event('title_rewrite', 'error', completed)
                    else:
                        tokens_used += getattr(r_title_rewrite, 'tokens_used', 0) or 0
                        models_used.append(r_title_rewrite.model)
                        llm_rounds += 1
                        title_rewrite_section, title_counts = _validate_title_rewrite_rows(
                            (r_title_rewrite.content or '').strip(),
                            source_by_key=source_by_key,
                            max_rows=max_rows,
                        )
                        title_rewrite_rows = title_counts.get('kept', 0)
                        title_rewrite_rows_dropped = title_counts.get('dropped', 0)
                        title_rewrite_pass_applied = title_rewrite_rows > 0
                        completed.append('title_rewrite')
                        yield _overview_progress_event('title_rewrite', 'done', completed)
                else:
                    title_rewrite_no_candidates = True
                    title_rewrite_section = _title_suggestions_no_candidates_markdown(max_keys)
                    completed.append('title_rewrite')
                    yield _overview_progress_event('title_rewrite', 'done', completed)

    if title_rewrite_section.strip():
        yield _overview_partial_event(
            'after_title',
            _join_overview_chunks(part2, part1, title_rewrite_section),
        )

    chunks: List[str] = []
    if part2:
        chunks.append(part2.strip())
    if part1:
        chunks.append(part1.strip())
    if title_rewrite_section:
        chunks.append(title_rewrite_section.strip())
    overview_text = '\n\n'.join(c for c in chunks if c).strip()
    logger.info(
        'backlog-overview: complete issues=%s llm_rounds=%s output_tokens≈%s incomplete=%s',
        len(batch),
        llm_rounds,
        tokens_used,
        overview_incomplete,
    )
    issues_truncated_out = max(0, total_submitted - len(batch))
    ga_blockers_in_batch = sum(1 for i in batch if i.get('gaBlocker') is True)
    sl_cov = {str(k).strip().upper() for k in scorecard_sl_keys_ordered if str(k).strip()}
    sc_cov = {str(k).strip().upper() for k in scorecard_scored_keys_ordered if str(k).strip()}
    ga_keys_in_batch = {
        str(i.get('key', '')).strip().upper()
        for i in batch
        if i.get('key') and i.get('gaBlocker') is True
    }
    ai_coverage: Dict[str, Any] = {
        'issues_received_raw': submitted_count_before_parent_filter,
        'issues_after_parent_filter': submitted_count_after_parent_filter,
        'issues_in_prompt_batch': len(batch),
        'issues_truncated_out': issues_truncated_out,
        'prompt_batch_cap': _OVERVIEW_MAX_ISSUES,
        'deep_pass_enabled': Config.JIRA_BACKLOG_OVERVIEW_DEEP_PASS_ENABLED,
        'deep_pass_max_keys': Config.JIRA_BACKLOG_OVERVIEW_DEEP_MAX_KEYS,
        'deep_pass_keys_selected': deep_key_count,
        'deep_pass_applied': deep_pass_applied,
        'title_scan_candidates': title_rewrite_candidates,
        'title_rewrite_rows': title_rewrite_rows,
        'title_rewrite_pass_applied': title_rewrite_pass_applied,
        'ga_blockers_in_batch': ga_blockers_in_batch,
        'shortlist_model_keys': len(scorecard_sl_keys_ordered) if use_scorecard else None,
        'scorecard_scored_keys': len(scorecard_scored_keys_ordered) if use_scorecard else None,
        'shortlist_cap': Config.JIRA_TRIAGE_SCORECARD_MAX_KEYS if use_scorecard else None,
        'ga_blocker_union_enabled': Config.JIRA_TRIAGE_SCORECARD_INCLUDE_GA_BLOCKERS if use_scorecard else None,
        'ga_blockers_included_in_scored_set': (len(ga_keys_in_batch & sc_cov) if use_scorecard else None),
        'scored_keys_added_by_ga_union': (max(0, len(sc_cov - sl_cov)) if use_scorecard else None),
    }
    meta: Dict[str, Any] = {
        'issue_count': len(batch),
        'truncated': truncated,
        'submitted_count': total_submitted,
        'model': models_used[-1],
        'overview_passes': llm_rounds,
        'models': models_used,
        'output_tokens': tokens_used,
        'priority_deep_pass_keys': deep_key_count,
        'priority_deep_pass_applied': deep_pass_applied,
        'priority_rows_dropped_invalid': dropped_invalid_rows,
        'priority_rows_dropped_mismatch': dropped_mismatch_rows,
        'title_rewrite_enabled': (
            Config.JIRA_BACKLOG_TITLE_REWRITE_ENABLED and not Config.JIRA_BACKLOG_TITLE_REWRITE_DISABLED
        ),
        'title_rewrite_candidates': title_rewrite_candidates,
        'title_rewrite_rows': title_rewrite_rows,
        'title_rewrite_rows_dropped': title_rewrite_rows_dropped,
        'title_rewrite_pass_applied': title_rewrite_pass_applied,
        'title_rewrite_no_candidates': title_rewrite_no_candidates,
        'completed_steps': list(completed),
        'parent_context_filter_applied': True,
        'submitted_count_before_parent_filter': submitted_count_before_parent_filter,
        'submitted_count_after_parent_filter': submitted_count_after_parent_filter,
        'snapshot_stats': snapshot_stats,
        'overview_incomplete': overview_incomplete,
        'omitted_sections': omitted_sections,
        'incomplete_reason': '; '.join(incomplete_reasons) if incomplete_reasons else None,
        'failed_step': first_failed_optional_step,
        'scorecard_enabled': use_scorecard,
        'scorecards_by_key': scorecards_by_key if use_scorecard else {},
        'scorecard_config_hash': scorecard_config_hash,
        'scorecard_schema_version': SCORECARD_SCHEMA_VERSION if use_scorecard else None,
        'scorecard_shortlist_size': scorecard_shortlist_size if use_scorecard else None,
        'scorecard_scored_keys': scorecard_scored_keys if use_scorecard else None,
        'scorecard_errors': scorecard_errors[:25] if use_scorecard else [],
        'scorecard_threshold_summary': (
            scorecard_threshold_reference_lines(min_scorecard_delta) if use_scorecard else []
        ),
        'ai_coverage': ai_coverage,
    }
    yield {
        'type': 'result',
        'status': 'success',
        'http_status': 200,
        'overview': overview_text,
        'meta': meta,
    }


@jira_bp.route('/backlog-overview', methods=['POST'])
def backlog_overview():
    """
    Generate an AI markdown overview from a client-supplied list of issues (same filtered set as the UI).
    Expects JSON: { "issues": [ { ... } ] }. Does not call Jira; uses Claude via service container.

    Flow: pass1 (themes/duplicates), pass2 (priority review from titles/metadata), optional pass2b
    (re-does ## Priority review with description excerpts for keys that appeared in the reprioritization table).
    Optional `description` per issue (truncated) enables pass2b; omit deep pass via Config / env.

    When JIRA_TRIAGE_SCORECARD_ENABLED=1: pass2 becomes JSON shortlist → JSON scorecard (schema v2,
    14-point additive rubric) → deterministic Raise/Lower from server-side Jira mapping; optional pass2b
    re-scores with description excerpts.
    See env: JIRA_TRIAGE_SCORECARD_MAX_KEYS, JIRA_TRIAGE_SCORECARD_MIN_DELTA_RANKS.
    Legacy v1 tuning vars (WEIGHTS_JSON, THRESHOLDS_JSON, MIN_CONFIDENCE) are ignored for scorecard v2.

    Query: stream=1 streams NDJSON lines (progress + terminal result). Default is a single JSON response.

    Env JIRA_BACKLOG_OVERVIEW_TEMPERATURE (0.0-1.0, default 0): Claude sampling for all overview passes.
    """
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-Type must be application/json'}), 400

    data = request.get_json(silent=True) or {}
    issues_in = data.get('issues')
    if not isinstance(issues_in, list):
        return jsonify({'status': 'error', 'message': 'Request body must include an "issues" array'}), 400

    sanitized: List[Dict[str, Any]] = []
    for item in issues_in:
        s = _sanitize_overview_issue(item)
        if s:
            sanitized.append(s)

    if not sanitized:
        return jsonify({
            'status': 'error',
            'message': 'No valid issues to analyze (each item needs at least a key).',
        }), 400

    submitted_count_before_parent_filter = len(sanitized)
    sanitized = [i for i in sanitized if _issue_has_parent_context(i)]
    submitted_count_after_parent_filter = len(sanitized)
    if not sanitized:
        return jsonify({
            'status': 'error',
            'message': 'No parent/epic-linked issues to analyze after parent-context filter.',
        }), 400

    total_submitted = len(sanitized)
    truncated = total_submitted > _OVERVIEW_MAX_ISSUES
    batch = sanitized[:_OVERVIEW_MAX_ISSUES]

    use_scorecard = Config.JIRA_TRIAGE_SCORECARD_ENABLED
    user_message_pass1 = _format_issues_for_overview_prompt(
        batch, truncated, total_submitted, prompt_variant='pass1'
    )
    user_message_pass2 = (
        ''
        if use_scorecard
        else _format_issues_for_overview_prompt(
            batch, truncated, total_submitted, prompt_variant='pass2'
        )
    )

    pii_config = Config.get_pii_config()
    protector = create_pii_protector(pii_config) if pii_config.get('redact_mode') else None
    if protector:
        user_message_pass1 = protector.redact_text(user_message_pass1)
        if user_message_pass2:
            user_message_pass2 = protector.redact_text(user_message_pass2)

    service_container = getattr(g, 'service_container', None)
    if not service_container:
        logger.error('Service container missing for backlog overview')
        return jsonify({
            'status': 'error',
            'message': 'Server misconfiguration: service container unavailable',
        }), 500

    claude_service = service_container.get_claude_service()
    if claude_service is None:
        return jsonify({
            'status': 'error',
            'message': 'Claude API is not configured (set ANTHROPIC_API_KEY).',
        }), 503

    use_stream = (request.args.get('stream') or '').strip().lower() in ('1', 'true', 'yes')

    def run_events():
        return _iter_backlog_overview_events(
            claude_service,
            batch,
            truncated,
            total_submitted,
            user_message_pass1,
            user_message_pass2,
            protector,
            submitted_count_before_parent_filter,
            submitted_count_after_parent_filter,
            use_scorecard=use_scorecard,
        )

    if use_stream:
        def ndjson_gen():
            try:
                for ev in run_events():
                    yield json.dumps(ev, default=str) + '\n'
            except Exception as e:
                logger.exception('backlog-overview stream failed: %s', e)
                err = _overview_error_result(e, failed_step='unknown', completed_steps=[])
                yield json.dumps(err, default=str) + '\n'

        return Response(
            stream_with_context(ndjson_gen()),
            mimetype='application/x-ndjson',
        )

    last_result: Optional[Dict[str, Any]] = None
    try:
        for ev in run_events():
            if ev.get('type') == 'result':
                last_result = ev
    except Exception as e:
        logger.exception('Backlog overview pipeline failed: %s', e)
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to generate backlog overview',
            'error_code': 'BACKLOG_OVERVIEW_ERROR',
            'failed_step': 'unknown',
            'completed_steps': [],
            'details': {},
        }), 500

    if not last_result:
        return jsonify({'status': 'error', 'message': 'No result from overview pipeline'}), 500

    if last_result.get('status') == 'error':
        http = int(last_result.get('http_status') or 500)
        return jsonify({
            'status': 'error',
            'message': last_result.get('message') or 'Failed to generate backlog overview',
            'error_code': last_result.get('error_code'),
            'failed_step': last_result.get('failed_step'),
            'completed_steps': last_result.get('completed_steps') or [],
            'details': last_result.get('details') or {},
            'retry_after_seconds': last_result.get('retry_after_seconds'),
        }), http

    return jsonify({
        'status': 'success',
        'overview': last_result.get('overview') or '',
        'meta': last_result.get('meta') or {},
    }), 200
