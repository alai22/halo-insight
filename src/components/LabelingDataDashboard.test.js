import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { healthGaps, WhatNeedsDoing } from './LabelingDataDashboard';

// axios ships ESM that CRA's Jest doesn't transform; these tests make no requests.
jest.mock('axios', () => ({ get: jest.fn(), post: jest.fn(), put: jest.fn() }));

const quiet = {
  uploads: null,
  uploadsStale: false,
  unreadableRecent: 0,
  gmailIngest: null,
  pendingForwards: null,
  chartsBehind: false,
  uniqueFiles: 0,
  outputFiles: 0,
  unprocessedEmails: [],
  nextStep: { tone: 'ok' },
  clone: { not_cloned: 0 },
  waitingOnSyncTotal: 0,
  coverage: { totals: {}, missing_reasons: {} },
  stackedTrees: false,
  duplicateRefs: 0,
  incompleteSessions: 0,
};

test('no gaps when everything is current', () => {
  expect(healthGaps(quiet)).toEqual([]);
  expect(renderToStaticMarkup(<WhatNeedsDoing gaps={[]} onAction={() => {}} />)).toContain(
    'Nothing needs doing'
  );
});

// The Nov 2 state: charts behind, an unknown collar log name, and Lindsey's logs waiting for app data.
test('orders gaps by pipeline stage and says what fixes each', () => {
  const gaps = healthGaps({
    ...quiet,
    unreadableRecent: 90,
    chartsBehind: true,
    uniqueFiles: 2582,
    outputFiles: 2538,
    stackedTrees: true,
    duplicateRefs: 1276,
    coverage: {
      totals: { collar_only: 27 },
      missing_reasons: { time_gap: 19, no_blobs_for_sn: 2 },
      collar_only_logs: Array.from({ length: 27 }, () => ({ labelers: ['lindseyw7485@gmail.com'] })),
      unrecognized_logs: {
        count: 51,
        patterns: [
          {
            pattern: 'ai_log_ei_activity_5c',
            count: 51,
            collars: ['24h4290093rt', '26h5364782rt'],
            sample: 'ai_log_ei_activity_5c_2026-10-31_00-27-04_v5.log',
          },
        ],
      },
    },
  });
  expect(gaps.map((g) => g.key)).toEqual([
    'unreadable_uploads',
    'charts_behind',
    'unrecognized_logs',
    'collar_only',
    'no_logs',
    'time_gap',
    'duplicates',
  ]);
  const byKey = Object.fromEntries(gaps.map((g) => [g.key, g]));
  expect(byKey.charts_behind.count).toBe(44);
  expect(byKey.charts_behind.action.key).toBe('process');
  expect(byKey.unrecognized_logs.tone).toBe('error');
  expect(byKey.unrecognized_logs.cause).toContain('ai_log_ei_activity_5c');
  expect(byKey.collar_only.cause).toContain('lindseyw7485 (27)');
  expect(byKey.no_logs.action.key).toBe('reason:no_blobs_for_sn');

  const html = renderToStaticMarkup(<WhatNeedsDoing gaps={gaps} onAction={() => {}} />);
  expect(html).toContain('What needs doing');
  expect(html).toContain('Staging into charts');
  expect(html).toContain('Process staging');
  expect(html).toContain('Outside this page');
});

test('a sync gap offers Sync collar data and Gmail ingest is named for backfills', () => {
  const gaps = healthGaps({
    ...quiet,
    uploadsStale: true,
    uploads: { last_upload_at: '2026-11-01T14:22:00Z' },
    gmailIngest: { enabled: true, configured: true },
    clone: { not_cloned: 12 },
  });
  expect(gaps.map((g) => g.key)).toEqual(['uploads_stale', 'not_synced']);
  expect(gaps[0].todo).toContain('Gmail ingest');
  expect(gaps[1].action.key).toBe('sync');
  expect(gaps[1].count).toBe(12);
});
