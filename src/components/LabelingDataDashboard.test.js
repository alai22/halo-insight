import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { buildDateLabelStack, buildProgressEmail, healthGaps, WhatNeedsDoing } from './LabelingDataDashboard';

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

describe('buildProgressEmail', () => {
  const progress = {
    target_seconds: 180,
    labels: [
      { key: 'Lying', name: 'Lying', group: 'posture' },
      { key: 'Potty', name: 'Potty', group: 'posture' },
      { key: 'Barking', name: 'Barking', group: 'posture' },
      { key: 'Door', name: 'Door', group: 'environment' },
    ],
  };
  const person = {
    person: 'Ana Lopez',
    emails: ['a@x.com'],
    dogs: ['Rex', 'Bo'],
    labels: { Lying: 400, Potty: 179, Barking: 0, Door: 60 },
  };

  test('lists each label with time so far and what is still needed', () => {
    const email = buildProgressEmail(person, progress);
    expect(email.subject).toBe('Your Halo labeling progress with Rex');
    expect(email.doneCount).toBe(1);
    expect(email.text).toContain('Hi Ana,');
    expect(email.text).toContain('Thank you for labeling with Rex and Bo!');
    // 179s is just short: it rounds down to 2.9 had and up to 0.1 needed, never "done".
    expect(email.text).toMatch(/Potty +2\.9 min +0\.1 min more/);
    expect(email.text).toMatch(/Lying +6\.6 min +✓ Done/);
    expect(email.text).toContain("You've reached 3 minutes in 1 of 4 labels. To finish, that's about 5.1 min more in total");
    expect(email.text).toContain('mostly Barking (3 min), Door (2 min) and Potty (0.1 min)');
    expect(email.html).toContain('<td style="padding:4px 12px;border-bottom:1px solid #e5e7eb;">Potty</td>');
  });

  test('says everything is done, and greets an email-only labeler generically', () => {
    const all = { ...person, person: 'x@y.com', dogs: [], labels: { Lying: 180, Potty: 200, Barking: 999, Door: 180 } };
    const email = buildProgressEmail(all, progress);
    expect(email.text).toContain('Hi there,');
    expect(email.text).toContain('in every label');
    expect(email.subject).toBe('Your Halo labeling progress');
  });

  test('escapes names in the HTML', () => {
    const email = buildProgressEmail({ ...person, dogs: ['<b>Rex</b>'] }, progress);
    expect(email.html).toContain('&lt;b&gt;Rex&lt;/b&gt;');
    expect(email.html).not.toContain('<b>Rex</b>');
  });
});

describe('buildDateLabelStack', () => {
  it('splits each day into labels, biggest label first, keeping empty days', () => {
    const sessions = [
      { timestamp: '2026-11-18T09:00:00', activities: { Lying: 60, Walking: 30 } },
      { timestamp: '2026-11-18T17:00:00', activities: { Lying: 40, Potty: 0 } },
      { timestamp: '2026-11-20T08:00:00', activities: { Walking: 20 } },
    ];
    const days = ['2026-11-18', '2026-11-19', '2026-11-20'].map((date) => ({
      date,
      label: date.slice(5),
      dogs: 1,
      owners: 1,
    }));
    const { rows, keys } = buildDateLabelStack(sessions, days);
    expect(keys).toEqual(['Lying', 'Walking']);
    expect(rows.map((r) => [r.label, r.Lying, r.Walking, r.total])).toEqual([
      ['11-18', 100, 30, 130],
      ['11-19', 0, 0, 0],
      ['11-20', 0, 20, 20],
    ]);
  });
});
