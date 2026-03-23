"""
Jira API Routes for Bug Triage Copilot

Provides issue list, status, OAuth 2.0 (3LO) connect flow, and AI backlog overview.
"""

import logging
import re
import secrets
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

from flask import Blueprint, g, jsonify, redirect, request, session
import requests

from backend.services.jira_client import JiraClient
from backend.services import jira_oauth
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

# Post-process model output: drop reprioritization rows that say "raise" to Blocker when current is already Blocker.
_RE_MD_TABLE_ROW = re.compile(r'^\s*\|(.+)\|\s*$')
_RE_RAISE = re.compile(r'raise', re.IGNORECASE)
_RE_BLOCKER = re.compile(r'\bblocker\b', re.IGNORECASE)
_RE_HEADER_SEP = re.compile(r'^[\s\-:|]+$')
_RE_TICKET_KEY_CELL = re.compile(r'^[A-Za-z][A-Za-z0-9]{1,19}-\d+$')


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


def _strip_invalid_raise_to_blocker_rows(markdown: str) -> str:
    """
    Remove reprioritization table rows where Current is already Blocker but
    the model still emitted a Raise…Blocker recommendation (recurring LLM mistake).
    Supports 4-column (legacy) or 5-column (Ticket, Title, …) tables.
    Only applies between ### Recommended Jira priority changes and the next ## section.
    """
    if not markdown or 'Recommended Jira priority changes' not in markdown:
        return markdown

    lines = markdown.split('\n')
    out: List[str] = []
    in_repr = False
    dropped = 0

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
        cur_rec = _repr_row_current_and_recommendation(cells) if cells else None
        if (
            cur_rec
            and not cells[0].lower().startswith('ticket')
            and not _RE_HEADER_SEP.match(cells[0])
            and _current_priority_is_blocker(cur_rec[0])
            and _recommendation_is_raise_to_blocker(cur_rec[1])
        ):
            dropped += 1
            logger.info(
                'backlog-overview: dropped invalid Raise-to-Blocker row for ticket %s',
                cells[0][:32],
            )
            continue
        out.append(line)

    if dropped:
        logger.info('backlog-overview: dropped %s invalid Blocker→Raise rows', dropped)
    return '\n'.join(out)


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
        if _repr_row_current_and_recommendation(cells) is None:
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


# Pass 1: themes, clarification, duplicates—no Priority review (that is pass 2 for output budget).
# max_tokens per pass come from Config (default 4096; >4096 often 400 Bad Request on Haiku).

_BACKLOG_OVERVIEW_SYSTEM_PASS1 = """You are an engineering lead helping triage a Jira bug backlog for **Halo Collar** (pet GPS / smart collar; mobile apps for pet tracking, maps, geofences, device pairing, etc.). You receive issues as **TAB-separated** lines (see user message header row for column order—**priority** is the 4th column).

**Important:** Do **not** output a `## Priority review` section. Priority review is generated in a separate step; including it here is **forbidden**.

Write a markdown overview for the team. Use these sections only (omit a section if nothing substantive to say). **When multiple sections apply, keep this `##` order** so the recap reads top-down: **themes and unclear tickets before duplicate clusters** (this block is shown **after** `## Priority review` in the UI, which covers Jira priority recommendations first).

## Critical / high-risk themes
(Themes and risk—**not** the Jira priority name "Critical".)
## Needs clarification
Tickets that look vague, blocked, or missing context based on titles/metadata.
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
    + """**Output:** Produce **only** the markdown subsection starting with `### Recommended Jira priority changes` (see Format below). Do **not** output `## Priority review`—the application prepends backlog statistics. Do **not** output an aggregate “count by priority” table; a snapshot is injected for you. No preamble, no other `##` sections, no themes or duplicates here.

Assess **every** issue in the table for Jira priority vs title/metadata. **Only tabulate** tickets where you recommend changing the Jira priority field in the reprioritization table.

**Coverage (mandatory):** Pay deliberate attention to **Major**, **Normal**, and **Minor** tickets—not only Blocker/Critical. Many mis-prioritizations appear as severe user impact in the title while priority is still Normal or Major. Scan those tiers before concluding.

**Row targets (when justified—do not invent recommendations):** If the issue count is **≥100**, aim for **at least 8** rows in `### Recommended Jira priority changes` when that many **distinct, justified** Raise/Lower recommendations exist. If the issue count is **≥300**, aim for **at least 15** such rows when that many exist. If fewer are genuinely justified, say so in one sentence under that subheading (do not pad with weak rows).

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

