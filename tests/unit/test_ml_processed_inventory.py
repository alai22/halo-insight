"""Unit tests for the ml-processed collar-log inventory."""

import json

from backend.services.ml_processed_inventory import (
    MlProcessedInventory,
    ml_object_key_allowed,
    parse_missing_csv,
    parse_ml_log_filename,
)


def test_parse_collar_and_bench_filenames():
    collar = parse_ml_log_filename(
        "ai_log_fftnet_v3_4c_2026-10-14_21-06-08_v5_24h4290093rt.csv"
    )
    assert collar["session_at"] == "2026-10-14T21:06:08"
    assert collar["collar_sn"] == "24h4290093rt"
    assert collar["kind"] == "collar"
    assert collar["version"] == "v5"
    assert collar["ext"] == "csv"

    duplicate = parse_ml_log_filename(
        "ai_log_fftnet_v3_4c_2026-09-20_23-38-15_v5 (1)_26h5232291rt.json"
    )
    assert duplicate["collar_sn"] == "26h5232291rt"
    assert duplicate["ext"] == "json"
    assert duplicate["session_at"] == "2026-09-20T23:38:15"

    bench = parse_ml_log_filename("ai_log_on_shelf_50f_8c_2026-07-06_00-53-57_v3.csv")
    assert bench["collar_sn"] is None
    assert bench["kind"] == "on_shelf"

    carry = parse_ml_log_filename("ai_log_hand_carry_50f_8c_2026-07-06_08-30-09_v3.csv")
    assert carry["kind"] == "hand_carry"
    assert parse_ml_log_filename("notes.txt") is None


def test_parse_missing_csv_coerces_numbers():
    text = (
        "collar_sn,dog_name,sessions,minutes\n"
        "24h4290093rt,Joey,34,87.5\n"
    )
    rows = parse_missing_csv(text)
    assert rows == [
        {"collar_sn": "24h4290093rt", "dog_name": "Joey", "sessions": 34, "minutes": 87.5}
    ]
    assert parse_missing_csv("") == []


def test_download_key_must_stay_under_prefix():
    prefix = "ml-processed/"
    assert ml_object_key_allowed("ml-processed/activity/csv-logs/a.csv", prefix)
    assert not ml_object_key_allowed("extracted-txt/a.csv", prefix)
    assert not ml_object_key_allowed("ml-processed/../extracted-txt/a.csv", prefix)
    assert not ml_object_key_allowed("/ml-processed/a.csv", prefix)


class _FakeS3:
    def __init__(self, objects):
        self.objects = dict(objects)

    def get_paginator(self, _name):
        client = self

        class _Pager:
            def paginate(self, Bucket=None, Prefix=""):  # noqa: N803
                keys = sorted(k for k in client.objects if k.startswith(Prefix))
                yield {
                    "Contents": [
                        {"Key": k, "Size": len(client.objects[k]), "LastModified": None}
                        for k in keys
                    ]
                }

        return _Pager()

    def get_object(self, Bucket=None, Key=None):  # noqa: N803
        class _Body:
            def __init__(self, data):
                self._data = data

            def read(self):
                return self._data

        if Key not in self.objects:
            raise KeyError(Key)
        return {"Body": _Body(self.objects[Key])}


def test_build_inventory_pairs_sidecars_and_gap_reports():
    csv_key = (
        "ml-processed/activity/csv-logs/"
        "ai_log_fftnet_v3_4c_2026-10-14_21-06-08_v5_24h4290093rt.csv"
    )
    json_key = csv_key[:-3] + "json"
    bench_csv = (
        "ml-processed/activity/csv-logs/"
        "ai_log_on_shelf_50f_8c_2026-07-06_00-53-57_v3.csv"
    )
    other_csv = (
        "ml-processed/activity/csv-logs-gyro-fix/"
        "ai_log_fftnet_v3_4c_2026-05-01_12-00-00_v5_24h4290093rt.csv"
    )
    sidecar = {
        "collar_sn": "24h4290093rt",
        "dog_name": "Joey",
        "labeler": "LindseyW7485@gmail.com",
        "source_log": "ai_log.log",
        "source_zip": "activity_session_2026-10-14T21:06:07_0",
    }
    missing_collars = (
        "collar_sn,dog_name,sessions,minutes,labelers\n"
        "24h111,Ada,2,10,ada@example.com\n"
    )
    missing_sessions = (
        "collar_sn,dog_name,labeler,session,start,minutes\n"
        "24h111,Ada,ada@example.com,activity_session_x,2026-03-06 21:43:01,20.0\n"
    )
    s3 = _FakeS3(
        {
            csv_key: b"csv-bytes",
            json_key: json.dumps(sidecar).encode(),
            bench_csv: b"bench",
            other_csv: b"older",
            "ml-processed/activity/csv-logs/notes.txt": b"nope",
            "ml-processed/missing-collar-logs/activity_missing_by_collar.csv": missing_collars.encode(),
            "ml-processed/missing-collar-logs/activity_missing_sessions.csv": missing_sessions.encode(),
        }
    )
    report = MlProcessedInventory(bucket_name="test", prefix="ml-processed/", s3_client=s3).build()

    assert report["totals"]["sessions"] == 3
    assert report["totals"]["collars"] == 1
    assert report["totals"]["bench_sessions"] == 1
    assert report["totals"]["unparsed"] == 1
    assert report["totals"]["missing_collars"] == 1
    assert report["totals"]["missing_sessions"] == 1

    newest = report["sessions"][0]
    assert newest["dataset"] == "csv-logs"
    assert newest["dog_name"] == "Joey"
    assert newest["labeler"] == "lindseyw7485@gmail.com"
    assert newest["source_zip"] == "activity_session_2026-10-14T21:06:07_0"
    assert newest["csv_key"] == csv_key
    assert newest["json_key"] == json_key

    by_id = {row["id"]: row for row in report["datasets"]}
    assert by_id["csv-logs"]["collar_sessions"] == 1
    assert by_id["csv-logs"]["bench_sessions"] == 1
    assert by_id["csv-logs"]["unparsed"] == 1
    assert by_id["csv-logs-gyro-fix"]["sessions"] == 1

    assert report["collars"][0]["collar_sn"] == "24h4290093rt"
    assert report["collars"][0]["sessions"] == 2
    assert report["collars"][0]["dog_name"] == "Joey"
    assert report["missing"]["by_collar"][0]["sessions"] == 2
    assert report["unparsed"][0]["filename"] == "notes.txt"
