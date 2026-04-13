"""Unit tests for Jira triage scorecard v2 parsing and deterministic merge."""

from backend.api.routes.jira_routes import _validate_reprioritization_rows
from backend.services.jira_triage_scorecard import (
    ScorecardBatchIn,
    ScorecardRowIn,
    build_scorecards_by_key_meta,
    ga_verdict_from_total,
    implied_jira_priority_from_row,
    merge_scorecard_to_recommendation,
    parse_scorecard_json,
    parse_shortlist_keys_json,
    raw_total_from_row,
    recommendations_to_reprioritization_markdown,
    scorecard_framework_config_hash,
)


def _row(**kwargs):
    defaults = dict(
        key="H-1",
        feature_importance=2,
        reach=2,
        technical_severity=2,
        workaround_quality=1,
        regression_risk=0,
        raw_total=7,
        ga_verdict="Fix if capacity",
        jira_priority="Major",
    )
    defaults.update(kwargs)
    return ScorecardRowIn(**defaults)


def test_raw_total_and_ga_verdict():
    r = _row(feature_importance=2, reach=1, technical_severity=1, workaround_quality=0, regression_risk=1)
    assert raw_total_from_row(r) == 5
    assert ga_verdict_from_total(5) == "PostGA"
    assert ga_verdict_from_total(6) == "Fix if capacity"
    assert ga_verdict_from_total(10) == "Block GA"


def test_implied_jira_priority_bands():
    assert implied_jira_priority_from_row(_row(feature_importance=1, reach=1, technical_severity=1, workaround_quality=0, regression_risk=0)) == "minor"  # 3
    assert implied_jira_priority_from_row(_row(feature_importance=1, reach=1, technical_severity=1, workaround_quality=1, regression_risk=1)) == "normal"  # 5
    assert implied_jira_priority_from_row(_row(feature_importance=2, reach=1, technical_severity=1, workaround_quality=1, regression_risk=1)) == "major"  # 6
    r6 = _row(feature_importance=2, reach=1, technical_severity=2, workaround_quality=1, regression_risk=0)
    assert raw_total_from_row(r6) == 6
    assert implied_jira_priority_from_row(r6) == "major"
    assert implied_jira_priority_from_row(_row(feature_importance=2, reach=2, technical_severity=2, workaround_quality=1, regression_risk=0)) == "major"  # 7
    assert implied_jira_priority_from_row(_row(feature_importance=2, reach=2, technical_severity=2, workaround_quality=1, regression_risk=1)) == "critical"  # 8
    assert implied_jira_priority_from_row(_row(feature_importance=2, reach=2, technical_severity=3, workaround_quality=1, regression_risk=1)) == "critical"  # 9
    assert implied_jira_priority_from_row(_row(feature_importance=2, reach=3, technical_severity=3, workaround_quality=2, regression_risk=0)) == "blocker"  # 10


def test_implied_blocker_safety_override_low_total():
    r = _row(
        key="HALO-X",
        feature_importance=4,
        reach=0,
        technical_severity=2,
        workaround_quality=0,
        regression_risk=0,
        raw_total=6,
        ga_verdict="Fix if capacity",
        jira_priority="Blocker",
    )
    assert raw_total_from_row(r) == 6
    assert implied_jira_priority_from_row(r) == "blocker"
    assert ga_verdict_from_total(6) == "Fix if capacity"


def test_implied_blocker_workaround_quality():
    r = ScorecardRowIn(
        key="HALO-Y",
        feature_importance=4,
        reach=0,
        technical_severity=0,
        workaround_quality=1,
        regression_risk=0,
        raw_total=5,
        ga_verdict="PostGA",
        jira_priority="Blocker",
    )
    assert raw_total_from_row(r) == 5
    assert implied_jira_priority_from_row(r) == "blocker"


def test_merge_no_confidence_gate_always_considered():
    r = ScorecardRowIn(
        key="H-1",
        feature_importance=4,
        reach=3,
        technical_severity=3,
        workaround_quality=2,
        regression_risk=2,
        raw_total=14,
        ga_verdict="Block GA",
        jira_priority="Blocker",
    )
    rec = merge_scorecard_to_recommendation(r, "Normal", min_delta_ranks=1)
    assert rec is not None
    assert rec["action"] == "raise"
    assert rec["target"] == "blocker"


def test_parse_scorecard_json_v2_with_fence():
    raw = """```json
{"version":"2","rows":[{"key":"HALO-1","feature_importance":3,"reach":2,"technical_severity":2,"workaround_quality":1,"regression_risk":0,"raw_total":8,"ga_verdict":"Fix if capacity","jira_priority":"Critical"}]}
```"""
    batch, errs = parse_scorecard_json(raw)
    assert not errs
    assert batch is not None
    assert len(batch.rows) == 1
    assert batch.rows[0].key == "HALO-1"
    assert raw_total_from_row(batch.rows[0]) == 8


def test_parse_rejects_v1_version():
    raw = '{"version":"1","rows":[{"key":"HALO-1","feature_importance":3}]}'
    batch, errs = parse_scorecard_json(raw)
    assert batch is None
    assert errs


def test_recommendations_markdown_and_validator():
    rows = ScorecardRowIn(
        key="HALO-9",
        feature_importance=3,
        reach=3,
        technical_severity=3,
        workaround_quality=2,
        regression_risk=2,
        raw_total=13,
        ga_verdict="Block GA",
        jira_priority="Blocker",
    )
    batch = ScorecardBatchIn(rows=[rows])
    src = {"HALO-9": {"priority": "Normal", "title": "Test bug", "description": ""}}
    md = recommendations_to_reprioritization_markdown(
        batch,
        src,
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


def test_build_scorecards_by_key_meta():
    batch = ScorecardBatchIn(
        rows=[
            ScorecardRowIn(
                key="X-1",
                feature_importance=1,
                reach=1,
                technical_severity=1,
                workaround_quality=0,
                regression_risk=0,
                raw_total=3,
                ga_verdict="PostGA",
                jira_priority="Minor",
            ),
        ]
    )
    src = {"X-1": {"priority": "Major", "title": "t", "description": ""}}
    meta = build_scorecards_by_key_meta(
        batch,
        src,
        min_delta_ranks=1,
    )
    assert "X-1" in meta
    assert meta["X-1"]["raw_total"] == 3
    assert meta["X-1"]["ga_verdict"] == "PostGA"
    assert meta["X-1"]["implied_priority"] == "minor"
    assert "recommendation" in meta["X-1"]


def test_framework_config_hash_stable():
    assert scorecard_framework_config_hash() == scorecard_framework_config_hash()
    assert len(scorecard_framework_config_hash()) == 16
