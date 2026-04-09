"""
Unit tests for deterministic Jira reprioritization row validation.
"""

from backend.api.routes.jira_routes import _validate_reprioritization_rows


def _mk_markdown(rows: str) -> str:
    return "\n".join(
        [
            "### Recommended Jira priority changes",
            "",
            "| Ticket | Title | Current priority | Jira priority recommendation | Reason |",
            "|---|---|---|---|---|",
            rows.strip(),
            "",
        ]
    )


def test_drops_blocker_raise_to_blocker():
    md = _mk_markdown("| HALO-1 | t | Blocker | Raise to Blocker | x |")
    cleaned, dropped = _validate_reprioritization_rows(md, {"HALO-1": "blocker"})
    assert "HALO-1" not in cleaned
    assert dropped["invalid"] == 1
    assert dropped["mismatch"] == 0


def test_drops_blocker_raise_to_critical():
    md = _mk_markdown("| HALO-2 | t | Blocker | Raise to Critical | x |")
    cleaned, dropped = _validate_reprioritization_rows(md, {"HALO-2": "blocker"})
    assert "HALO-2" not in cleaned
    assert dropped["invalid"] == 1


def test_keeps_critical_raise_to_blocker():
    md = _mk_markdown("| HALO-3 | t | Critical | Raise to Blocker | x |")
    cleaned, dropped = _validate_reprioritization_rows(md, {"HALO-3": "critical"})
    assert "HALO-3" in cleaned
    assert dropped["invalid"] == 0
    assert dropped["mismatch"] == 0


def test_keeps_major_lower_to_normal():
    md = _mk_markdown("| HALO-4 | t | Major | Lower to Normal | x |")
    cleaned, dropped = _validate_reprioritization_rows(md, {"HALO-4": "major"})
    assert "HALO-4" in cleaned
    assert dropped["invalid"] == 0
    assert dropped["mismatch"] == 0


def test_drops_raise_to_same_level():
    md = _mk_markdown("| HALO-5 | t | Major | Raise to Major | x |")
    cleaned, dropped = _validate_reprioritization_rows(md, {"HALO-5": "major"})
    assert "HALO-5" not in cleaned
    assert dropped["invalid"] == 1


def test_drops_current_priority_mismatch_against_source():
    md = _mk_markdown("| HALO-6 | t | Critical | Raise to Blocker | x |")
    cleaned, dropped = _validate_reprioritization_rows(md, {"HALO-6": "major"})
    assert "HALO-6" not in cleaned
    assert dropped["invalid"] == 0
    assert dropped["mismatch"] == 1

