"""Gmail ingester: sender resolution, zip → staging layout, cursor, re-run safety."""

import base64
import io
import json
import zipfile
from datetime import datetime, timedelta, timezone

import pytest

from backend.services.labeling_gmail_ingest_service import (
    LabelingGmailIngestService,
    extract_session_files,
    forwarded_for_someone_else,
    parse_since,
    resolve_sender,
    service_account_info,
)
from backend.services.labeling_ingest_service import LabelingIngestService

GROUP = {"ai_logs@halocollar.com"}
MAILBOX = "ai_logs_ingest@halocollar.com"
TRIO = (
    "activity_session_2026-11-01T15:09:55_0_collar_collected.txt",
    "activity_session_2026-11-01T15:09:55_0_durations.txt",
    "activity_session_2026-11-01T15:09:55_0_user_reported.txt",
)


# ----------------------------------------------------------------- fakes


class FakeS3:
    def __init__(self, objects=None):
        self.objects = {}
        self.modified = {}
        for key, body in (objects or {}).items():
            self.put_object(Key=key, Body=body)
        self.puts = []

    def put_object(self, Bucket=None, Key=None, Body=None, ContentType=None, at=None):  # noqa: N803
        self.objects[Key] = bytes(Body if isinstance(Body, (bytes, bytearray)) else str(Body).encode())
        self.modified[Key] = at or datetime.now(timezone.utc)
        if hasattr(self, "puts"):
            self.puts.append(Key)

    def get_object(self, Bucket=None, Key=None):  # noqa: N803
        if Key not in self.objects:
            raise KeyError(Key)
        data = self.objects[Key]
        return {"Body": io.BytesIO(data)}

    def _page(self, Prefix="", Delimiter=None, MaxKeys=None):  # noqa: N803
        keys = sorted(k for k in self.objects if k.startswith(Prefix))
        if not Delimiter:
            contents = [
                {"Key": k, "Size": len(self.objects[k]), "LastModified": self.modified[k]} for k in keys
            ]
            if MaxKeys:
                contents = contents[:MaxKeys]
            return {"Contents": contents}
        prefixes, contents = set(), []
        for k in keys:
            rest = k[len(Prefix):]
            if Delimiter in rest:
                prefixes.add(Prefix + rest.split(Delimiter)[0] + Delimiter)
            else:
                contents.append({"Key": k})
        return {"Contents": contents, "CommonPrefixes": [{"Prefix": p} for p in sorted(prefixes)]}

    def list_objects_v2(self, Bucket=None, Prefix="", MaxKeys=None, Delimiter=None):  # noqa: N803
        return self._page(Prefix, Delimiter, MaxKeys)

    def get_paginator(self, _name):
        fake = self

        class _P:
            def paginate(self, Bucket=None, Prefix="", Delimiter=None):  # noqa: N803
                yield fake._page(Prefix, Delimiter)

        return _P()


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode()


def make_zip(files, nested="logs/"):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, body in files.items():
            z.writestr(f"{nested}{name}", body)
        z.writestr("__MACOSX/logs/._" + next(iter(files)), b"junk")
        z.writestr(f"{nested}notes.txt", b"not a session")
    return buf.getvalue()


def trio_zip():
    return make_zip({name: f"Collar SN: 24h4290312rt\n{name}".encode() for name in TRIO})


def gmail_message(mid, headers, zip_bytes=None, body="Logs attached", internal=None, zip_name="ai_logs.zip"):
    parts = [{"mimeType": "text/plain", "filename": "", "body": {"data": _b64(body.encode())}}]
    if zip_bytes is not None:
        parts.append(
            {"mimeType": "application/zip", "filename": zip_name, "body": {"attachmentId": f"att-{mid}"}}
        )
    return {
        "id": mid,
        "threadId": f"t-{mid}",
        "internalDate": str(internal or int(datetime(2026, 11, 1, 16, tzinfo=timezone.utc).timestamp() * 1000)),
        "payload": {
            "mimeType": "multipart/mixed",
            "headers": [{"name": k, "value": v} for k, v in headers.items()],
            "parts": parts,
        },
        "_zip": zip_bytes,
    }


