#!/usr/bin/env python3
"""
Ingest labeler emails from the ai_logs_ingest inbox into staging (Gmail API).

Usage:
  python ingest_labeling_gmail.py                       # new mail since the cursor
  python ingest_labeling_gmail.py --since 2026-11-01    # backfill (e.g. the Make gap)
  python ingest_labeling_gmail.py --since 2026-11-01 --until 2026-11-03 --dry-run
  python ingest_labeling_gmail.py --mode live --since 2026-11-01
  python ingest_labeling_gmail.py --compare             # shadow vs Make report

Mode defaults to LABELING_GMAIL_INGEST_MODE (shadow → staging-gmail/, live → staging/).
Re-running is safe: emails already handled or already in staging are skipped.
"""

from __future__ import annotations

import argparse
import json
import sys

from dotenv import load_dotenv

load_dotenv()

from backend.services.labeling_gmail_ingest_service import (  # noqa: E402
    LabelingGmailIngestService,
    parse_since,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--since", help="Backfill from this date (YYYY-MM-DD, UTC)")
    parser.add_argument("--until", help="Stop before this date (YYYY-MM-DD, UTC)")
    parser.add_argument("--mode", choices=["shadow", "live"], help="Override LABELING_GMAIL_INGEST_MODE")
    parser.add_argument("--dry-run", action="store_true", help="Read and parse only; write nothing")
    parser.add_argument("--compare", action="store_true", help="Compare shadow batches with Make's staging/")
    args = parser.parse_args(argv)

    if args.compare:
        service = LabelingGmailIngestService(mode="shadow")
        result = service.compare_with_make(since=parse_since(args.since) if args.since else None)
        service.save_compare(result)
        print(json.dumps(result, indent=2, default=str))
        return 0

    service = LabelingGmailIngestService(mode=args.mode)
    report = service.run(
        since=parse_since(args.since) if args.since else None,
        until=parse_since(args.until) if args.until else None,
        dry_run=args.dry_run,
        on_progress=lambda m: print(m, file=sys.stderr),
    )
    print(json.dumps(report, indent=2, default=str))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
