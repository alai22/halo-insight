"""
Convert common Markdown to Slack mrkdwn for Slack bot replies.

Shared by Operations and Product bots. Slack does not render `#` headers or
`**bold**`. It uses: *bold*   _italic_   ~strike~   `code`   ```pre```
"""

from __future__ import annotations

import re

_HEADER_RE = re.compile(r'^\s{0,3}#{1,6}\s+(.*\S)\s*$', re.MULTILINE)
_BOLD_RE = re.compile(r'\*\*(.+?)\*\*')
_BOLD_UNDERSCORE_RE = re.compile(r'__(.+?)__')
_QUAD_STAR_RE = re.compile(r'\*{4,}')


def to_slack_mrkdwn(text: str) -> str:
    """
    Best-effort CommonMark → Slack mrkdwn.

    Safe to run on already-Slack-formatted text in most cases:
    headers become bold; **bold** becomes *bold*.
    """
    if not text:
        return text

    def _header_sub(match: re.Match) -> str:
        title = match.group(1).strip()
        title = re.sub(r'\s+#+\s*$', '', title).strip()
        title = _BOLD_RE.sub(r'\1', title)
        title = _BOLD_UNDERSCORE_RE.sub(r'\1', title)
        return f'*{title}*'

    out = _HEADER_RE.sub(_header_sub, text)
    out = _BOLD_RE.sub(r'*\1*', out)
    out = _BOLD_UNDERSCORE_RE.sub(r'*\1*', out)
    out = _QUAD_STAR_RE.sub('*', out)
    return out.strip()
