"""
Unit tests for title clarity suggestion parsing/validation helpers.
"""

from backend.api.routes.jira_routes import (
    _extract_title_rewrite_keys,
    _validate_title_rewrite_rows,
)


def _mk_title_markdown(rows: str) -> str:
    return "\n".join(
        [
            "### Title clarity suggestions",
            "| Ticket | Current priority | Current title | Proposed title |",
            "|---|---|---|---|",
            rows.strip(),
        ]
    )


def test_extract_title_rewrite_keys_preserves_valid_order_and_max():
    text = '{"keys":["HALO-2","HALO-99","HALO-1","HALO-2"]}'
    got = _extract_title_rewrite_keys(text, ["HALO-1", "HALO-2", "HALO-3"], 2)
    assert got == ["HALO-2", "HALO-1"]


def test_validate_title_rewrite_rows_keeps_valid_row():
    md = _mk_title_markdown(
        "| HALO-10 | Major | App crashes when opening map after walk | Crash when opening map after walk summary loads |"
    )
    source = {
        "HALO-10": {
            "priority": "Major",
            "title": "App crashes when opening map after walk",
        }
    }
    cleaned, counts = _validate_title_rewrite_rows(md, source, max_rows=5)
    assert "HALO-10" in cleaned
    assert counts["kept"] == 1
    assert counts["dropped"] == 0


def test_validate_title_rewrite_rows_drops_priority_mismatch():
    md = _mk_title_markdown(
        "| HALO-11 | Critical | Existing title text | Better title text with specifics |"
    )
    source = {"HALO-11": {"priority": "Major", "title": "Existing title text"}}
    cleaned, counts = _validate_title_rewrite_rows(md, source, max_rows=5)
    assert cleaned == ""
    assert counts["kept"] == 0
    assert counts["dropped"] == 1


def test_validate_title_rewrite_rows_drops_proposed_same_as_current():
    md = _mk_title_markdown(
        "| HALO-12 | Minor | Sync spinner never ends | Sync spinner never ends |"
    )
    source = {"HALO-12": {"priority": "Minor", "title": "Sync spinner never ends"}}
    cleaned, counts = _validate_title_rewrite_rows(md, source, max_rows=5)
    assert cleaned == ""
    assert counts["kept"] == 0
    assert counts["dropped"] == 1
