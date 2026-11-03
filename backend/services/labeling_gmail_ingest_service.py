"""
Read labeler emails from Gmail and write them in the staging layout Make.com uses.

Labelers email the ai_logs@halocollar.com Google Group. Its mail lands in the
ai_logs_ingest@halocollar.com inbox, which this service reads through the Gmail
API (read-only scope, service account with domain-wide delegation).

Each email becomes one batch, the layout labeling_ingest_service reads:
  <prefix><labeler email>/<gmail message id>/
    raw/<attachment>.zip
    extracted/<activity|gps>_session_*.txt
    _meta.json                       # "ingest_complete": true once every file is in

Unclear senders go to the forward quarantine instead, which
resolve_forward_labeler / promote_forwards already handle:
  <prefix>_forwards/<gmail message id>/  (+ email_body.txt)

Modes, so this can run beside Make until it is trusted:
  shadow  writes to LABELING_GMAIL_SHADOW_PREFIX (staging-gmail/). Process
          staging never reads it; compare_with_make() checks it against staging/.
  live    writes to staging/. Skips any message id Make already delivered
          (any folder, including display-name ones) so both can run at once.

Exactly once: the cursor in labeling-jobs/gmail_ingest_state_<mode>.json keeps
the newest Gmail internalDate seen and the message ids already handled. Each run
lists messages after (newest - overlap) and skips handled ids, so a restart or a
re-run never writes the same email twice. Process staging also de-duplicates
sessions across message ids.
"""

from __future__ import annotations

import base64
import io
import json
import re
import zipfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from email.utils import getaddresses, parseaddr
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple

import boto3

from ..utils.config import Config
from ..utils.logging import get_logger
from .labeling_data_analyzer import FILENAME_RE
from .labeling_ingest_service import (
    FORWARDS_FOLDER,
    RESERVED_STAGING_FOLDERS,
    normalize_labeler_email,
    parse_original_from_forward_body,
)

logger = get_logger("labeling_gmail_ingest_service")

GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
META_SOURCE = "gmail-api-ingest"
MODES = ("shadow", "live")

# Re-list this far behind the newest email seen, in case Gmail indexes late.
CURSOR_OVERLAP = timedelta(days=1)
# Handled ids older than this (behind the cursor) can never be listed again.
PROCESSED_KEEP = timedelta(days=21)
# A message that fails this many runs in a row is left for a person to look at.
MAX_ATTEMPTS = 5
# Zip guards: one member, and everything taken from one email.
MAX_MEMBER_BYTES = 50 * 1024 * 1024
MAX_EMAIL_BYTES = 300 * 1024 * 1024
BODY_META_CHARS = 20000
RECENT_ERRORS_KEEP = 20
RUN_HISTORY_KEEP = 30

FORWARD_SUBJECT_RE = re.compile(r"^\s*(fwd?|fw)\s*:", re.I)
FORWARD_BODY_MARKERS = ("---------- forwarded message", "begin forwarded message")
VIA_DISPLAY_RE = re.compile(r"\bvia\b", re.I)

ProgressFn = Optional[Callable[[str], None]]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _csv_set(value: Optional[str]) -> Set[str]:
    return {s.strip().lower() for s in (value or "").split(",") if s.strip()}


def header_map(message: Dict[str, Any]) -> Dict[str, str]:
    """Lower-cased header name → first value, from a Gmail format=full message."""
    out: Dict[str, str] = {}
    for h in ((message.get("payload") or {}).get("headers") or []):
        name = str(h.get("name") or "").lower()
        if name and name not in out:
            out[name] = str(h.get("value") or "")
    return out


def _addresses(value: Optional[str]) -> List[str]:
    return [addr.strip().lower() for _n, addr in getaddresses([value or ""]) if addr]