class FakeGmail:
    def __init__(self, messages):
        self.messages = {m["id"]: m for m in messages}
        self.queries = []
        self.gets = []
        self.fail = set()

    def list_message_ids(self, query):
        self.queries.append(query)
        after = int(query.split("after:")[1].split()[0]) * 1000
        return [
            mid for mid, m in sorted(self.messages.items()) if int(m["internalDate"]) > after
        ]

    def get_message(self, mid):
        self.gets.append(mid)
        if mid in self.fail:
            raise RuntimeError("Gmail 500")
        return self.messages[mid]

    def get_attachment(self, mid, attachment_id):
        return self.messages[mid]["_zip"]


def via_group(name, email, mid="m1", **kw):
    """What the inbox gets for a group post (DMARC rewrite of From)."""
    return gmail_message(
        mid,
        {
            "From": f"'{name}' via AI Logs <ai_logs@halocollar.com>",
            "To": "ai_logs@halocollar.com",
            "Reply-To": f"{name} <{email}>",
            "X-Original-Sender": email,
            "Subject": "Halo logs",
            "Message-ID": f"<{mid}@mail.gmail.com>",
        },
        trio_zip(),
        **kw,
    )


def service(gmail, s3, mode="shadow", **kw):
    return LabelingGmailIngestService(
        gmail=gmail,
        s3_client=s3,
        bucket_name="test-bucket",
        mode=mode,
        mailbox=MAILBOX,
        staging_prefix="staging/",
        shadow_prefix="staging-gmail/",
        group_addresses=GROUP,
        query="has:attachment",
        initial_lookback_days=3,
        **kw,
    )


NOW_ISH = datetime(2026, 11, 2, 12, tzinfo=timezone.utc)


# ------------------------------------------------------- sender resolution


def test_sender_via_group_uses_original_sender():
    headers = {
        "from": "'Lindsey W' via AI Logs <ai_logs@halocollar.com>",
        "x-original-sender": "lindseyw7485@gmail.com",
        "reply-to": "Lindsey W <lindseyw7485@gmail.com>",
    }
    assert resolve_sender(headers, GROUP, MAILBOX) == ("lindseyw7485@gmail.com", "x-original-sender")


def test_sender_via_group_falls_back_to_reply_to_then_original_from():
    headers = {"from": "AI Logs <ai_logs@halocollar.com>", "reply-to": "Brandon Rivera <brandon@x.com>"}
    assert resolve_sender(headers, GROUP, MAILBOX) == ("brandon@x.com", "reply-to")
    headers = {"from": "ai_logs@halocollar.com", "x-original-from": "Brandon Rivera <brandon@x.com>"}
    assert resolve_sender(headers, GROUP, MAILBOX) == ("brandon@x.com", "x-original-from")


def test_sender_via_display_name_with_own_address():
    headers = {"from": "Brandon Rivera via halocollar.com <brandon@yahoo.com>"}
    assert resolve_sender(headers, GROUP, MAILBOX) == ("brandon@yahoo.com", "from")


def test_sender_direct_email():
    headers = {"from": "Jenny K <jenny@halocollar.com>", "to": MAILBOX}
    assert resolve_sender(headers, GROUP, MAILBOX) == ("jenny@halocollar.com", "from")


def test_sender_unclear_returns_none():
    headers = {"from": "AI Logs <ai_logs@halocollar.com>", "reply-to": "ai_logs@halocollar.com"}
    assert resolve_sender(headers, GROUP, MAILBOX) == (None, "none")


def test_forward_for_someone_else_detected():
    body = "---------- Forwarded message ---------\nFrom: Lindsey <lindseyw7485@gmail.com>\n"
    assert forwarded_for_someone_else("Fwd: logs", body, "alai@halocollar.com")
    # Forwarding your own email keeps it yours.
    assert not forwarded_for_someone_else("Fwd: logs", body, "lindseyw7485@gmail.com")
    assert not forwarded_for_someone_else("Halo logs", "Logs attached", "lindseyw7485@gmail.com")


# ------------------------------------------------------- zip → trio layout


def test_extract_session_files_flattens_and_filters():
    files, warnings = extract_session_files(trio_zip())
    assert sorted(files) == sorted(TRIO)
    assert warnings == []


