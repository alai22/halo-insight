"""Staging upload health: when Make.com last uploaded, and batches Process can't read."""

from datetime import datetime, timedelta, timezone

from backend.services.labeling_ingest_service import (
    LabelingIngestService,
    classify_staging_batches,
    gmail_message_time,
)


def test_gmail_message_time_decodes_the_id():
    assert gmail_message_time("1a1976cc04da78f3") == "2026-11-01T14:04:09Z"
    assert gmail_message_time("not-a-gmail-id") is None


def _info(extracted=0, raw=0, meta=True, uploaded_at="2026-11-02T13:00:00Z"):
    return {"extracted": extracted, "raw": raw, "meta": meta, "uploaded_at": uploaded_at}


def test_classify_flags_meta_only_zip_only_and_name_folders():
    batches = {
        ("brandon rivera", "1a1976cc04da78f3"): _info(),  # meta-only, display-name folder
        ("Lindsey Delaney", "1a19ffff00000000"): _info(extracted=3),  # files, but not an email
        ("brandon rivera", "1a19c5b0459ac393"): _info(),  # meta beside readable files: fine
        ("brivera@halocollar.com", "1a19c5b0459ac393"): _info(extracted=132, raw=1),
        ("lindsey@example.com", "1a19aaaa00000000"): _info(raw=1),  # never unzipped
        ("ana@example.com", "1a19bbbb00000000"): _info(meta=True),  # upload stopped
        ("_forwards", "1a19cccc00000000"): _info(),  # quarantine is handled elsewhere
    }
    rows = {(b["folder"], b["message_id"]): b["reason"] for b in classify_staging_batches(batches)}
    assert set(rows) == {
        ("brandon rivera", "1a1976cc04da78f3"),
        ("Lindsey Delaney", "1a19ffff00000000"),
        ("lindsey@example.com", "1a19aaaa00000000"),
        ("ana@example.com", "1a19bbbb00000000"),
    }
    assert "Only _meta.json" in rows[("brandon rivera", "1a1976cc04da78f3")]
    assert "isn't an email address" in rows[("Lindsey Delaney", "1a19ffff00000000")]
    assert "never unzipped" in rows[("lindsey@example.com", "1a19aaaa00000000")]
    assert "Only _meta.json" in rows[("ana@example.com", "1a19bbbb00000000")]


class _S3:
    def __init__(self, objects):
        self.objects = objects

    def get_paginator(self, _name):
        objects = self.objects

        class _P:
            def paginate(self, Bucket, Prefix):  # noqa: N803
                yield {"Contents": [o for o in objects if o["Key"].startswith(Prefix)]}

        return _P()

    def get_object(self, Bucket, Key):  # noqa: N803
        raise KeyError(Key)


def test_staging_status_reports_a_stalled_upload(monkeypatch):
    now = datetime.now(timezone.utc)
    old = now - timedelta(hours=30)
    objects = [
        {"Key": "staging/ana@example.com/1a19bbbb00000000/_meta.json", "LastModified": old, "Size": 10},
        {
            "Key": "staging/bo@example.com/1a19dddd00000000/extracted/"
            "activity_session_2026-10-29T10:00:00_0_durations.txt",
            "LastModified": old,
            "Size": 10,
        },
    ]
    service = LabelingIngestService(bucket_name="b", s3_client=_S3(objects))
    monkeypatch.setattr(service, "pending_forwards", lambda: None)
    uploads = service.staging_status()["uploads"]
    assert uploads["stale"] is True
    assert uploads["hours_since_upload"] >= 29
    assert uploads["unreadable_recent_count"] == 1
    assert uploads["unreadable"][0]["message_id"] == "1a19bbbb00000000"

    objects.append({
        "Key": "staging/bo@example.com/1a19eeee00000000/_meta.json",
        "LastModified": now,
        "Size": 10,
    })
    assert service.staging_status()["uploads"]["stale"] is False