def resolve_sender(
    headers: Dict[str, str],
    group_addresses: Iterable[str],
    mailbox: Optional[str] = None,
) -> Tuple[Optional[str], str]:
    """
    The labeler who actually sent an email that reached the inbox.

    Mail through the Google Group shows From as "X via halocollar.com" or as the
    group address itself (DMARC rewrite). The real sender is then in
    X-Original-Sender, Reply-To or X-Original-From. Returns (email, source);
    email is None when nothing trustworthy names a person.
    """
    not_people = {a.lower() for a in group_addresses if a}
    if mailbox:
        not_people.add(mailbox.lower())

    def _person(value: Optional[str]) -> Optional[str]:
        for addr in _addresses(value) or ([value] if value else []):
            email = normalize_labeler_email(addr)
            if email and email not in not_people:
                return email
        return None

    from_value = headers.get("from", "")
    display, from_addr = parseaddr(from_value)
    from_addr = (from_addr or "").lower()
    via_group = from_addr in not_people or bool(VIA_DISPLAY_RE.search(display or ""))

    if not via_group:
        email = _person(from_value)
        if email:
            return email, "from"

    for name in ("x-original-sender", "reply-to", "x-original-from"):
        email = _person(headers.get(name))
        if email:
            return email, name
    # "X via halocollar.com" with X's own address and no group headers.
    if from_addr not in not_people:
        email = _person(from_value)
        if email:
            return email, "from"
    return None, "none"


def looks_forwarded(subject: Optional[str], body: Optional[str]) -> bool:
    if subject and FORWARD_SUBJECT_RE.match(subject):
        return True
    lowered = (body or "").lower()
    return any(marker in lowered for marker in FORWARD_BODY_MARKERS)


def forwarded_for_someone_else(
    subject: Optional[str], body: Optional[str], sender: Optional[str]
) -> bool:
    """A forward whose quoted original is from another person (e.g. Adrian
    forwarding a labeler's email). A labeler forwarding their own mail is theirs."""
    if not looks_forwarded(subject, body):
        return False
    original = parse_original_from_forward_body(body or "")
    return bool(original and original != sender)


