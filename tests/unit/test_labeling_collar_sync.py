"""Clone snapshot and session-to-dump join counts. No Azure or S3."""

from datetime import datetime

from backend.services.labeling_collar_sync_service import (
    CollarAiFile,
    build_clone_snapshot,
    classify_blob_presence,
    match_coverage,
)


def _file(sn, family, when, size=10):
    return CollarAiFile(
        key=f"collar-raw/{sn}/ai/{family}.log",
        collar_sn=sn,
        filename=f"{family}.log",
        family=family,
        timestamp=when.strftime("%Y-%m-%dT%H:%M:%S"),
        when=when,
        size=size,
    )


def test_classify_blob_presence():
    assert classify_blob_presence(None, 10) == "copied"
    assert classify_blob_presence(10, 10) == "skipped"
    assert classify_blob_presence(9, 10) == "copied"


def test_match_coverage_splits_missing_reasons_by_sn():
    present = datetime(2026, 4, 21, 18, 38, 31)
    files = [_file("sn1", "activity", present)]
    sessions = [
        {
            "user": "a@x.com",
            "collar_sn": "sn1",
            "family": "activity",
            "timestamp": "2026-04-21T18:38:31",
            "duration_seconds": 10,
        },
        {
            "user": "a@x.com",
            "collar_sn": "sn1",
            "family": "activity",
            "timestamp": "2026-04-21T12:00:00",
            "duration_seconds": 5,
        },
        {
            "user": "a@x.com",
            "collar_sn": "_unknown",
            "family": "activity",
            "timestamp": "2026-04-21T18:38:31",
            "duration_seconds": 3,
        },
        {
            "user": "b@x.com",
            "collar_sn": "sn2",
            "family": "gps",
            "timestamp": "2026-04-21T18:38:31",
            "duration_seconds": 4,
        },
    ]
    coverage = match_coverage(sessions, files, pad_sec=60)
    assert coverage["totals"]["matched"] == 1
    assert coverage["totals"]["missing"] == 3
    assert coverage["missing_reasons"] == {
        "no_blobs_for_sn": 1,
        "time_gap": 1,
        "unknown_sn": 1,
        "bad_timestamp": 0,
    }
    by_sn = {row["collar_sn"]: row for row in coverage["by_sn"]}
    assert by_sn["sn1"]["sessions"] == 2
    assert by_sn["sn1"]["matched"] == 1
    assert by_sn["sn1"]["time_gap"] == 1
    assert by_sn["sn1"]["s3_files"] == 1
    assert by_sn["sn2"]["no_blobs_for_sn"] == 1
    assert by_sn["sn2"]["s3_files"] == 0
    assert by_sn["_unknown"]["unknown_sn"] == 1
    assert by_sn["_unknown"]["sessions"] == 1


def test_match_coverage_by_date_splits_matched_app_only_and_collar_only():
    files = [
        _file("sn1", "activity", datetime(2026, 4, 21, 18, 38, 31)),
        _file("sn1", "activity", datetime(2026, 4, 22, 9, 0, 0)),
    ]
    sessions = [
        {
            "user": "a@x.com",
            "collar_sn": "sn1",
            "family": "activity",
            "timestamp": "2026-04-21T18:38:31",
            "duration_seconds": 10,
        },
        {
            "user": "a@x.com",
            "collar_sn": "sn1",
            "family": "activity",
            "timestamp": "2026-04-21T12:00:00",
            "duration_seconds": 5,
        },
        {
            "user": "a@x.com",
            "collar_sn": "_unknown",
            "family": "activity",
            "timestamp": "2026-04-20T08:00:00",
            "duration_seconds": 3,
        },
        {
            "user": "a@x.com",
            "collar_sn": "sn1",
            "family": "activity",
            "timestamp": "not a time",
            "duration_seconds": 3,
        },
    ]
    coverage = match_coverage(sessions, files, pad_sec=60)
    assert coverage["by_date"] == [
        {"date": "2026-04-20", "matched": 0, "app_only": 1, "collar_only": 0},
        {"date": "2026-04-21", "matched": 1, "app_only": 1, "collar_only": 0},
        {"date": "2026-04-22", "matched": 0, "app_only": 0, "collar_only": 1},
    ]
    by_reason = {row["reason"]: row for row in coverage["mismatched_sessions"]}
    assert set(by_reason) == {"time_gap", "unknown_sn", "bad_timestamp"}
    # 12:00 session; closest sn1 log is 18:38:31 the same day.
    assert by_reason["time_gap"]["nearest_log_delta_sec"] == 6 * 3600 + 38 * 60 + 31
    assert by_reason["time_gap"]["email"] == "a@x.com"
    assert "nearest_log_delta_sec" not in by_reason["unknown_sn"]
    [log] = coverage["collar_only_logs"]
    assert log["timestamp"] == "2026-04-22T09:00:00"
    assert log["labelers"] == ["a@x.com"]
    # Closest session is 2026-04-21T18:38:31, so the log is 14h21m29s later.
    assert log["nearest_session_delta_sec"] == 14 * 3600 + 21 * 60 + 29
    used, unused = coverage["collar_files"]
    assert used["timestamp"] == "2026-04-21T18:38:31"
    assert used["sessions"] == [
        {"email": "a@x.com", "timestamp": "2026-04-21T18:38:31", "family": "activity"}
    ]
    assert unused["sessions"] == []


def test_clone_snapshot_not_cloned_depends_on_check_vs_copy():
    rows = [
        {
            "collar_sn": "sn1",
            "azure_files": 3,
            "s3_files": 1,
            "copied": 2,
            "skipped": 1,
            "errors": 0,
        },
        {
            "collar_sn": "sn2",
            "azure_files": 1,
            "s3_files": 0,
            "copied": 0,
            "skipped": 0,
            "errors": 1,
        },
    ]
    checked = build_clone_snapshot(
        rows, inventory_only=True, generated_at="2026-04-21T00:00:00Z"
    )
    assert checked["generated_at"] == "2026-04-21T00:00:00Z"
    assert checked["inventory_only"] is True
    assert checked["azure_files"] == 4
    assert checked["s3_files"] == 1
    assert checked["copied"] == 2
    assert checked["skipped_unchanged"] == 1
    assert checked["errors"] == 1
    assert checked["not_cloned"] == 3
    assert [row["collar_sn"] for row in checked["by_sn"]] == ["sn1", "sn2"]
    assert checked["by_sn"][0]["skipped"] == 1

    copied = build_clone_snapshot(
        rows, inventory_only=False, generated_at="2026-04-21T00:00:00Z"
    )
    assert copied["inventory_only"] is False
    assert copied["not_cloned"] == 1


def test_match_coverage_window_counts_only_files_inside_it():
    files = [
        _file("sn1", "activity", datetime(2026, 4, 21, 23, 59, 0)),
        _file("sn1", "activity", datetime(2026, 4, 22, 0, 1, 0)),
    ]
    sessions = [
        {
            "user": "a@x.com",
            "collar_sn": "sn1",
            "family": "activity",
            "timestamp": "2026-04-22T00:00:00",
            "duration_seconds": 10,
        }
    ]
    coverage = match_coverage(sessions, files, pad_sec=120, window=("2026-04-22", "2026-04-30"))
    # The session matches both, including the 04-21 log just outside the window...
    assert coverage["totals"]["matched"] == 1
    # ...but only the 04-22 log is counted or listed.
    assert coverage["totals"]["ai_files"] == 1
    assert [f["timestamp"] for f in coverage["collar_files"]] == ["2026-04-22T00:01:00"]
    assert coverage["collar_only_logs"] == []
