"""
Inventory of collar logs copied into S3 under ml-processed/.

Layout:
  ml-processed/activity/<dataset>/<log>.csv
  ml-processed/activity/<dataset>/<log>.json   # sidecar: collar_sn, dog, labeler
  ml-processed/missing-collar-logs/activity_missing_by_collar.csv
  ml-processed/missing-collar-logs/activity_missing_sessions.csv

The CSV bodies are not read. Session time and collar SN come from the filename;
dog name and labeler come from the JSON sidecar when it is present.
"""

from __future__ import annotations

import csv
import io
import json
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

import boto3

from ..utils.config import Config
from ..utils.logging import get_logger
from .labeling_data_analyzer import UNKNOWN_COLLAR_SN, sanitize_collar_sn

logger = get_logger("ml_processed_inventory")

MISSING_BY_COLLAR = "activity_missing_by_collar.csv"
MISSING_SESSIONS = "activity_missing_sessions.csv"

# ai_log_fftnet_v3_4c_2026-10-14_21-06-08_v5_24h4290093rt.csv
# ai_log_fftnet_v3_4c_2026-09-20_23-38-15_v5 (1)_26h5232291rt.json
# ai_log_on_shelf_50f_8c_2026-07-06_00-53-57_v3.csv
_LOG_NAME_RE = re.compile(
    r"^(?P<stem>.+?)_(?P<date>\d{4}-\d{2}-\d{2})_(?P<time>\d{2}-\d{2}-\d{2})"
    r"(?:_(?P<version>v\d+))?"
    r"(?: \(\d+\))?"
    r"(?:_(?P<sn>\d{2}[A-Za-z][A-Za-z0-9]+))?"
    r"\.(?P<ext>csv|json)$",
    re.IGNORECASE,
)

_INT_FIELDS = {"sessions", "near_miss_seconds"}
_FLOAT_FIELDS = {"minutes"}


def ml_object_key_allowed(key: str, prefix: str) -> bool:
    """True when key is a single object under the collar-log prefix."""
    if not key or key.startswith("/") or "\\" in key:
        return False
    parts = key.split("/")
    if any(part in ("", ".", "..") for part in parts):
        return False
    root = prefix if prefix.endswith("/") else f"{prefix}/"
    return key.startswith(root)


def parse_ml_log_filename(filename: str) -> Optional[Dict[str, Any]]:
    """Parse a copied log filename. Returns None when the name has no session timestamp."""
    match = _LOG_NAME_RE.match(filename or "")
    if not match:
        return None
    date = match.group("date")
    clock = match.group("time").replace("-", ":")
    sn = (match.group("sn") or "").lower() or None
    stem = match.group("stem") or ""
    return {
        "basename": filename[: -(len(match.group("ext")) + 1)],
        "ext": match.group("ext").lower(),
        "session_at": f"{date}T{clock}",
        "version": (match.group("version") or "").lower() or None,
        "collar_sn": sn,
        "kind": _classify_kind(stem, sn),
    }


def _classify_kind(stem: str, collar_sn: Optional[str]) -> str:
    lowered = (stem or "").lower()
    if "hand_carry" in lowered or "hand-carry" in lowered:
        return "hand_carry"
    if "on_shelf" in lowered or "on-shelf" in lowered:
        return "on_shelf"
    if collar_sn:
        return "collar"
    return "other"


