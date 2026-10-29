"""Unit tests for labeling data parsers and analyzer."""

from pathlib import Path

import pytest

from backend.services.labeling_data_analyzer import (
    LabelingDataAnalyzer,
    canonicalize_activity_label,
    format_ui_summary,
    parse_collar_collected,
    parse_duration_to_seconds,
    parse_durations,
    parse_filename,
    parse_rel_path,
    parse_user_reported,
    sanitize_collar_sn,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "labeling"
TREE = Path(__file__).resolve().parents[1] / "fixtures" / "labeling_tree"


def _read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class TestParsers:
    def test_parse_filename(self):
        parsed = parse_filename(
            "activity_session_2026-04-21T18:38:31_0_collar_collected.txt"
        )
        assert parsed == {
            "family": "activity",
            "timestamp": "2026-04-21T18:38:31",
            "index": 0,
            "kind": "collar_collected",
        }
        gps = parse_filename(
            "gps_session_2025-10-10T12:13:33_0_durations.txt"
        )
        assert gps == {
            "family": "gps",
            "timestamp": "2025-10-10T12:13:33",
            "index": 0,
            "kind": "durations",
        }
        assert parse_filename("random.txt") is None

    def test_parse_rel_path_nested_and_legacy(self):
        nested = parse_rel_path(
            "laura@x.com/24h4290312rt/activity_session_2026-04-21T18:38:31_0_durations.txt"
        )
        assert nested["user"] == "laura@x.com"
        assert nested["collar_sn"] == "24h4290312rt"
        assert nested["kind"] == "durations"

        legacy = parse_rel_path(
            "laura@x.com/activity_session_2026-04-21T18:38:31_0_durations.txt"
        )
        assert legacy["user"] == "laura@x.com"
        assert legacy["collar_sn"] is None
        assert sanitize_collar_sn(" 24h4290312rt ") == "24h4290312rt"

    def test_parse_duration_to_seconds(self):
        assert parse_duration_to_seconds("00:00:00") == 0.0
        assert parse_duration_to_seconds("00:00:01.5000000") == pytest.approx(1.5)
        assert parse_duration_to_seconds("00:01:24.2000000") == pytest.approx(84.2)

    def test_canonicalize_activity_label(self):
        assert canonicalize_activity_label("Standing (10)") == "Standing"
        assert canonicalize_activity_label("Standing") == "Standing"
        assert canonicalize_activity_label("RunningPlaying (4)") == "RunningPlaying"
        assert canonicalize_activity_label("  Sedentary  ") == "Sedentary"

    def test_parse_collar_collected(self):
        text = _read("activity_session_2026-04-21T18:38:31_0_collar_collected.txt")
        parsed = parse_collar_collected(text)
        assert parsed.dog_name == "Diamond"
        assert parsed.dog_breed == "Mixed"
        assert parsed.collar_sn == "24h4290312rt"
        assert parsed.session_started is True
        assert parsed.session_ended is True
        labels = [e["label"] for e in parsed.activity_events]
        assert labels == ["OnShelf (12)", "Standing (10)", "OnShelf (12)"]
        assert parsed.activity_events[0]["note"] == "initial state"

    def test_parse_durations(self):
        text = _read("activity_session_2026-04-21T18:38:31_0_durations.txt")
        durations = parse_durations(text)
        assert durations["Standing (10)"] == pytest.approx(1.5)
        assert durations["OnShelf (12)"] == 0.0

    def test_parse_user_reported(self):
        text = _read("activity_session_2026-04-21T18:38:31_0_user_reported.txt")
        parsed = parse_user_reported(text)
        assert len(parsed.events) == 2
        assert parsed.events[0]["label"] == "Standing (10)"
        assert parsed.events[0]["event"] == "touch start"
        assert parsed.events[1]["event"] == "touch end"


class TestLocalAnalyze:
    def test_analyze_local_tree(self):
        assert TREE.exists(), f"missing fixture tree {TREE}"
        analyzer = LabelingDataAnalyzer(bucket_name="local", prefix="extracted-txt/")
        summary = analyzer.analyze_local(str(TREE))
        assert summary["total_users"] >= 1
        assert summary["total_files"] >= 3
        assert summary["files_by_kind"]["collar_collected"] >= 1
        assert summary["files_by_kind"]["durations"] >= 1
        assert "Standing" in summary["activity_duration_seconds"]
        assert "Standing (10)" not in summary["activity_duration_seconds"]
        assert summary["activity_duration_seconds"]["Standing"] > 0
        assert summary["collar_activity_events"].get("Standing", 0) >= 1
        assert summary["user_reported_events"].get("Standing", 0) >= 1
        assert summary["by_date"]
        assert summary["by_date"][0]["date"] == "2026-04-21"
        assert summary["by_date"][0]["duration_seconds"] > 0
        assert summary["by_date"][0]["sessions"] >= 1
        assert summary["by_date"][0]["dogs"] == 1
        assert summary["by_date"][0]["by_user"][0]["dogs"] == 1
        assert summary["total_dogs"] == 1
        diamond = next(d for d in summary["dogs"] if d["collar_sn"] == "24h4290312rt")
        assert diamond["name"] == "Diamond"
        assert diamond["breed"] == "Mixed"
        assert diamond["sessions"] == 2
        assert diamond["total_duration_seconds"] == pytest.approx(85.7)
        assert diamond["owners"] == ["laura.k.entsminger@gmail.com"]
        standing_dogs = summary["activity_dog_counts"]["Standing"]
        assert standing_dogs == 1
        assert summary["activity_owner_counts"]["Standing"] == 1
        assert summary["sessions"]
        assert summary["sessions"][0]["collar_sn"]
        assert summary["sessions"][0]["duration_seconds"] > 0

    def test_format_ui_summary(self):
        analyzer = LabelingDataAnalyzer(bucket_name="local", prefix="extracted-txt/")
        ui = format_ui_summary(analyzer.analyze_local(str(TREE)))
        assert ui["totals"]["users"] >= 1
        assert ui["totals"]["dogs"] == 1
        assert ui["totals"]["duration_seconds"] > 0
        standing = next(a for a in ui["activities"] if a["name"] == "Standing")
        assert standing["label"] == "Standing"
        assert standing["dogs"] == 1
        assert standing["owners"] == 1
        assert ui["by_date"]
        assert ui["by_date"][0]["date"] == "2026-04-21"
        assert ui["by_date"][0]["dogs"] == 1
        assert ui["users"][0]["email"]
        assert ui["users"][0]["total_duration_seconds"] > 0
        assert ui["users"][0]["dogs"] == 1
        assert ui["users"][0]["collar_sns"]
        assert ui["users"][0]["collars"]
        assert ui["users"][0]["collars"][0]["collar_sn"] == "24h4290312rt"
        diamond = next(d for d in ui["dogs"] if d["collar_sn"] == "24h4290312rt")
        assert diamond["sessions"] == 2
        assert diamond["total_duration_seconds"] == pytest.approx(85.7)

    def test_gps_indoor_outdoor_summary(self):
        analyzer = LabelingDataAnalyzer(bucket_name="local", prefix="extracted-txt/")
        summary = analyzer.analyze_local(str(TREE))
        gps = summary.get("gps") or {}
        assert gps.get("total_files", 0) >= 3
        assert gps["activity_duration_seconds"].get("IndoorBlocked", 0) > 0
        assert gps["activity_duration_seconds"].get("OutdoorOpenSky", 0) > 0
        ui = format_ui_summary(summary)
        assert ui["gps"]["totals"]["duration_seconds"] > 0
        assert ui["gps"]["totals"]["dogs"] == 1
        indoor = next(a for a in ui["gps"]["activities"] if a["name"] == "IndoorBlocked")
        assert indoor["dogs"] == 1
        assert indoor["owners"] == 1
        gps_dog = next(d for d in ui["gps"]["dogs"] if d["collar_sn"] == "24h4390528rt")
        assert gps_dog["name"] == "Reeses Midnight"
        assert gps_dog["owners"] == ["kehrman@halocollar.com"]
        assert gps_dog["sessions"] == 1
        assert gps_dog["total_duration_seconds"] == pytest.approx(141.5)

    def test_merges_bare_and_id_duration_labels(self, tmp_path: Path):
        user_dir = tmp_path / "labeler@x.com" / "collar1"
        user_dir.mkdir(parents=True)
        (user_dir / "activity_session_2026-04-21T18:38:31_0_durations.txt").write_text(
            '{\n  "Standing (10)": "00:00:10.0000000",\n  "Walking (1)": "00:00:05.0000000"\n}\n',
            encoding="utf-8",
        )
        (user_dir / "activity_session_2026-04-21T18:39:26_2_durations.txt").write_text(
            '{\n  "Standing": "00:00:03.0000000",\n  "Walking": "00:00:02.0000000"\n}\n',
            encoding="utf-8",
        )
        analyzer = LabelingDataAnalyzer(bucket_name="local", prefix="extracted-txt/")
        summary = analyzer.analyze_local(str(tmp_path))
        assert summary["activity_duration_seconds"]["Standing"] == pytest.approx(13.0)
        assert summary["activity_duration_seconds"]["Walking"] == pytest.approx(7.0)
        assert len(summary["activity_duration_seconds"]) == 2

    def test_unknown_collar_excluded_from_dog_counts(self, tmp_path: Path):
        known = tmp_path / "owner@x.com" / "snknown1"
        known.mkdir(parents=True)
        (known / "activity_session_2026-04-21T18:38:31_0_durations.txt").write_text(
            '{ "Standing (10)": "00:00:10.0000000" }\n',
            encoding="utf-8",
        )
        (known / "activity_session_2026-04-21T18:38:31_0_collar_collected.txt").write_text(
            "18:38:31.123: Dog's name: Ace\n"
            "18:38:31.150: Dog's breed: Beagle\n"
            "18:38:31.150: Dog's weight: 12.5\n"
            "18:38:31.150: Collar SN: snknown1\n",
            encoding="utf-8",
        )
        legacy = tmp_path / "owner@x.com"
        (legacy / "activity_session_2026-04-22T18:38:31_0_durations.txt").write_text(
            '{ "Walking (1)": "00:00:04.0000000" }\n',
            encoding="utf-8",
        )

        analyzer = LabelingDataAnalyzer(bucket_name="local", prefix="extracted-txt/")
        summary = analyzer.analyze_local(str(tmp_path))
        assert summary["total_dogs"] == 1
        by_day = {row["date"]: row for row in summary["by_date"]}
        assert by_day["2026-04-21"]["dogs"] == 1
        assert by_day["2026-04-21"]["by_user"][0]["dogs"] == 1
        assert by_day["2026-04-22"]["dogs"] == 0

        ui = format_ui_summary(summary)
        assert ui["totals"]["dogs"] == 1
        assert ui["users"][0]["dogs"] == 1
        standing = next(a for a in ui["activities"] if a["name"] == "Standing")
        walking = next(a for a in ui["activities"] if a["name"] == "Walking")
        assert standing["dogs"] == 1
        assert standing["owners"] == 1
        assert walking["dogs"] == 0
        assert walking["owners"] == 1
        known_dog = next(d for d in ui["dogs"] if d["collar_sn"] == "snknown1")
        unknown_dog = next(d for d in ui["dogs"] if d["collar_sn"] == "_unknown")
        assert known_dog["name"] == "Ace"
        assert known_dog["breed"] == "Beagle"
        assert known_dog["sessions"] == 1
        assert known_dog["total_duration_seconds"] == pytest.approx(10.0)
        assert known_dog["owners"] == ["owner@x.com"]
        assert unknown_dog["total_duration_seconds"] == pytest.approx(4.0)
        assert unknown_dog["sessions"] == 1
