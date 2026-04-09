"""Unit tests for Jira triage scorecard parsing and deterministic merge."""

from backend.api.routes.jira_routes import _validate_reprioritization_rows
from backend.services.jira_triage_scorecard import (
    ScorecardBreakpoints,
    ScorecardWeights,
    build_scorecards_by_key_meta,
    composite_score,
    implied_priority_from_score,
    merge_scorecard_to_recommendation,
    parse_scorecard_json,
    parse_shortlist_keys_json,
    recommendations_to_reprioritization_markdown,
)


def test_composite_score_range():
    from backend.services.jira_triage_scorecard import ScorecardRowIn

    row = ScorecardRowIn(
        key="H-1",
        severity=5,
        frequency=5,
        customer_impact=5,
        scope=5,
        release_risk=5,
        confidence=5,
    )
    w = ScorecardWeights()
    s = composite_score(row, w)
    assert 99.0 <= s <= 100.0


def test_implied_priority_from_breakpoints():
    b = ScorecardBreakpoints()
    assert implied_priority_from_score(90, b) == "blocker"
    assert implied_priority_from_score(50, b) == "normal"


def test_merge_recommendation_raise_when_delta_ok():
    from backend.services.jira_triage_scorecard import ScorecardRowIn

    row = ScorecardRowIn(
        key="H-1",
        severity=5,
        frequency=5,
        customer_impact=5,
        scope=5,
        release_risk=5,
        confidence=5,
    )
    w = ScorecardWeights()
    b = ScorecardBreakpoints()
    rec = merge_scorecard_to_recommendation(row, "Normal", w, b, min_confidence=2, min_delta_ranks=1)
    assert rec is not None
    assert rec["action"] == "raise"
    assert rec["target"] == "blocker"


def test_merge_suppressed_low_confidence():
    from backend.services.jira_triage_scorecard import ScorecardRowIn

    row = ScorecardRowIn(
        key="H-1",
        severity=5,
        frequency=5,
        customer_impact=5,
        scope=5,
        release_risk=5,
        confidence=1,
    )
    w = ScorecardWeights()
    b = ScorecardBreakpoints()
    rec = merge_scorecard_to_recommendation(row, "Normal", w, b, min_confidence=2, min_delta_ranks=1)
    assert rec is None


def test_parse_scorecard_json_with_fence():
    raw = """```json
{"version":"1","rows":[{"key":"HALO-1","severity":5,"frequency":3,"customer_impact":4,"scope":2,"release_risk":3,"confidence":4}]}
```"""
    batch, errs = parse_scorecard_json(raw)
    assert not errs
    assert batch is not None
    assert len(batch.rows) == 1
    assert batch.rows[0].key == "HALO-1"


def test_recommendations_markdown_and_validator():
    from backend.services.jira_triage_scorecard import ScorecardBatchIn, ScorecardRowIn

    rows = ScorecardRowIn(
        key="HALO-9",
        severity=5,
        frequency=5,
        customer_impact=5,
        scope=5,
        release_risk=5,
        confidence=5,
    )
    batch = ScorecardBatchIn(rows=[rows])
    src = {"HALO-9": {"priority": "Normal", "title": "Test bug", "description": ""}}
    md = recommendations_to_reprioritization_markdown(
        batch,
        src,
        ScorecardWeights(),
        ScorecardBreakpoints(),
        min_confidence=2,
        min_delta_ranks=1,
    )
    pri = {"HALO-9": "normal"}
    cleaned, dropped = _validate_reprioritization_rows(md, source_priorities=pri)
    assert dropped["invalid"] == 0
    assert "HALO-9" in cleaned
    assert "Raise" in cleaned


def test_parse_shortlist_keys_json():
    raw = '{"keys":["HALO-2","HALO-1","UNKNOWN"]}'
    keys, errs = parse_shortlist_keys_json(raw, {"HALO-1", "HALO-2"}, max_keys=10)
    assert keys == ["HALO-2", "HALO-1"]


def test_build_scorecards_by_key_meta_includes_recommendation():
    from backend.services.jira_triage_scorecard import ScorecardBatchIn, ScorecardRowIn

    batch = ScorecardBatchIn(
        rows=[
            ScorecardRowIn(
                key="X-1",
                severity=2,
                frequency=2,
                customer_impact=2,
                scope=2,
                release_risk=2,
                confidence=4,
            ),
        ]
    )
    src = {"X-1": {"priority": "Major", "title": "t", "description": ""}}
    meta = build_scorecards_by_key_meta(
        batch,
        src,
        ScorecardWeights(),
        ScorecardBreakpoints(),
        min_confidence=2,
        min_delta_ranks=1,
    )
    assert "X-1" in meta
    assert meta["X-1"]["computed_score"] >= 0
    # Low composite vs Major may or may not produce Lower — either way structure is present
    assert "recommendation" in meta["X-1"]