def test_extract_skips_oversized_member():
    files, warnings = extract_session_files(trio_zip(), max_member_bytes=5)
    assert files == {}
    assert len(warnings) == 3


def test_run_writes_staging_layout_by_email_not_display_name():
    s3 = FakeS3()
    gmail = FakeGmail([via_group("Brandon Rivera", "brandon@yahoo.com", mid="18f0a1")])
    report = service(gmail, s3, mode="live").run()
    assert report["ingested"] == 1 and report["errors"] == []
    prefix = "staging/brandon@yahoo.com/18f0a1/"
    for name in TRIO:
        assert f"{prefix}extracted/{name}" in s3.objects
    assert f"{prefix}raw/ai_logs.zip" in s3.objects
    assert not any("brandon rivera" in k.lower() for k in s3.objects)
    assert not any("notes.txt" in k or "._" in k for k in s3.objects)
    meta = json.loads(s3.objects[f"{prefix}_meta.json"])
    assert meta["Labeler Email Address"] == "brandon@yahoo.com"
    assert meta["sender_resolved_from"] == "x-original-sender"
    assert meta["source"] == "gmail-api-ingest"
    # _meta.json is the last batch write and marks the batch complete.
    assert s3.puts[-2].endswith("_meta.json")  # last put is the cursor state
    assert meta["ingest_complete"] is True

    # Process staging reads it exactly like a Make batch.
    files = LabelingIngestService(
        bucket_name="test-bucket", staging_prefix="staging/", output_prefix="extracted-txt/", s3_client=s3
    ).list_staging_extracted()
    assert {(f.email, f.message_id) for f in files} == {("brandon@yahoo.com", "18f0a1")}
    assert len(files) == 3


def test_unclear_sender_goes_to_forwards_quarantine():
    s3 = FakeS3()
    msg = gmail_message(
        "m9", {"From": "AI Logs <ai_logs@halocollar.com>", "Subject": "logs"}, trio_zip()
    )
    report = service(FakeGmail([msg]), s3, mode="live").run()
    assert report["quarantined"] == 1
    meta = json.loads(s3.objects["staging/_forwards/m9/_meta.json"])
    assert meta["needs_attribution"] is True
    assert "staging/_forwards/m9/email_body.txt" in s3.objects


def test_forwarded_email_quarantined_and_promotable():
    s3 = FakeS3()
    body = (
        "---------- Forwarded message ---------\n"
        "From: Lindsey W <lindseyw7485@gmail.com>\nDate: Sat, Nov 1, 2026\n"
    )
    msg = gmail_message(
        "fw1",
        {"From": "Adrian Lai <alai@halocollar.com>", "Subject": "Fwd: Halo logs"},
        trio_zip(),
        body=body,
    )
    service(FakeGmail([msg]), s3, mode="live").run()
    ingest = LabelingIngestService(
        bucket_name="test-bucket", staging_prefix="staging/", output_prefix="extracted-txt/", s3_client=s3
    )
    pending = ingest.pending_forwards()
    assert [p["labeler_email"] for p in pending["pending"]] == ["lindseyw7485@gmail.com"]


def test_email_without_logs_writes_nothing():
    s3 = FakeS3()
    msg = gmail_message("n1", {"From": "jenny@halocollar.com", "Subject": "hi"}, None)
    report = service(FakeGmail([msg]), s3, mode="live").run()
    assert report["no_logs"] == 1
    assert not any(k.startswith("staging/") for k in s3.objects)


def test_shadow_mode_writes_beside_make_only():
    s3 = FakeS3()
    service(FakeGmail([via_group("Lindsey", "lindseyw7485@gmail.com", mid="s1")]), s3).run()
    assert any(k.startswith("staging-gmail/lindseyw7485@gmail.com/s1/extracted/") for k in s3.objects)
    assert not any(k.startswith("staging/") for k in s3.objects)


# -------------------------------------------------------------- the cursor


