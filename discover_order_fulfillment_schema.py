#!/usr/bin/env python3
"""
Schema discovery for the order reconciliation feature.

Runs DESCRIBE TABLE + a small sample against the silver fulfillment table and
prints what it finds, so the endpoint can be written against real column names
instead of assumptions from the discovery doc.

Usage:
    python discover_order_fulfillment_schema.py [--table DB.SCHEMA.TABLE] [--json]

Requires SNOWFLAKE_PAT in .env. Read-only: every statement goes through
backend.services.snowflake_client.assert_read_only().
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List

from backend.services.snowflake_client import get_snowflake_client
from backend.utils.config import Config

# Columns the internal discovery doc claims exist. Treated as hints to verify,
# not as gospel — the whole point of this script is to confirm or refute them.
EXPECTED_COLUMNS = [
    'order_number',
    'netsuite_tranid',
    'sales_order_id',
    'status_code',
    'status_label',
    'fulfillment_warehouse_name',
    'order_fulfillment_warehouse_summary',
    'netsuite_ship_status',
    'netsuite_billing_status',
    'is_aw_order',
    'is_sw_order',
    'is_rep_order',
    'is_rpl_order',
    'primary_shipment_tracking_number',
    'serial_number',
]

# Low-cardinality columns worth profiling so the UI filters can be built from
# real values (and so we catch e.g. an unexpected warehouse name).
PROFILE_COLUMNS = [
    'status_code',
    'status_label',
    'fulfillment_warehouse_name',
    'order_fulfillment_warehouse_summary',
    'netsuite_ship_status',
    'netsuite_billing_status',
]

DATE_HINTS = ('date', 'created', 'ordered', 'trandate', 'timestamp', '_at')


def _print_header(title: str) -> None:
    print()
    print(title)
    print('-' * len(title))


def describe(client, table: str) -> List[Dict[str, Any]]:
    rows = client.describe_table(table)
    _print_header(f'DESCRIBE TABLE {table} — {len(rows)} column(s)')
    for row in rows:
        name = row.get('name', '?')
        dtype = row.get('type', '?')
        nullable = row.get('null?', row.get('null', '?'))
        print(f'  {name:<45} {dtype:<28} null={nullable}')
    return rows


def check_expectations(actual_names: List[str]) -> Dict[str, List[str]]:
    lowered = {n.lower() for n in actual_names}
    present = [c for c in EXPECTED_COLUMNS if c.lower() in lowered]
    missing = [c for c in EXPECTED_COLUMNS if c.lower() not in lowered]

    _print_header('Expected columns from the discovery doc')
    for col in present:
        print(f'  [ok]      {col}')
    for col in missing:
        print(f'  [MISSING] {col}')

    date_like = sorted(
        n for n in actual_names if any(h in n.lower() for h in DATE_HINTS)
    )
    _print_header('Date-ish columns (candidates for order age)')
    for name in date_like:
        print(f'  {name}')
    if not date_like:
        print('  (none found — order age cannot be computed)')

    return {'present': present, 'missing': missing, 'date_candidates': date_like}


def sample(client, table: str, limit: int = 5) -> List[Dict[str, Any]]:
    _, rows = client.run_select(f'SELECT * FROM {table} LIMIT {int(limit)}')
    _print_header(f'Sample rows (LIMIT {limit})')
    for i, row in enumerate(rows, 1):
        print(f'  --- row {i} ---')
        for key, value in row.items():
            rendered = '' if value is None else str(value)
            if len(rendered) > 80:
                rendered = rendered[:77] + '...'
            print(f'    {key:<45} {rendered}')
    return rows


def profile(client, table: str, actual_names: List[str]) -> Dict[str, Any]:
    lowered = {n.lower(): n for n in actual_names}
    out: Dict[str, Any] = {}

    _print_header('Value distributions')
    for col in PROFILE_COLUMNS:
        real = lowered.get(col.lower())
        if not real:
            print(f'  {col}: (column not present, skipped)')
            continue
        _, rows = client.run_select(
            f'SELECT {real} AS value, COUNT(*) AS n FROM {table} '
            f'GROUP BY {real} ORDER BY n DESC LIMIT 30'
        )
        out[real] = rows
        print(f'  {real}:')
        for row in rows:
            print(f'      {str(row.get("VALUE", row.get("value"))):<40} {row.get("N", row.get("n"))}')

    _, total = client.run_select(f'SELECT COUNT(*) AS n FROM {table}')
    row_count = total[0].get('N', total[0].get('n')) if total else None
    print(f'\n  total rows: {row_count}')
    out['_row_count'] = row_count
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--table', default=Config.ORDER_RECON_TABLE)
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--json', action='store_true', help='also dump findings as JSON')
    parser.add_argument('--skip-profile', action='store_true')
    args = parser.parse_args()

    client = get_snowflake_client()
    if not client.is_configured():
        print(
            'SNOWFLAKE_PAT is not set. Add it to .env:\n'
            "    echo 'SNOWFLAKE_PAT=<token-secret>' >> .env",
            file=sys.stderr,
        )
        return 2

    print(f'account={client.account} user={client.user} role={client.role} '
          f'warehouse={client.warehouse}')

    described = describe(client, args.table)
    actual_names = [r.get('name', '') for r in described if r.get('name')]

    findings: Dict[str, Any] = {
        'table': args.table,
        'columns': [
            {'name': r.get('name'), 'type': r.get('type'), 'nullable': r.get('null?')}
            for r in described
        ],
    }
    findings.update(check_expectations(actual_names))

    sample(client, args.table, args.limit)

    if not args.skip_profile:
        findings['distributions'] = profile(client, args.table, actual_names)

    if args.json:
        print()
        print(json.dumps(findings, indent=2, default=str))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