def _iso(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = str(value).strip()
    return text or None


def _num(value: Any, kind: str) -> Any:
    if value is None or value == "":
        return None
    try:
        if kind == "int":
            return int(float(value))
        return float(value)
    except (TypeError, ValueError):
        return value


def parse_missing_csv(text: str) -> List[Dict[str, Any]]:
    """Parse a missing-collar gap report. Empty input yields an empty list."""
    if not text or not text.strip():
        return []
    rows: List[Dict[str, Any]] = []
    reader = csv.DictReader(io.StringIO(text))
    for raw in reader:
        if not raw:
            continue
        row: Dict[str, Any] = {}
        for key, value in raw.items():
            if not key:
                continue
            name = key.strip()
            cell = (value or "").strip()
            if name in _INT_FIELDS:
                row[name] = _num(cell, "int")
            elif name in _FLOAT_FIELDS:
                row[name] = _num(cell, "float")
            else:
                row[name] = cell or None
        if any(row.values()):
            rows.append(row)
    return rows


def _apply_sidecar(session: Dict[str, Any], payload: Any) -> None:
    if not isinstance(payload, dict):
        return
    for field in ("dog_name", "labeler", "source_log", "source_zip", "sn_source"):
        value = payload.get(field)
        if isinstance(value, str) and value.strip():
            session[field] = value.strip()
    labeler = session.get("labeler")
    if isinstance(labeler, str):
        session["labeler"] = labeler.lower()
    sn = payload.get("collar_sn")
    if isinstance(sn, str) and sn.strip():
        cleaned = sanitize_collar_sn(sn).lower()
        if cleaned and cleaned != UNKNOWN_COLLAR_SN:
            session["collar_sn"] = cleaned
            if session.get("kind") == "other":
                session["kind"] = "collar"


def _dataset_and_filename(rel: str) -> Optional[Tuple[str, str]]:
    parts = [p for p in (rel or "").split("/") if p]
    if not parts:
        return None
    filename = parts[-1]
    if not filename or filename.endswith("/"):
        return None
    dataset = parts[0] if len(parts) > 1 else "activity"
    return dataset, filename


def assemble_inventory(
    sessions: List[Dict[str, Any]],
    unparsed: List[Dict[str, Any]],
    missing_by_collar: List[Dict[str, Any]],
    missing_sessions: List[Dict[str, Any]],
    *,
    bucket: str,
    prefix: str,
) -> Dict[str, Any]:
    """Roll session rows into dataset cards, a collar table, and totals."""
    datasets: Dict[str, Dict[str, Any]] = {}
    collars: Dict[str, Dict[str, Any]] = {}

    def _dataset(name: str) -> Dict[str, Any]:
        row = datasets.get(name)
        if row is None:
            row = {
                "id": name,
                "sessions": 0,
                "collar_sessions": 0,
                "bench_sessions": 0,
                "bytes": 0,
                "collar_sns": set(),
                "session_date_min": None,
                "session_date_max": None,
                "copied_at_max": None,
            }
            datasets[name] = row
        return row

    for session in sessions:
        ds = _dataset(session.get("dataset") or "activity")
        ds["sessions"] += 1
        ds["bytes"] += int(session.get("bytes") or 0)
        session_at = session.get("session_at") or ""
        day = session_at[:10] if len(session_at) >= 10 else None
        if day:
            if ds["session_date_min"] is None or day < ds["session_date_min"]:
                ds["session_date_min"] = day
            if ds["session_date_max"] is None or day > ds["session_date_max"]:
                ds["session_date_max"] = day
        copied = session.get("last_modified")
        if copied and (ds["copied_at_max"] is None or copied > ds["copied_at_max"]):
            ds["copied_at_max"] = copied
        sn = session.get("collar_sn")
        if session.get("kind") == "collar" and sn:
            ds["collar_sessions"] += 1
            ds["collar_sns"].add(sn)
            collar = collars.get(sn)
            if collar is None:
                collar = {
                    "collar_sn": sn,
                    "dog_name": None,
                    "labelers": set(),
                    "datasets": set(),
                    "sessions": 0,
                    "bytes": 0,
                    "first_session": None,
                    "last_session": None,
                }
                collars[sn] = collar
            collar["sessions"] += 1
            collar["bytes"] += int(session.get("bytes") or 0)
            collar["datasets"].add(session.get("dataset") or "activity")
            if session.get("labeler"):
                collar["labelers"].add(session["labeler"])
            is_newest = bool(session_at) and (
                collar["last_session"] is None or session_at >= collar["last_session"]
            )
            if session_at:
                if collar["first_session"] is None or session_at < collar["first_session"]:
                    collar["first_session"] = session_at
                if is_newest:
                    collar["last_session"] = session_at
            if session.get("dog_name") and (is_newest or not collar["dog_name"]):
                collar["dog_name"] = session["dog_name"]
        else:
            ds["bench_sessions"] += 1

    for item in unparsed:
        ds = _dataset(item.get("dataset") or "activity")
        ds["bytes"] += int(item.get("bytes") or 0)

    dataset_rows = []
    for row in datasets.values():
        dataset_rows.append(
            {
                "id": row["id"],
                "sessions": row["sessions"],
                "collar_sessions": row["collar_sessions"],
                "bench_sessions": row["bench_sessions"],
                "collars": len(row["collar_sns"]),
                "bytes": row["bytes"],
                "unparsed": sum(1 for item in unparsed if item.get("dataset") == row["id"]),
                "session_date_min": row["session_date_min"],
                "session_date_max": row["session_date_max"],
                "copied_at_max": row["copied_at_max"],
            }
        )
    dataset_rows.sort(key=lambda row: row["id"])

    collar_rows = []
    for row in collars.values():
        collar_rows.append(
            {
                "collar_sn": row["collar_sn"],
                "dog_name": row["dog_name"],
                "labelers": sorted(row["labelers"]),
                "datasets": sorted(row["datasets"]),
                "sessions": row["sessions"],
                "bytes": row["bytes"],
                "first_session": row["first_session"],
                "last_session": row["last_session"],
            }
        )
    collar_rows.sort(key=lambda row: (-row["sessions"], row["collar_sn"]))

    sessions_sorted = sorted(
        sessions,
        key=lambda row: (
            row.get("session_at") or "",
            row.get("dataset") or "",
            row.get("filename") or "",
        ),
        reverse=True,
    )
    collar_sessions = sum(1 for row in sessions if row.get("kind") == "collar" and row.get("collar_sn"))
    return {
        "bucket": bucket,
        "prefix": prefix,
        "totals": {
            "sessions": len(sessions),
            "collar_sessions": collar_sessions,
            "bench_sessions": len(sessions) - collar_sessions,
            "collars": len(collar_rows),
            "datasets": len(dataset_rows),
            "bytes": sum(int(row.get("bytes") or 0) for row in sessions)
            + sum(int(row.get("bytes") or 0) for row in unparsed),
            "unparsed": len(unparsed),
            "missing_collars": len(missing_by_collar),
            "missing_sessions": len(missing_sessions),
        },
        "datasets": dataset_rows,
        "collars": collar_rows,
        "sessions": sessions_sorted,
        "unparsed": unparsed,
        "missing": {
            "by_collar": missing_by_collar,
            "sessions": missing_sessions,
        },
    }


class MlProcessedInventory:
    """List ml-processed collar logs and attach JSON sidecar metadata."""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        prefix: Optional[str] = None,
        region: Optional[str] = None,
        s3_client=None,
    ):
        self.bucket_name = bucket_name or Config.LABELING_S3_BUCKET_NAME
        self.prefix = (prefix or Config.LABELING_S3_ML_PREFIX or "ml-processed/").rstrip("/") + "/"
        self.region = region or Config.S3_REGION or "us-east-1"
        self.s3_client = s3_client or boto3.client("s3", region_name=self.region)
        if not self.bucket_name:
            raise ValueError("LABELING_S3_BUCKET_NAME is not configured")

    @property
    def activity_prefix(self) -> str:
        return f"{self.prefix}activity/"

    @property
    def missing_prefix(self) -> str:
        return f"{self.prefix}missing-collar-logs/"

    def build(self) -> Dict[str, Any]:
        objects = self._list(self.activity_prefix)
        sessions, unparsed, json_keys = self._pair_objects(objects)
        sidecars = self._fetch_json_map(json_keys)
        for session in sessions:
            key = session.get("json_key")
            if key:
                _apply_sidecar(session, sidecars.get(key))
        missing_by_collar = self._read_missing(MISSING_BY_COLLAR)
        missing_sessions = self._read_missing(MISSING_SESSIONS)
        return assemble_inventory(
            sessions,
            unparsed,
            missing_by_collar,
            missing_sessions,
            bucket=self.bucket_name,
            prefix=self.prefix,
        )

    def _list(self, prefix: str) -> List[Dict[str, Any]]:
        found: List[Dict[str, Any]] = []
        paginator = self.s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                key = obj.get("Key") or ""
                if not key or key.endswith("/"):
                    continue
                found.append(obj)
        return found

    def _pair_objects(
        self, objects: Iterable[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
        groups: Dict[Tuple[str, str], Dict[str, Any]] = {}
        unparsed: List[Dict[str, Any]] = []
        for obj in objects:
            key = obj.get("Key") or ""
            rel = key[len(self.activity_prefix) :] if key.startswith(self.activity_prefix) else key
            located = _dataset_and_filename(rel)
            if not located:
                continue
            dataset, filename = located
            parsed = parse_ml_log_filename(filename)
            if not parsed:
                unparsed.append(
                    {
                        "dataset": dataset,
                        "key": key,
                        "filename": filename,
                        "bytes": int(obj.get("Size") or 0),
                        "last_modified": _iso(obj.get("LastModified")),
                    }
                )
                continue
            slot = groups.get((dataset, parsed["basename"]))
            if slot is None:
                slot = {
                    "dataset": dataset,
                    "basename": parsed["basename"],
                    "filename": filename if parsed["ext"] == "csv" else f"{parsed['basename']}.csv",
                    "kind": parsed["kind"],
                    "session_at": parsed["session_at"],
                    "version": parsed["version"],
                    "collar_sn": parsed["collar_sn"],
                    "dog_name": None,
                    "labeler": None,
                    "source_log": None,
                    "source_zip": None,
                    "sn_source": None,
                    "csv_key": None,
                    "json_key": None,
                    "bytes": 0,
                    "last_modified": None,
                }
                groups[(dataset, parsed["basename"])] = slot
            size = int(obj.get("Size") or 0)
            slot["bytes"] += size
            modified = _iso(obj.get("LastModified"))
            if modified and (slot["last_modified"] is None or modified > slot["last_modified"]):
                slot["last_modified"] = modified
            if parsed["ext"] == "csv":
                slot["csv_key"] = key
                slot["filename"] = filename
            else:
                slot["json_key"] = key
            if parsed["collar_sn"] and not slot["collar_sn"]:
                slot["collar_sn"] = parsed["collar_sn"]
            if slot["kind"] == "other" and parsed["kind"] != "other":
                slot["kind"] = parsed["kind"]

        sessions = list(groups.values())
        json_keys = [row["json_key"] for row in sessions if row.get("json_key")]
        return sessions, unparsed, json_keys

    def _fetch_json_map(self, keys: List[str]) -> Dict[str, Any]:
        if not keys:
            return {}
        found: Dict[str, Any] = {}
        workers = min(32, len(keys))
        done = 0
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(self._get_json, key): key for key in keys}
            for future in as_completed(futures):
                key = futures[future]
                done += 1
                try:
                    found[key] = future.result()
                except Exception as exc:  # noqa: BLE001
                    logger.warning("Failed to read sidecar %s: %s", key, exc)
                    found[key] = None
                if done % 400 == 0:
                    logger.info("Read collar-log sidecars %s/%s", done, len(keys))
        return found

    def _get_json(self, key: str) -> Optional[Dict[str, Any]]:
        body = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"].read()
        payload = json.loads(body.decode("utf-8", errors="replace"))
        return payload if isinstance(payload, dict) else None

    def _read_missing(self, filename: str) -> List[Dict[str, Any]]:
        key = f"{self.missing_prefix}{filename}"
        try:
            body = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"].read()
        except Exception as exc:  # noqa: BLE001
            logger.info("Collar-log gap report %s not loaded: %s", key, exc)
            return []
        return parse_missing_csv(body.decode("utf-8", errors="replace"))