def _b64(data: Optional[str]) -> bytes:
    if not data:
        return b""
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def _walk_parts(part: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    yield part
    for child in part.get("parts") or []:
        yield from _walk_parts(child)


def plain_text_body(message: Dict[str, Any]) -> str:
    """First text/plain part (no filename), decoded."""
    for part in _walk_parts(message.get("payload") or {}):
        if part.get("filename"):
            continue
        if str(part.get("mimeType") or "").lower() == "text/plain":
            data = (part.get("body") or {}).get("data")
            if data:
                return _b64(data).decode("utf-8", errors="replace")
    return ""


def attachment_parts(message: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [p for p in _walk_parts(message.get("payload") or {}) if p.get("filename")]


def _safe_name(name: str) -> str:
    base = name.replace("\\", "/").split("/")[-1].strip()
    base = re.sub(r"[^\w.@+-]+", "_", base)
    return base or "attachment"


def extract_session_files(
    zip_bytes: bytes,
    max_member_bytes: int = MAX_MEMBER_BYTES,
) -> Tuple[Dict[str, bytes], List[str]]:
    """
    Session txts from a log zip, keyed by base filename.

    Nested folders are flattened; anything that is not an
    <activity|gps>_session_*.txt (macOS ._ files included) is ignored.
    Returns (files, warnings).
    """
    files: Dict[str, bytes] = {}
    warnings: List[str] = []
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            parts = info.filename.replace("\\", "/").split("/")
            name = parts[-1]
            if "__MACOSX" in parts or name.startswith("._"):
                continue
            if not FILENAME_RE.match(name):
                continue
            if info.file_size > max_member_bytes:
                warnings.append(f"{name}: {info.file_size} bytes is over the size limit; skipped")
                continue
            data = archive.read(info)
            if name in files and files[name] != data:
                warnings.append(f"{name}: two different copies in the zip; kept the larger")
                if len(data) <= len(files[name]):
                    continue
            files[name] = data
    return files, warnings


def service_account_info(value: Optional[str]) -> Dict[str, Any]:
    """
    The key from LABELING_GMAIL_SERVICE_ACCOUNT_JSON: inline JSON, base64 of the
    JSON (one line, safe for docker --env-file), or a path to the key file.
    """
    raw = (value or "").strip()
    if not raw:
        raise ValueError(
            "LABELING_GMAIL_SERVICE_ACCOUNT_JSON is not configured "
            "(service account key JSON, its base64, or a path to it)"
        )
    if raw.startswith("{"):
        return json.loads(raw)
    if raw.endswith(".json") or "/" in raw:
        with open(raw, "r", encoding="utf-8") as fh:
            return json.load(fh)
    try:
        return json.loads(base64.b64decode(raw + "=" * (-len(raw) % 4)).decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(
            "LABELING_GMAIL_SERVICE_ACCOUNT_JSON is not JSON, base64 JSON, or a .json path"
        ) from exc


class GmailClient:
    """Thin read-only wrapper over the Gmail API, so tests can swap in a fake."""

    def __init__(self, service, user_id: str = "me"):
        self._service = service
        self._user = user_id

    @classmethod
    def from_config(cls, mailbox: Optional[str] = None) -> "GmailClient":
        from google.oauth2 import service_account  # imported lazily: optional dependency
        from googleapiclient.discovery import build

        creds = service_account.Credentials.from_service_account_info(
            service_account_info(Config.LABELING_GMAIL_SERVICE_ACCOUNT_JSON),
            scopes=[GMAIL_READONLY_SCOPE],
        )
        subject = mailbox or Config.LABELING_GMAIL_INGEST_MAILBOX
        creds = creds.with_subject(subject)
        service = build("gmail", "v1", credentials=creds, cache_discovery=False)
        return cls(service)

    def list_message_ids(self, query: str) -> List[str]:
        ids: List[str] = []
        token = None
        while True:
            resp = (
                self._service.users()
                .messages()
                # Spam and trash too: a labeler's email filtered as spam, or
                # deleted after Make read it, still belongs in staging.
                .list(
                    userId=self._user,
                    q=query,
                    pageToken=token,
                    maxResults=500,
                    includeSpamTrash=True,
                )
                .execute()
            )
            ids.extend(m["id"] for m in resp.get("messages") or [])
            token = resp.get("nextPageToken")
            if not token:
                return ids

    def get_message(self, message_id: str) -> Dict[str, Any]:
        return (
            self._service.users()
            .messages()
            .get(userId=self._user, id=message_id, format="full")
            .execute()
        )

    def get_attachment(self, message_id: str, attachment_id: str) -> bytes:
        resp = (
            self._service.users()
            .messages()
            .attachments()
            .get(userId=self._user, messageId=message_id, id=attachment_id)
            .execute()
        )
        return _b64(resp.get("data"))


class LabelingGmailIngestService:
    """Turn inbox emails into staging batches (see module docstring)."""

    def __init__(
        self,
        gmail=None,
        s3_client=None,
        bucket_name: Optional[str] = None,
        mode: Optional[str] = None,
        mailbox: Optional[str] = None,
        staging_prefix: Optional[str] = None,
        shadow_prefix: Optional[str] = None,
        group_addresses: Optional[Iterable[str]] = None,
        query: Optional[str] = None,
        initial_lookback_days: Optional[int] = None,
    ):
        self.bucket_name = bucket_name or Config.LABELING_S3_BUCKET_NAME
        if not self.bucket_name:
            raise ValueError("LABELING_S3_BUCKET_NAME is not configured")
        self.mode = (mode or Config.LABELING_GMAIL_INGEST_MODE or "shadow").strip().lower()
        if self.mode not in MODES:
            raise ValueError(f"LABELING_GMAIL_INGEST_MODE must be one of {MODES}, not {self.mode!r}")
        self.mailbox = (mailbox or Config.LABELING_GMAIL_INGEST_MAILBOX or "").lower()
        self.staging_prefix = _prefix(staging_prefix or Config.LABELING_S3_STAGING_PREFIX or "staging/")
        self.shadow_prefix = _prefix(
            shadow_prefix or Config.LABELING_GMAIL_SHADOW_PREFIX or "staging-gmail/"
        )
        if self.shadow_prefix == self.staging_prefix:
            raise ValueError("LABELING_GMAIL_SHADOW_PREFIX must differ from the staging prefix")
        self.group_addresses = (
            {a.lower() for a in group_addresses}
            if group_addresses is not None
            else _csv_set(Config.LABELING_GROUP_SENDERS)
        )
        self.query = Config.LABELING_GMAIL_INGEST_QUERY if query is None else query
        self.initial_lookback_days = int(
            initial_lookback_days
            if initial_lookback_days is not None
            else Config.LABELING_GMAIL_INITIAL_LOOKBACK_DAYS
        )
        self.s3_client = s3_client or boto3.client(
            "s3", region_name=Config.S3_REGION or "us-east-1"
        )
        self._gmail = gmail

    # ------------------------------------------------------------------ paths

    @property
    def target_prefix(self) -> str:
        return self.staging_prefix if self.mode == "live" else self.shadow_prefix

    @property
    def state_key(self) -> str:
        return f"labeling-jobs/gmail_ingest_state_{self.mode}.json"

    @property
    def compare_key(self) -> str:
        return "labeling-jobs/gmail_ingest_compare.json"

    @property
    def gmail(self):
        if self._gmail is None:
            self._gmail = GmailClient.from_config(self.mailbox)
        return self._gmail

    # ------------------------------------------------------------------- S3

    def _get_json(self, key: str) -> Optional[Dict[str, Any]]:
        try:
            body = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"].read()
            data = json.loads(body.decode("utf-8"))
            return data if isinstance(data, dict) else None
        except Exception:  # noqa: BLE001
            return None

    def _put(self, key: str, body: bytes, content_type: str) -> None:
        self.s3_client.put_object(
            Bucket=self.bucket_name, Key=key, Body=body, ContentType=content_type
        )

    def _put_json(self, key: str, data: Dict[str, Any]) -> None:
        self._put(key, json.dumps(data, indent=2, sort_keys=True).encode("utf-8"), "application/json")

    def _list(self, prefix: str, delimiter: Optional[str] = None) -> Iterable[Dict[str, Any]]:
        paginator = self.s3_client.get_paginator("list_objects_v2")
        kwargs: Dict[str, Any] = {"Bucket": self.bucket_name, "Prefix": prefix}
        if delimiter:
            kwargs["Delimiter"] = delimiter
        for page in paginator.paginate(**kwargs):
            yield page

    def load_state(self) -> Dict[str, Any]:
        state = self._get_json(self.state_key) or {}
        state.setdefault("schema_version", 1)
        state.setdefault("mode", self.mode)
        state.setdefault("processed", {})
        state.setdefault("failures", {})
        state.setdefault("totals", {"ingested": 0, "quarantined": 0, "no_logs": 0, "errors": 0})
        state.setdefault("recent_errors", [])
        state.setdefault("runs", [])
        return state

    def save_state(self, state: Dict[str, Any]) -> None:
        state["updated_at"] = _iso(_now())
        self._put_json(self.state_key, state)

    def batches_by_message_id(self, prefix: str) -> Dict[str, List[str]]:
        """message id → folders holding it, from <prefix><folder>/<message id>/."""
        out: Dict[str, List[str]] = defaultdict(list)
        folders: List[str] = []
        for page in self._list(prefix, delimiter="/"):
            for cp in page.get("CommonPrefixes") or []:
                folder = cp["Prefix"][len(prefix):].strip("/")
                if folder and (folder == FORWARDS_FOLDER or folder not in RESERVED_STAGING_FOLDERS):
                    folders.append(folder)
        for folder in folders:
            folder_prefix = f"{prefix}{folder}/"
            for page in self._list(folder_prefix, delimiter="/"):
                for cp in page.get("CommonPrefixes") or []:
                    mid = cp["Prefix"][len(folder_prefix):].strip("/")
                    if mid and not mid.startswith("_"):
                        out[mid].append(folder)
        return dict(out)

    def _has_extracted(self, batch_prefix: str) -> bool:
        resp = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name, Prefix=f"{batch_prefix}extracted/", MaxKeys=1
        )
        return bool(resp.get("Contents"))

    def already_delivered(
        self, message_id: str, index: Dict[str, List[str]]
    ) -> Optional[str]:
        """
        Folder where this email already sits complete under the target prefix.

        Our own batch counts once its _meta.json says ingest_complete; one cut
        off by a restart is written again. A Make batch counts only if it has
        extracted files: Make's dropped emails left _meta.json-only batches, and
        those should be filled in.
        """
        for folder in index.get(message_id) or []:
            batch = f"{self.target_prefix}{folder}/{message_id}/"
            meta = self._get_json(f"{batch}_meta.json")
            if meta and meta.get("source") == META_SOURCE:
                if meta.get("ingest_complete"):
                    return folder
                continue
            if self._has_extracted(batch):
                return folder
        return None

    # -------------------------------------------------------------- one email

    def build_batch(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Everything one email will write, without writing it.

        Returns {folder, files: {relpath: bytes}, meta, extracted, warnings,
        forwarded, labeler, source}. folder is None when the email carries no
        session logs.
        """
        mid = message["id"]
        headers = header_map(message)
        subject = headers.get("subject", "")
        body = plain_text_body(message)
        labeler, source = resolve_sender(headers, self.group_addresses, self.mailbox)
        forwarded = forwarded_for_someone_else(subject, body, labeler)

        files: Dict[str, bytes] = {}
        extracted: Dict[str, bytes] = {}
        attachments: List[str] = []
        warnings: List[str] = []
        total = 0
        for part in attachment_parts(message):
            name = _safe_name(part["filename"])
            lower = name.lower()
            if not (lower.endswith(".zip") or FILENAME_RE.match(name)):
                continue
            body_info = part.get("body") or {}
            if body_info.get("attachmentId"):
                data = self.gmail.get_attachment(mid, body_info["attachmentId"])
            else:
                data = _b64(body_info.get("data"))
            total += len(data)
            if total > MAX_EMAIL_BYTES:
                raise ValueError(f"attachments are over {MAX_EMAIL_BYTES} bytes")
            attachments.append(name)
            if lower.endswith(".zip"):
                files[f"raw/{name}"] = data
                try:
                    got, zip_warnings = extract_session_files(data)
                except zipfile.BadZipFile:
                    warnings.append(f"{name}: not a readable zip")
                    continue
                warnings.extend(f"{name}: {w}" for w in zip_warnings)
                for fname, content in got.items():
                    if fname in extracted and len(extracted[fname]) >= len(content):
                        continue
                    extracted[fname] = content
            else:
                extracted[name] = data

        quarantine = forwarded or not labeler
        folder: Optional[str] = None
        if extracted:
            folder = FORWARDS_FOLDER if quarantine else labeler
        for fname, content in extracted.items():
            files[f"extracted/{fname}"] = content
        if quarantine and folder and body:
            files["email_body.txt"] = body.encode("utf-8")

        internal_ms = int(message.get("internalDate") or 0)
        received_at = (
            _iso(datetime.fromtimestamp(internal_ms / 1000, tz=timezone.utc))
            if internal_ms
            else None
        )
        meta: Dict[str, Any] = {
            "schema_version": 1,
            "source": META_SOURCE,
            "ingest_mode": self.mode,
            "Message ID": mid,
            "gmail_thread_id": message.get("threadId"),
            "rfc822_message_id": headers.get("message-id"),
            "Email Subject": subject,
            "Email Date": headers.get("date"),
            "received_at": received_at,
            "mailbox": self.mailbox,
            "Labeler Email Address": labeler,
            "sender_resolved_from": source,
            "headers": {
                k: headers.get(k)
                for k in ("from", "to", "reply-to", "x-original-sender", "x-original-from")
                if headers.get(k)
            },
            "Attachment Filename": attachments[0] if attachments else None,
            "attachments": attachments,
            "extracted_files": sorted(extracted),
            "ingested_at": _iso(_now()),
        }
        if warnings:
            meta["warnings"] = warnings
        if quarantine:
            meta["needs_attribution"] = True
            meta["forwarded"] = forwarded
            meta["envelope_from"] = labeler
            if body:
                meta["Email Body"] = body[:BODY_META_CHARS]
        return {
            "message_id": mid,
            "folder": folder,
            "files": files,
            "meta": meta,
            "extracted": len(extracted),
            "warnings": warnings,
            "forwarded": forwarded,
            "labeler": labeler,
            "source": source,
            "internal_ms": internal_ms,
        }

    def write_batch(self, batch: Dict[str, Any]) -> str:
        prefix = f"{self.target_prefix}{batch['folder']}/{batch['message_id']}/"
        # Meta first, marked incomplete, so a restart mid-batch is redone, not
        # mistaken for a finished Make batch.
        self._put_json(f"{prefix}_meta.json", {**batch["meta"], "ingest_complete": False})
        for rel, data in batch["files"].items():
            content_type = (
                "application/zip" if rel.lower().endswith(".zip") else "text/plain; charset=utf-8"
            )
            self._put(f"{prefix}{rel}", data, content_type)
        self._put_json(f"{prefix}_meta.json", {**batch["meta"], "ingest_complete": True})
        return prefix

    # ----------------------------------------------------------------- a run

    def _query_after(self, after: datetime, before: Optional[datetime] = None) -> str:
        bits = [f"after:{int(after.timestamp())}"]
        if before:
            bits.append(f"before:{int(before.timestamp())}")
        if self.query:
            bits.append(self.query)
        return " ".join(bits)

    def run(
        self,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        dry_run: bool = False,
        on_progress: ProgressFn = None,
    ) -> Dict[str, Any]:
        """
        Ingest new emails. With since (a backfill), list from that date instead
        of from the cursor; already handled or delivered emails are still skipped.
        """
        started = _now()
        state = self.load_state()
        processed: Dict[str, Any] = state["processed"]
        failures: Dict[str, Any] = state["failures"]

        if since is not None:
            after = since
        elif state.get("cursor_internal_ms"):
            after = datetime.fromtimestamp(
                int(state["cursor_internal_ms"]) / 1000, tz=timezone.utc
            ) - CURSOR_OVERLAP
        else:
            after = started - timedelta(days=self.initial_lookback_days)

        report: Dict[str, Any] = {
            "mode": self.mode,
            "mailbox": self.mailbox,
            "target_prefix": self.target_prefix,
            "backfill": since is not None,
            "dry_run": dry_run,
            "after": _iso(after),
            "before": _iso(until) if until else None,
            "started_at": _iso(started),
            "listed": 0,
            "skipped_processed": 0,
            "skipped_delivered": 0,
            "ingested": 0,
            "quarantined": 0,
            "no_logs": 0,
            "extracted_files": 0,
            "errors": [],
            "warnings": [],
            "batches": [],
        }

        ids = self.gmail.list_message_ids(self._query_after(after, until))
        report["listed"] = len(ids)
        new_ids = [m for m in ids if m not in processed]
        report["skipped_processed"] = len(ids) - len(new_ids)
        # Earlier failures are retried by id, even once they fall out of the window.
        listed = set(new_ids)
        new_ids += [m for m in failures if m not in listed and m not in processed]
        index = self.batches_by_message_id(self.target_prefix) if new_ids else {}

        cursor_ms = int(state.get("cursor_internal_ms") or 0)
        for n, mid in enumerate(new_ids, 1):
            if on_progress:
                on_progress(f"Reading email {n} of {len(new_ids)}…")
            try:
                folder = self.already_delivered(mid, index)
                if folder:
                    report["skipped_delivered"] += 1
                    if not dry_run:
                        processed[mid] = {"at": _iso(_now()), "folder": folder, "outcome": "already_delivered"}
                    continue
                message = self.gmail.get_message(mid)
                batch = self.build_batch(message)
                cursor_ms = max(cursor_ms, batch["internal_ms"])
                report["warnings"].extend(f"{mid}: {w}" for w in batch["warnings"])
                if not batch["folder"]:
                    report["no_logs"] += 1
                    outcome = "no_logs"
                else:
                    if not dry_run:
                        self.write_batch(batch)
                    outcome = "quarantined" if batch["folder"] == FORWARDS_FOLDER else "ingested"
                    report[outcome] += 1
                    report["extracted_files"] += batch["extracted"]
                    report["batches"].append(
                        {
                            "message_id": mid,
                            "folder": batch["folder"],
                            "labeler": batch["labeler"],
                            "sender_resolved_from": batch["source"],
                            "extracted_files": batch["extracted"],
                            "received_at": batch["meta"].get("received_at"),
                        }
                    )
                if not dry_run:
                    processed[mid] = {
                        "at": _iso(_now()),
                        "folder": batch["folder"],
                        "outcome": outcome,
                        "internal_ms": batch["internal_ms"],
                        "rfc822_message_id": batch["meta"].get("rfc822_message_id"),
                    }
                    failures.pop(mid, None)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Gmail ingest of %s failed: %s", mid, exc)
                entry = failures.get(mid) or {"attempts": 0}
                entry = {"attempts": int(entry.get("attempts") or 0) + 1, "error": str(exc)[:500], "at": _iso(_now())}
                report["errors"].append({"message_id": mid, "error": entry["error"], "attempts": entry["attempts"]})
                if not dry_run:
                    if entry["attempts"] >= MAX_ATTEMPTS:
                        # Stop retrying; it stays listed under recent errors.
                        processed[mid] = {"at": entry["at"], "folder": None, "outcome": "failed", "error": entry["error"]}
                        failures.pop(mid, None)
                    else:
                        failures[mid] = entry

        report["finished_at"] = _iso(_now())
        if dry_run:
            return report

        # Only a normal run moves the cursor; a backfill of old dates must not
        # drag it back. Failed emails are retried by id, so it can move past them.
        if since is None:
            state["cursor_internal_ms"] = max(int(state.get("cursor_internal_ms") or 0), cursor_ms)
        state["first_run_at"] = state.get("first_run_at") or report["started_at"]
        state["coverage_start"] = min(
            filter(None, [state.get("coverage_start"), report["after"]])
        )
        _prune_processed(processed, int(state.get("cursor_internal_ms") or 0))
        for key in ("ingested", "quarantined", "no_logs"):
            state["totals"][key] = int(state["totals"].get(key) or 0) + report[key]
        state["totals"]["errors"] = int(state["totals"].get("errors") or 0) + len(report["errors"])
        state["recent_errors"] = (
            state["recent_errors"] + [{**e, "at": report["finished_at"]} for e in report["errors"]]
        )[-RECENT_ERRORS_KEEP:]
        summary = {k: v for k, v in report.items() if k not in ("batches", "warnings")}
        summary["errors"] = len(report["errors"])
        summary["warnings"] = len(report["warnings"])
        state["last_run"] = summary
        if report["ingested"] or report["quarantined"]:
            state["last_ingest_at"] = report["finished_at"]
        state["runs"] = (state["runs"] + [summary])[-RUN_HISTORY_KEEP:]
        self.save_state(state)
        return report

    # --------------------------------------------------------- vs Make.com

    def _batch_inventory(self, prefix: str) -> Dict[str, Dict[str, Any]]:
        """message id → {folder, first_seen, extracted: set} under one prefix."""
        out: Dict[str, Dict[str, Any]] = {}
        for page in self._list(prefix):
            for obj in page.get("Contents") or []:
                rel = obj["Key"][len(prefix):]
                parts = [p for p in rel.split("/") if p]
                if len(parts) < 3:
                    continue
                folder, mid = parts[0], parts[1]
                if mid.startswith("_") or (folder in RESERVED_STAGING_FOLDERS and folder != FORWARDS_FOLDER):
                    continue
                seen = obj.get("LastModified")
                item = out.setdefault(
                    f"{folder}/{mid}",
                    {"folder": folder, "message_id": mid, "first_seen": seen, "extracted": set()},
                )
                if seen and (item["first_seen"] is None or seen < item["first_seen"]):
                    item["first_seen"] = seen
                if len(parts) == 4 and parts[2] == "extracted":
                    item["extracted"].add(parts[3])
        return out

    def compare_with_make(self, since: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Shadow batches (ours) against staging/ (Make), email by email.

        Window: since, else when the shadow ingester first ran (minus the first
        lookback). Make batches are dated by when their objects reached S3.
        """
        shadow_state = (
            self._get_json("labeling-jobs/gmail_ingest_state_shadow.json") or {}
        )
        if since is None and shadow_state.get("coverage_start"):
            since = datetime.strptime(shadow_state["coverage_start"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if since is None:
            since = _now() - timedelta(days=self.initial_lookback_days)

        ours = self._batch_inventory(self.shadow_prefix)
        make_all = self._batch_inventory(self.staging_prefix)
        make = {
            k: v
            for k, v in make_all.items()
            if v["first_seen"] is not None and _aware(v["first_seen"]) >= since
        }

        ours_by_mid: Dict[str, Dict[str, Any]] = {}
        for v in ours.values():
            ours_by_mid.setdefault(v["message_id"], v)
        # Make may name a batch by the RFC Message-ID instead of the Gmail id.
        rfc_to_mid = {
            str(info.get("rfc822_message_id") or "").strip("<> ").lower(): mid
            for mid, info in (shadow_state.get("processed") or {}).items()
            if info.get("rfc822_message_id")
        }
        make_by_mid: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for v in make.values():
            mid = v["message_id"]
            if mid not in ours_by_mid:
                mid = rfc_to_mid.get(mid.strip("<> ").lower(), mid)
            make_by_mid[mid].append(v)

        both, make_only, gmail_only, folder_mismatch, file_diffs = [], [], [], [], []
        for mid, make_batches in sorted(make_by_mid.items()):
            mine = ours_by_mid.get(mid)
            make_files: Set[str] = set().union(*(b["extracted"] for b in make_batches))
            make_folders = sorted({b["folder"] for b in make_batches})
            first_seen = min(_aware(b["first_seen"]) for b in make_batches)
            if not mine:
                make_only.append(
                    {
                        "message_id": mid,
                        "make_folders": make_folders,
                        "make_files": len(make_files),
                        "seen_at": _iso(first_seen),
                    }
                )
                continue
            both.append(mid)
            if mine["folder"] not in make_folders:
                folder_mismatch.append(
                    {"message_id": mid, "make_folders": make_folders, "gmail_folder": mine["folder"]}
                )
            if make_files != mine["extracted"]:
                file_diffs.append(
                    {
                        "message_id": mid,
                        "make_files": len(make_files),
                        "gmail_files": len(mine["extracted"]),
                        "only_make": sorted(make_files - mine["extracted"])[:10],
                        "only_gmail": sorted(mine["extracted"] - make_files)[:10],
                    }
                )
        make_any_time = {v["message_id"] for v in make_all.values()}
        for mid, mine in sorted(ours_by_mid.items()):
            # Make delivered it before the window: not a Gmail-only email.
            if mid in make_by_mid or mid in make_any_time:
                continue
            gmail_only.append(
                {
                    "message_id": mid,
                    "gmail_folder": mine["folder"],
                    "gmail_files": len(mine["extracted"]),
                    "seen_at": _iso(_aware(mine["first_seen"])) if mine["first_seen"] else None,
                }
            )

        # Make's _meta.json-only batches are emails it dropped, not real batches.
        make_empty = [m for m in make_only if not m["make_files"]]
        result = {
            "generated_at": _iso(_now()),
            "since": _iso(since),
            "make_batches": len(make_by_mid),
            "gmail_batches": len(ours_by_mid),
            "both": len(both),
            "make_only": make_only[:100],
            "make_only_count": len(make_only),
            "make_only_empty_count": len(make_empty),
            "gmail_only": gmail_only[:100],
            "gmail_only_count": len(gmail_only),
            "folder_mismatch": folder_mismatch[:100],
            "folder_mismatch_count": len(folder_mismatch),
            "file_diffs": file_diffs[:100],
            "file_diff_count": len(file_diffs),
        }
        # Agree = every Make batch with logs was caught, with the same files.
        result["agrees"] = (
            len(make_only) - len(make_empty) == 0 and not file_diffs
        )
        return result

    def save_compare(self, result: Dict[str, Any]) -> None:
        self._put_json(self.compare_key, result)

    def load_compare(self) -> Optional[Dict[str, Any]]:
        return self._get_json(self.compare_key)


def _prefix(value: str) -> str:
    return value.rstrip("/") + "/"


def _aware(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return datetime.strptime(str(value), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _prune_processed(processed: Dict[str, Any], cursor_ms: int) -> None:
    """Drop handled ids so far behind the cursor that no listing can return them."""
    if not cursor_ms:
        return
    floor = cursor_ms - int(PROCESSED_KEEP.total_seconds() * 1000)
    for mid in [m for m, v in processed.items() if 0 < int((v or {}).get("internal_ms") or 0) < floor]:
        processed.pop(mid, None)


def parse_since(value: str) -> datetime:
    """YYYY-MM-DD (UTC midnight) or a full ISO timestamp."""
    value = (value or "").strip()
    if not value:
        raise ValueError("since is required, e.g. 2026-11-01")
    try:
        if len(value) == 10:
            return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise ValueError(f"Could not read date {value!r}; use YYYY-MM-DD") from exc
