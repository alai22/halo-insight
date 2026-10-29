#!/usr/bin/env python3
"""
Mirror Azure collar AI dumps into S3 collar-raw/<sn>/ai/ and join to labeled sessions.

Only copies <sn>/ai/* for collar SNs already present in extracted-txt/.

Usage:
  python sync_labeling_collar_data.py --inventory-only
  python sync_labeling_collar_data.py --dry-run
  python sync_labeling_collar_data.py
  python sync_labeling_collar_data.py --sn 24h4290312rt
"""

from __future__ import annotations

import argparse
import json
import sys

from dotenv import load_dotenv

load_dotenv()

from backend.services.labeling_collar_sync_service import (  # noqa: E402
    LabelingCollarSyncService,
    azure_configured,
    redact_secrets,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Plan copies; no S3 writes")
    parser.add_argument(
        "--inventory-only",
        action="store_true",
        help="List Azure ai/ blobs for labeled SNs; do not copy",
    )
    parser.add_argument(
        "--sn",
        action="append",
        dest="sns",
        default=None,
        help="Limit to this collar SN (repeatable)",
    )
    parser.add_argument("--workers", type=int, default=8, help="Parallel copy workers")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    args = parser.parse_args(argv)

    if not azure_configured():
        print(
            "Azure collar blob is not configured. Set LABELING_AZURE_SAS_URL "
            "or LABELING_AZURE_BLOB_URL + LABELING_AZURE_SAS_TOKEN in .env",
            file=sys.stderr,
        )
        return 2

    try:
        report = LabelingCollarSyncService().sync(
            dry_run=args.dry_run,
            inventory_only=args.inventory_only,
            sns=args.sns,
            workers=args.workers,
        )
    except Exception as exc:  # noqa: BLE001
        print(redact_secrets(str(exc)), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2, default=str))
        return 1 if report.get("errors") else 0

    print(f"Bucket: s3://{report['bucket']}/{report['collar_prefix']}")
    print(
        f"dry_run={report['dry_run']} inventory_only={report['inventory_only']} "
        f"sns={report.get('sns_count', 0)}"
    )
    print(
        f"listed={report.get('listed', 0)} copied={report.get('copied', 0)} "
        f"skipped={report.get('skipped_unchanged', 0)} "
        f"bytes_copied={report.get('bytes_copied', 0)} "
        f"errors={len(report.get('errors') or [])}"
    )
    cov = (report.get("coverage") or {}).get("totals") or {}
    if cov:
        print(
            f"Coverage: sessions={cov.get('sessions', 0)} matched={cov.get('matched', 0)} "
            f"missing={cov.get('missing', 0)} unknown_sn={cov.get('unknown_sn', 0)} "
            f"ai_files={cov.get('ai_files', 0)}"
        )
    for sn in report.get("sns") or []:
        print(f"  {sn}")
    for err in (report.get("errors") or [])[:20]:
        print(f"ERROR: {err}", file=sys.stderr)
    return 1 if report.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
