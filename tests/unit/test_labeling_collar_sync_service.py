"""Unit tests for Azure collar AI dump sync and session join."""

from datetime import datetime
from types import SimpleNamespace

from backend.services.labeling_collar_sync_service import (
    CollarAiFile,
    LabelingCollarSyncService,
    match_coverage,
    parse_ai_log_filename,
    redact_secrets,
    resolve_azure_container_url,
)
from backend.services.labeling_data_analyzer import LabelingDataAnalyzer


class _FakeS3:
    def __init__(self, objects=None):
        self.objects = dict(objects or {})
        self.puts = []

    def get_paginator(self, _name):
        client = self

        class _Pager:
            def paginate(self, Bucket=None, Prefix=""):  # noqa: N803
                keys = sorted(k for k in client.objects if k.startswith(Prefix))
                yield {
                    "Contents": [
                        {"Key": k, "Size": len(client.objects[k])} for k in keys
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

    def put_object(self, Bucket=None, Key=None, Body=None, ContentType=None):  # noqa: N803
        data = Body if isinstance(Body, (bytes, bytearray)) else str(Body).encode()
        self.objects[Key] = bytes(data)
        self.puts.append(Key)

    def head_object(self, Bucket=None, Key=None):  # noqa: N803
        if Key not in self.objects:
            raise KeyError(Key)
        body = self.objects[Key]
        return {"ContentLength": len(body), "ETag": '"abc"'}


class _FakeAzure:
    def __init__(self, blobs):
        self.blobs = dict(blobs)

    def list_blobs(self, name_starts_with=""):
        for name, data in sorted(self.blobs.items()):
            if name.startswith(name_starts_with):
                yield SimpleNamespace(name=name, size=len(data))

    def get_blob_client(self, blob):
        name = blob if isinstance(blob, str) else blob.name
        data = self.blobs[name]

        class _Down:
            def readall(self):
                return data

        class _Client:
            def download_blob(self):
                return _Down()

        return _Client()


def _ai(sn, filename, family, ts, size=10):
    when = datetime.fromisoformat(ts)
    return CollarAiFile(
        key=f"collar-raw/{sn}/ai/{filename}",
        collar_sn=sn,
        filename=filename,
        family=family,
        timestamp=ts,
        when=when,
        size=size,
    )


def test_parse_ai_log_filename_variants():
    posture = parse_ai_log_filename(
        "24h4290312rt/ai/ai_log_model_50f_8c_2026-07-02_21-13-44_v3.log"
    )
    assert posture["family"] == "activity"
    assert posture["timestamp"] == "2026-07-02T21:13:44"

    gps = parse_ai_log_filename("ai_gps_log_model_gps_04_2025-12-11_14-45-40.log")
    assert gps["family"] == "gps"
    assert gps["timestamp"] == "2025-12-11T14:45:40"

    v2 = parse_ai_log_filename("ai_log_model_8c_80f_v2_2025-12-11_14-36-23_v2.log")
    assert v2["family"] == "activity"
    assert v2["timestamp"] == "2025-12-11T14:36:23"

    assert parse_ai_log_filename("20260506_204509_log4.log") is None
    assert parse_ai_log_filename("fw_update.log") is None


def test_resolve_azure_container_url_combined_and_split(monkeypatch):
    monkeypatch.setattr(
        "backend.services.labeling_collar_sync_service.Config.LABELING_AZURE_SAS_URL",
        None,
        raising=False,
    )
    monkeypatch.setattr(
        "backend.services.labeling_collar_sync_service.Config.LABELING_AZURE_BLOB_URL",
        None,
        raising=False,
    )
    monkeypatch.setattr(
        "backend.services.labeling_collar_sync_service.Config.LABELING_AZURE_SAS_TOKEN",
        None,
        raising=False,
    )
    assert resolve_azure_container_url() is None
    assert (
        resolve_azure_container_url(sas_url="https://acct.blob.core.windows.net/c?sv=1&sig=x")
        == "https://acct.blob.core.windows.net/c?sv=1&sig=x"
    )
    assert (
        resolve_azure_container_url(
            blob_url="https://acct.blob.core.windows.net/c/",
            sas_token="?sv=1&sig=x",
        )
        == "https://acct.blob.core.windows.net/c/?sv=1&sig=x"
    )


def test_redact_secrets_strips_query_string():
    text = "failed GET https://acct.blob.core.windows.net/c?sv=2024&sig=SUPERSECRET"
    assert "SUPERSECRET" not in redact_secrets(text)
    assert "?***" in redact_secrets(text)


def test_match_coverage_matched_missing_unknown_and_family():
    sessions = [
        {
            "user": "a@x.com",
            "family": "activity",
            "timestamp": "2026-07-02T21:13:40",
            "collar_sn": "24h4290312rt",
            "duration_seconds": 120,
        },
        {
            "user": "a@x.com",
            "family": "gps",
            "timestamp": "2025-12-11T14:45:00",
            "collar_sn": "24h4390528rt",
            "duration_seconds": 60,
        },
        {
            "user": "b@x.com",
            "family": "activity",
            "timestamp": "2026-04-21T18:38:31",
            "collar_sn": "24h4290312rt",
            "duration_seconds": 16,
        },
        {
            "user": "c@x.com",
            "family": "activity",
            "timestamp": "2026-04-21T18:38:31",
            "collar_sn": None,
            "duration_seconds": 10,
        },
    ]
    files = [
        _ai(
            "24h4290312rt",
            "ai_log_model_50f_8c_2026-07-02_21-13-44_v3.log",
            "activity",
            "2026-07-02T21:13:44",
        ),
        _ai(
            "24h4390528rt",
            "ai_gps_log_model_gps_04_2025-12-11_14-45-40.log",
            "gps",
            "2025-12-11T14:45:40",
        ),
    ]
    cov = match_coverage(sessions, files, pad_sec=300)
    assert cov["totals"]["sessions"] == 4
    assert cov["totals"]["matched"] == 2
    assert cov["totals"]["missing"] == 2
    assert cov["totals"]["unknown_sn"] == 1
    assert cov["totals"]["matched_seconds"] == 180.0
    reasons = {s["reason"] for s in cov["unmatched_samples"]}
    assert "time_gap" in reasons
    assert "unknown_sn" in reasons
    # GPS dump must not satisfy the April posture session
    april = [s for s in cov["unmatched_samples"] if s["timestamp"] == "2026-04-21T18:38:31"]
    assert any(s["email"] == "b@x.com" and s["reason"] == "time_gap" for s in april)


def test_sync_copies_ai_only_and_skips_unchanged():
    s3 = _FakeS3(
        {
            "extracted-txt/laura@x.com/24h4290312rt/"
            "activity_session_2026-07-02T21:13:40_0_collar_collected.txt": (
                b"21:13:40.000: Collar SN: 24h4290312rt\n"
            ),
            "extracted-txt/laura@x.com/24h4290312rt/"
            "activity_session_2026-07-02T21:13:40_0_durations.txt": (
                b'{"Standing (10)": "00:02:00.0000000"}\n'
            ),
            "extracted-txt/laura@x.com/24h4290312rt/"
            "activity_session_2026-07-02T21:13:40_0_user_reported.txt": b"",
            # already mirrored — same size as azure blob below
            "collar-raw/24h4290312rt/ai/ai_log_model_50f_8c_2026-07-02_21-13-44_v3.log": b"EXISTING!!",
        }
    )
    azure = _FakeAzure(
        {
            "24h4290312rt/ai/ai_log_model_50f_8c_2026-07-02_21-13-44_v3.log": b"EXISTING!!",
            "24h4290312rt/ai/ai_log_model_50f_8c_2026-07-02_21-16-26_v3.log": b"NEWBYTES",
            "24h4290312rt/logs/20260702_211344_console.log": b"IGNORE",
        }
    )
    svc = LabelingCollarSyncService(
        bucket_name="test-bucket",
        extracted_prefix="extracted-txt/",
        collar_prefix="collar-raw/",
        s3_client=s3,
        azure_client=azure,
        pad_sec=300,
    )
    report = svc.sync(dry_run=False, workers=2)
    assert report["listed"] == 2
    assert report["copied"] == 1
    assert report["skipped_unchanged"] == 1
    new_key = "collar-raw/24h4290312rt/ai/ai_log_model_50f_8c_2026-07-02_21-16-26_v3.log"
    assert s3.objects[new_key] == b"NEWBYTES"
    assert "collar-raw/24h4290312rt/logs/20260702_211344_console.log" not in s3.objects
    assert report["coverage"]["totals"]["matched"] == 1
    assert "labeling-jobs/session_collar_index_v1.json" in s3.objects


def test_analyzer_emits_session_rows():
    from pathlib import Path

    tree = Path(__file__).resolve().parents[1] / "fixtures" / "labeling_tree"
    analyzer = LabelingDataAnalyzer(bucket_name="local", prefix="extracted-txt/")
    summary = analyzer.analyze_local(str(tree))
    sessions = summary.get("sessions") or []
    assert sessions
    diamond = [s for s in sessions if s["collar_sn"] == "24h4290312rt"]
    assert diamond
    assert diamond[0]["duration_seconds"] > 0
    gps = (summary.get("gps") or {}).get("sessions") or []
    assert gps
    assert gps[0]["collar_sn"] == "24h4390528rt"