| Ticket | Title | Current priority | Jira priority recommendation | Reason |

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
) -> str:
    """Build user message text for Claude (pass1 / pass2 / pass2b with optional description excerpts)."""
    if prompt_variant == 'pass2b':
        lines = [
            f"The following {len(issues)} issues: first block is metadata for **every** issue (tab-separated). "
            f"After a line that is only `---`, **description_excerpts** rows apply **only** to those keys—use them for Raise/Lower per system prompt.",
        ]
    else:
        lines = [
            f"The following {len(issues)} issues are the current filtered backlog (metadata only).",
        ]
    if truncated:
        lines.append(f"Note: Analyzing first {len(issues)} of {total_submitted} issues submitted (cap for context size).")
    lines.append('')
    if prompt_variant == 'pass1':
        lines.append(
            'Your task for this message: themes, needs clarification, duplicates/clusters, and other notes only. '
            'Do **not** output ## Priority review or Jira priority recommendations.'
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
    for i in issues:
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
        by_key_upper = {
            str(i.get('key', '')).strip().upper(): i
            for i in issues
            if i.get('key')
        }
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
    elif prompt_variant == 'pass2b':
        lines.append(
            'Produce **only** the `### Recommended Jira priority changes` fragment as instructed (second pass / description excerpts).'
        )
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
        client = JiraClient()
        issues = client.fetch_issues_for_triage(
            project=project,
            max_results=max_results,
            ancestor_key=ancestor_key,
            issuetype=issuetype,  # default from param is Bug; None means all types (e.g. ?issuetype=all)
        )
        return jsonify({
            'status': 'success',
            'data': issues,
            'count': len(issues),
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


@jira_bp.route('/backlog-overview', methods=['POST'])
def backlog_overview():
    """
    Generate an AI markdown overview from a client-supplied list of issues (same filtered set as the UI).
    Expects JSON: { "issues": [ { ... } ] }. Does not call Jira; uses Claude via service container.

    Flow: pass1 (themes/duplicates), pass2 (priority review from titles/metadata), optional pass2b
    (re-does ## Priority review with description excerpts for keys that appeared in the reprioritization table).
    Optional `description` per issue (truncated) enables pass2b; omit deep pass via Config / env.
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

    total_submitted = len(sanitized)
    truncated = total_submitted > _OVERVIEW_MAX_ISSUES
    batch = sanitized[:_OVERVIEW_MAX_ISSUES]

    user_message_pass1 = _format_issues_for_overview_prompt(
        batch, truncated, total_submitted, prompt_variant='pass1'
    )
    user_message_pass2 = _format_issues_for_overview_prompt(
        batch, truncated, total_submitted, prompt_variant='pass2'
    )

    pii_config = Config.get_pii_config()
    protector = create_pii_protector(pii_config) if pii_config.get('redact_mode') else None
    if protector:
        user_message_pass1 = protector.redact_text(user_message_pass1)
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

    try:
        r1 = claude_service.send_message(
            message=user_message_pass1,
            model=None,
            max_tokens=Config.JIRA_BACKLOG_OVERVIEW_PASS1_MAX_TOKENS,
            system_prompt=_BACKLOG_OVERVIEW_SYSTEM_PASS1,
        )
        r2 = claude_service.send_message(
            message=user_message_pass2,
            model=None,
            max_tokens=Config.JIRA_BACKLOG_OVERVIEW_PASS2_MAX_TOKENS,
            system_prompt=_BACKLOG_OVERVIEW_SYSTEM_PASS2,
        )
        part1 = (r1.content or '').strip()
        part2_draft = _strip_invalid_raise_to_blocker_rows((r2.content or '').strip())
        tokens_used = (getattr(r1, 'tokens_used', 0) or 0) + (getattr(r2, 'tokens_used', 0) or 0)
        models_used: List[str] = [r1.model, r2.model]
        llm_rounds = 2
        part2 = _assemble_priority_review_with_snapshot(batch, part2_draft)
        snapshot_stats = _compute_backlog_snapshot_stats(batch)
        deep_key_count = 0
        deep_pass_applied = False

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
                user_message_pass2b = _format_issues_for_overview_prompt(
                    batch,
                    truncated,
                    total_submitted,
                    prompt_variant='pass2b',
                    description_keys_ordered=deep_keys,
                )
                if protector:
                    user_message_pass2b = protector.redact_text(user_message_pass2b)
                r2b = claude_service.send_message(
                    message=user_message_pass2b,
                    model=None,
                    max_tokens=Config.JIRA_BACKLOG_OVERVIEW_PASS2B_MAX_TOKENS,
                    system_prompt=_BACKLOG_OVERVIEW_SYSTEM_PASS2B,
                )
                part2b_out = _strip_invalid_raise_to_blocker_rows((r2b.content or '').strip())
                tokens_used += getattr(r2b, 'tokens_used', 0) or 0
                models_used.append(r2b.model)
                llm_rounds = 3
                pass2b_ok = bool(part2b_out.strip()) and (
                    '### Recommended Jira priority changes' in part2b_out
                )
                if pass2b_ok:
                    part2 = _assemble_priority_review_with_snapshot(batch, part2b_out)
                    deep_pass_applied = True
                    logger.info(
                        'backlog-overview: pass2b description refine issues=%s keys=%s',
                        len(batch),
                        deep_key_count,
                    )
                else:
                    logger.warning(
                        'backlog-overview: pass2b missing valid ### Recommended Jira priority changes; keeping pass2 output keys=%s',
                        deep_key_count,
                    )

        # Priority review first in the recap (actionable Jira changes), then themes / clarification / duplicates.
        overview_text = f'{part2}\n\n{part1}'.strip() if part2 else part1
        logger.info(
            'backlog-overview: complete issues=%s llm_rounds=%s output_tokens≈%s',
            len(batch),
            llm_rounds,
            tokens_used,
        )
        return jsonify({
            'status': 'success',
            'overview': overview_text,
            'meta': {
                'issue_count': len(batch),
                'truncated': truncated,
                'submitted_count': total_submitted,
                'model': models_used[-1],
                'overview_passes': llm_rounds,
                'models': models_used,
                'output_tokens': tokens_used,
                'priority_deep_pass_keys': deep_key_count,
                'priority_deep_pass_applied': deep_pass_applied,
                'snapshot_stats': snapshot_stats,
            },
        })
    except Exception as e:
        logger.exception('Backlog overview Claude call failed: %s', e)
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to generate backlog overview',
        }), 500