def test_cursor_saved_and_resumed_after_restart():
    s3 = FakeS3()
    t1 = int(datetime(2026, 11, 1, 16, tzinfo=timezone.utc).timestamp() * 1000)
    gmail = FakeGmail([via_group("L", "l@x.com", mid="a1", internal=t1)])
    service(gmail, s3, mode="live").run()
    state = json.loads(s3.objects["labeling-jobs/gmail_ingest_state_live.json"])
    assert state["cursor_internal_ms"] == t1
    assert "a1" in state["processed"]
    assert state["last_run"]["ingested"] == 1

    # A new container (fresh service) resumes from the stored cursor.
    t2 = t1 + 3600 * 1000
    gmail.messages["a2"] = via_group("L", "l@x.com", mid="a2", internal=t2)
    fresh = service(gmail, s3, mode="live")
    report = fresh.run()
    after = int(gmail.queries[-1].split("after:")[1].split()[0])
    assert after == (t1 // 1000) - 86400  # cursor minus the one-day overlap
    assert report["ingested"] == 1 and report["skipped_processed"] == 1
    assert gmail.gets.count("a1") == 1


def test_first_run_uses_lookback():
    s3 = FakeS3()
    gmail = FakeGmail([])
    service(gmail, s3).run()
    after = int(gmail.queries[0].split("after:")[1].split()[0])
    expected = (datetime.now(timezone.utc) - timedelta(days=3)).timestamp()
    assert abs(after - expected) < 60


def test_failed_email_retried_then_given_up():
    s3 = FakeS3()
    gmail = FakeGmail([via_group("L", "l@x.com", mid="bad")])
    gmail.fail.add("bad")
    svc = service(gmail, s3, mode="live")
    for attempt in range(1, 6):
        report = svc.run()
        assert report["errors"][0]["attempts"] == attempt
    state = json.loads(s3.objects["labeling-jobs/gmail_ingest_state_live.json"])
    assert state["processed"]["bad"]["outcome"] == "failed"
    assert state["failures"] == {}
    assert svc.run()["errors"] == []


def test_failure_is_retried_by_id_even_outside_window():
    s3 = FakeS3()
    old = int(datetime(2026, 10, 1, tzinfo=timezone.utc).timestamp() * 1000)
    s3.put_object(
        Key="labeling-jobs/gmail_ingest_state_live.json",
        Body=json.dumps({"cursor_internal_ms": old + 40 * 86400 * 1000, "failures": {"x1": {"attempts": 1}}}),
    )
    gmail = FakeGmail([via_group("L", "l@x.com", mid="x1", internal=old)])
    report = service(gmail, s3, mode="live").run()
    assert report["ingested"] == 1


def test_backfill_does_not_move_cursor_back():
    s3 = FakeS3()
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    s3.put_object(
        Key="labeling-jobs/gmail_ingest_state_live.json", Body=json.dumps({"cursor_internal_ms": now_ms})
    )
    gap = int(datetime(2026, 11, 1, 8, tzinfo=timezone.utc).timestamp() * 1000)
    gmail = FakeGmail([via_group("L", "lindseyw7485@gmail.com", mid=f"g{i}", internal=gap + i) for i in range(10)])
    report = service(gmail, s3, mode="live").run(since=parse_since("2026-11-01"))
    assert report["ingested"] == 10 and report["backfill"]
    state = json.loads(s3.objects["labeling-jobs/gmail_ingest_state_live.json"])
    assert state["cursor_internal_ms"] == now_ms


def test_dry_run_writes_nothing():
    s3 = FakeS3()
    report = service(FakeGmail([via_group("L", "l@x.com")]), s3, mode="live").run(dry_run=True)
    assert report["ingested"] == 1
    assert s3.objects == {}


# --------------------------------------------------------- re-run safety


def test_rerun_skips_processed_ids():
    s3 = FakeS3()
    gmail = FakeGmail([via_group("L", "l@x.com", mid="r1")])
    svc = service(gmail, s3, mode="live")
    svc.run()
    writes = len(s3.puts)
    report = svc.run(since=parse_since("2026-10-30"))
    assert report["ingested"] == 0 and report["skipped_processed"] == 1
    assert len(s3.puts) == writes + 1  # only the state file


def test_live_skips_email_make_already_delivered_even_in_display_name_folder():
    s3 = FakeS3({
        "staging/brandon rivera/d1/_meta.json": b"{}",
        f"staging/brandon rivera/d1/extracted/{TRIO[0]}": b"x",
    })
    gmail = FakeGmail([via_group("Brandon Rivera", "brandon@yahoo.com", mid="d1")])
    report = service(gmail, s3, mode="live").run()
    assert report["skipped_delivered"] == 1 and report["ingested"] == 0
    assert gmail.gets == []
    assert not any(k.startswith("staging/brandon@yahoo.com/") for k in s3.objects)


def test_live_fills_in_make_meta_only_batch():
    s3 = FakeS3({"staging/lindseyw7485@gmail.com/e1/_meta.json": b'{"Message ID": "e1"}'})
    gmail = FakeGmail([via_group("Lindsey", "lindseyw7485@gmail.com", mid="e1")])
    report = service(gmail, s3, mode="live").run()
    assert report["ingested"] == 1
    assert f"staging/lindseyw7485@gmail.com/e1/extracted/{TRIO[0]}" in s3.objects


def test_lost_state_still_safe_because_own_meta_marks_done():
    s3 = FakeS3()
    gmail = FakeGmail([via_group("L", "l@x.com", mid="z1")])
    service(gmail, s3, mode="live").run()
    del s3.objects["labeling-jobs/gmail_ingest_state_live.json"]
    report = service(gmail, s3, mode="live").run(since=parse_since("2026-10-30"))
    assert report["skipped_delivered"] == 1 and report["ingested"] == 0


def test_batch_cut_off_by_restart_is_rewritten():
    s3 = FakeS3({
        "staging/l@x.com/p1/_meta.json": json.dumps(
            {"source": "gmail-api-ingest", "ingest_complete": False}
        ),
        f"staging/l@x.com/p1/extracted/{TRIO[0]}": b"partial",
    })
    report = service(FakeGmail([via_group("L", "l@x.com", mid="p1")]), s3, mode="live").run()
    assert report["ingested"] == 1
    assert f"staging/l@x.com/p1/extracted/{TRIO[2]}" in s3.objects
    assert json.loads(s3.objects["staging/l@x.com/p1/_meta.json"])["ingest_complete"] is True


def test_mode_must_be_known():
    with pytest.raises(ValueError):
        service(FakeGmail([]), FakeS3(), mode="both")


# ----------------------------------------------------------- vs Make.com


def test_compare_with_make():
    s3 = FakeS3()
    old = datetime(2026, 10, 1, tzinfo=timezone.utc)
    # Make got c1 (same files) and c2 (display-name folder); missed c3; c4 meta-only.
    for name in TRIO:
        s3.put_object(Key=f"staging/l@x.com/c1/extracted/{name}", Body=b"x")
        s3.put_object(Key=f"staging/brandon rivera/c2/extracted/{name}", Body=b"x")
    s3.put_object(Key="staging/l@x.com/c4/_meta.json", Body=b"{}")
    s3.put_object(Key=f"staging/l@x.com/old/extracted/{TRIO[0]}", Body=b"x", at=old)
    gmail = FakeGmail([
        via_group("L", "l@x.com", mid="c1"),
        via_group("Brandon Rivera", "brandon@yahoo.com", mid="c2"),
        via_group("L", "l@x.com", mid="c3"),
    ])
    svc = service(gmail, s3)
    svc.run(since=parse_since("2026-10-30"))
    result = svc.compare_with_make(since=parse_since("2026-10-30"))
    assert result["both"] == 2
    assert [m["message_id"] for m in result["gmail_only"]] == ["c3"]
    assert result["make_only_count"] == 1 and result["make_only_empty_count"] == 1
    assert result["folder_mismatch"][0]["make_folders"] == ["brandon rivera"]
    assert result["file_diff_count"] == 0
    assert result["agrees"] is True


def test_service_account_key_inline_base64_or_path(tmp_path):
    key = {"type": "service_account", "client_email": "x@y.iam.gserviceaccount.com"}
    raw = json.dumps(key)
    assert service_account_info(raw) == key
    assert service_account_info(base64.b64encode(raw.encode()).decode()) == key
    path = tmp_path / "key.json"
    path.write_text(raw)
    assert service_account_info(str(path)) == key
    with pytest.raises(ValueError):
        service_account_info("")
