import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { AlertCircle, CheckCircle2, Clock, DownloadCloud, Dog, FolderOpen, Play, RefreshCw, Users } from 'lucide-react';
import axios from 'axios';

const PROCESS_POLL_MS = 4000;
const SUMMARY_STORAGE_KEY = 'halo_labeling_summary_v6';
const DOG_CHART_LIMIT = 15;
const COLLAR_SYNC_HINT = 'Copy Azure <sn>/ai/* dumps into S3 collar-raw/ for labeled collars';
const PROMOTE_PROGRESS = 'Copying quarantine batches into staging/<labeler>/…';
const COLLAR_SYNC_PROGRESS = 'Copying Azure <sn>/ai/* into collar-raw/…';

const PHASE_LABELS = {
  listing: 'Listing staging files',
  clearing: 'Clearing previous extracted-txt',
  resolving_sn: 'Resolving collar serials',
  copying: 'Copying files into extracted-txt',
  planning: 'Planning which copies to remove',
  deleting: 'Removing duplicate copies',
  refreshing: 'Refreshing charts',
};

function phaseLabel(progress, job) {
  if (progress?.phase && PHASE_LABELS[progress.phase]) return PHASE_LABELS[progress.phase];
  if (job === 'compact-staging') return 'Removing duplicate copies';
  if (job === 'promote-forwards') return 'Promoting forwards';
  if (job === 'sync-collar') return 'Syncing collar dumps';
  return 'Processing staging';
}

const COLORS = [
  '#4285F4', '#EA4335', '#FBBC04', '#34A853', '#FF6D01', '#9334E6',
  '#00ACC1', '#64B5F6', '#F28B82', '#81C784', '#FFB74D', '#BA68C8',
];

function shortLabeler(email) {
  if (!email) return '?';
  const local = String(email).split('@')[0];
  return local.length > 16 ? `${local.slice(0, 14)}…` : local;
}

function labelerColorMap(emails) {
  const map = {};
  (emails || []).forEach((email, i) => {
    map[email] = COLORS[i % COLORS.length];
  });
  return map;
}

/** Pivot by_date[].by_user into Recharts stacked rows (date × labeler). */
function buildDateLabelerStack(byDate, labelerKeys) {
  return (byDate || []).map((d) => {
    const row = {
      date: d.date,
      label: (d.date || '').length >= 10 ? d.date.slice(5) : d.date,
      total: Number(d.duration_seconds) || 0,
      dogs: Number(d.dogs) || 0,
      owners: Number(d.users) || 0,
    };
    const byUser = {};
    (d.by_user || []).forEach((u) => {
      byUser[u.user] = Number(u.duration_seconds) || 0;
    });
    (labelerKeys || []).forEach((email) => {
      row[email] = byUser[email] || 0;
    });
    return row;
  });
}

/** Pivot users[].activities into Recharts stacked rows (activity × labeler). */
function buildActivityLabelerStack(activities, users, labelerKeys) {
  return (activities || []).map((a) => {
    const row = {
      label: a.label,
      name: displayLabel(a.label),
      total: Number(a.seconds) || 0,
      dogs: Number(a.dogs) || 0,
      owners: Number(a.owners) || 0,
    };
    (labelerKeys || []).forEach((email) => {
      const user = (users || []).find((u) => u.email === email);
      const act = (user?.activities || []).find((x) => x.label === a.label);
      row[email] = Number(act?.seconds) || 0;
    });
    return row;
  });
}

function VarietyTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  const row = payload[0].payload || {};
  const durations = payload.filter((item) => item.dataKey !== 'dogs' && Number(item.value));
  return (
    <div className="bg-white border border-gray-200 rounded-md px-3 py-2 text-xs shadow-sm">
      <div className="font-medium text-gray-900 mb-1">{label}</div>
      {durations.map((item) => (
        <div key={String(item.dataKey)} className="text-gray-700">
          {shortLabeler(item.name || item.dataKey)} {formatSecondsShort(item.value)}
        </div>
      ))}
      <div className="text-gray-500 mt-1">
        {Number(row.dogs) || 0} dogs · {Number(row.owners) || 0} owners
      </div>
    </div>
  );
}

function StackedDurationChart({
  data,
  seriesKeys,
  colorMap,
  xKey = 'label',
  height = 320,
  emptyText = 'No data yet.',
}) {
  if (!data?.length || !seriesKeys?.length) {
    return <p className="text-sm text-gray-500">{emptyText}</p>;
  }
  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data} margin={{ top: 8, right: 8, left: 8, bottom: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey={xKey} tick={{ fontSize: 11 }} interval="preserveStartEnd" />
          <YAxis
            yAxisId="duration"
            tick={{ fontSize: 12 }}
            tickFormatter={(v) => formatSecondsShort(v)}
          />
          <YAxis
            yAxisId="dogs"
            orientation="right"
            tick={{ fontSize: 12 }}
            allowDecimals={false}
            width={36}
          />
          <Tooltip content={<VarietyTooltip />} />
          <Legend
            formatter={(value) => (value === 'Dogs' ? 'Dogs' : shortLabeler(value))}
            wrapperStyle={{ fontSize: 12 }}
          />
          {seriesKeys.map((key, index) => (
            <Bar
              key={key}
              yAxisId="duration"
              dataKey={key}
              name={key}
              stackId="stack"
              fill={colorMap[key] || COLORS[index % COLORS.length]}
              radius={index === seriesKeys.length - 1 ? [3, 3, 0, 0] : [0, 0, 0, 0]}
            />
          ))}
          <Line
            yAxisId="dogs"
            type="monotone"
            dataKey="dogs"
            name="Dogs"
            stroke="#111827"
            strokeWidth={2}
            dot={{ r: 3, fill: '#111827' }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}

function LabelerVarietyChart({ data, height, colorMap, emptyText }) {
  if (!data?.length) {
    return <p className="text-sm text-gray-500">{emptyText}</p>;
  }
  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 20, right: 24, left: 8, bottom: 8 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            xAxisId="duration"
            type="number"
            tick={{ fontSize: 12 }}
            tickFormatter={(v) => formatSecondsShort(v)}
          />
          <XAxis
            xAxisId="dogs"
            type="number"
            orientation="top"
            allowDecimals={false}
            tick={{ fontSize: 12 }}
          />
          <YAxis type="category" dataKey="label" width={120} tick={{ fontSize: 12 }} />
          <Tooltip
            formatter={(value, name, props) => {
              if (name === 'Dogs') return [value, 'Dogs'];
              return [
                `${formatSecondsShort(value)} · ${props.payload.dogs} dogs · ${props.payload.sessions} sessions`,
                props.payload.email,
              ];
            }}
          />
          <Legend wrapperStyle={{ fontSize: 12 }} />
          <Bar
            xAxisId="duration"
            dataKey="seconds"
            name="Duration"
            barSize={10}
            radius={[0, 4, 4, 0]}
          >
            {data.map((entry, index) => (
              <Cell
                key={entry.email}
                fill={(colorMap && colorMap[entry.email]) || COLORS[index % COLORS.length]}
              />
            ))}
          </Bar>
          <Bar
            xAxisId="dogs"
            dataKey="dogs"
            name="Dogs"
            fill="#111827"
            barSize={8}
            radius={[0, 4, 4, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function missingReasonText(row) {
  const parts = [];
  if (row?.no_blobs_for_sn) parts.push(`${row.no_blobs_for_sn} not in S3`);
  if (row?.time_gap) parts.push(`${row.time_gap} time gap`);
  if (row?.unknown_sn) parts.push(`${row.unknown_sn} unknown serial`);
  if (row?.bad_timestamp) parts.push(`${row.bad_timestamp} bad timestamp`);
  if (!parts.length && row?.missing) return `${row.missing} missing`;
  return parts.join(' · ') || '—';
}

const AZURE_ERROR_ADVICE = {
  address:
    'The Azure account URL does not resolve. Check LABELING_AZURE_SAS_URL and LABELING_AZURE_BLOB_URL on the server. A template value like ACCOUNT/CONTAINER in LABELING_AZURE_SAS_URL wins over the token, so delete it or replace it.',
  access:
    'Azure refused the SAS token. Check that it has not expired and that its access policy grants Read and List on this container.',
  container: 'The container named in the Azure URL does not exist. Check the container name.',
  other: 'The error below is what Azure returned.',
};

/** Decide the one thing to do next for collar data, from server state. */
function collarNextStep({ statusLoaded, statusError, azureConfigured, clone, totals, reasons }) {
  if (!statusLoaded) {
    return statusError
      ? {
          tone: 'error',
          title: 'Could not load collar sync status from the server',
          body: 'The page could not tell whether Azure is set up. Click Refresh. If this stays, check the server logs for /api/labeling/status.',
          error: statusError,
          errorLabel: 'Server response',
        }
      : {
          tone: 'info',
          loading: true,
          title: 'Loading collar sync status…',
        };
  }
  if (!azureConfigured) {
    return {
      kind: 'not_configured',
      tone: 'error',
      title: 'Azure is not configured on the server',
      body: 'Set LABELING_AZURE_BLOB_URL and LABELING_AZURE_SAS_TOKEN (or one LABELING_AZURE_SAS_URL) on the server, restart it, then click Check Azure.',
    };
  }
  if (!clone) {
    return {
      tone: 'attention',
      title: 'Azure has not been checked yet',
      body: 'Click Check Azure to list the collar logs for the labeled collars. It does not copy anything.',
    };
  }
  const collars = Number(clone.collars ?? (clone.by_sn || []).length) || 0;
  const legacyUnreadable =
    clone.collars_unreadable == null && (clone.errors || 0) > 0 && !(clone.azure_files || 0);
  const unreadable = legacyUnreadable ? collars : Number(clone.collars_unreadable) || 0;
  if (unreadable > 0) {
    const sample = (clone.error_samples || [])[0] || null;
    return {
      kind: 'unreadable',
      tone: 'error',
      title:
        unreadable === collars
          ? `Azure could not be read for any of the ${collars} labeled collars`
          : `Azure could not be read for ${unreadable} of ${collars} labeled collars`,
      body: `${
        legacyUnreadable
          ? 'Nothing was listed, so nothing could be copied. Click Check Azure again to record the exact error.'
          : AZURE_ERROR_ADVICE[clone.error_kind] || AZURE_ERROR_ADVICE.other
      } After fixing it, restart the server and click Check Azure.`,
      error: sample ? sample.error : null,
      errorSn: sample ? sample.sn : null,
    };
  }
  const notCloned = Number(clone.not_cloned) || 0;
  if (notCloned > 0) {
    return {
      tone: 'attention',
      title: `${notCloned} collar log${notCloned === 1 ? '' : 's'} in Azure ${notCloned === 1 ? 'is' : 'are'} not in S3 yet`,
      body: 'Click Sync collar data to copy them. Sessions match once their collar log is in S3.',
    };
  }
  const missing = Number(totals.missing) || 0;
  if (missing > 0) {
    const parts = [];
    if (reasons.no_blobs_for_sn) {
      parts.push(
        `${reasons.no_blobs_for_sn} are on collars with no logs in Azure. Those collars have not uploaded ai/ logs yet`
      );
    }
    if (reasons.time_gap) {
      parts.push(
        `${reasons.time_gap} are on collars that uploaded logs, but none from around the session time`
      );
    }
    if (reasons.unknown_sn) parts.push(`${reasons.unknown_sn} have no collar serial in the app data`);
    if (reasons.bad_timestamp) parts.push(`${reasons.bad_timestamp} have an unreadable session time`);
    return {
      tone: 'info',
      title: `Azure is copied. ${missing} session${missing === 1 ? '' : 's'} still have no collar log`,
      body: `${parts.join('. ')}. Syncing again will not change these until the collars upload more logs.`,
    };
  }
  return {
    tone: 'ok',
    title: 'Every labeled session has collar data',
    body: 'Azure and S3 match, and each session found a collar log near its time.',
  };
}

const NEXT_STEP_STYLES = {
  error: 'bg-red-50 border-red-200 text-red-900',
  attention: 'bg-amber-50 border-amber-200 text-amber-900',
  info: 'bg-sky-50 border-sky-200 text-sky-900',
  ok: 'bg-emerald-50 border-emerald-200 text-emerald-900',
};

function CollarNextStep({ step }) {
  if (step.loading) {
    return (
      <div className="flex items-center gap-2 text-sm text-gray-500 px-1">
        <RefreshCw className="h-3.5 w-3.5 animate-spin" />
        {step.title}
      </div>
    );
  }
  const Icon = step.tone === 'ok' ? CheckCircle2 : AlertCircle;
  return (
    <div className={`border rounded-lg px-4 py-3 ${NEXT_STEP_STYLES[step.tone]}`}>
      <div className="flex items-start gap-3">
        <Icon className="h-4 w-4 flex-shrink-0 mt-0.5" />
        <div className="min-w-0">
          <div className="text-xs font-medium uppercase tracking-wide opacity-70">Next step</div>
          <div className="text-sm font-semibold mt-0.5">{step.title}</div>
          {step.body ? <p className="text-sm mt-1">{step.body}</p> : null}
          {step.error ? (
            <div className="mt-2 text-xs">
              <div className="opacity-70 mb-1">
                {step.errorLabel || 'Azure error'}
                {step.errorSn ? ` for ${step.errorSn}` : ''}:
              </div>
              <pre className="whitespace-pre-wrap break-all font-mono bg-white/70 border border-black/10 rounded p-2">
                {step.error}
              </pre>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}

const COVERAGE_SEGMENTS = [
  { key: 'matched', label: 'Matched', color: '#34A853' },
  { key: 'no_blobs_for_sn', label: 'No collar log in S3', color: '#EA4335' },
  { key: 'time_gap', label: 'Collar log, wrong time', color: '#FBBC04' },
  { key: 'unknown_sn', label: 'Unknown serial', color: '#9AA0A6' },
  { key: 'bad_timestamp', label: 'Bad timestamp', color: '#5F6368' },
];

/** One bar of all labeled sessions: matched versus each reason they did not match. */
function CoverageBreakdown({ totals, reasons }) {
  const counts = {
    matched: Number(totals.matched) || 0,
    no_blobs_for_sn: Number(reasons.no_blobs_for_sn) || 0,
    time_gap: Number(reasons.time_gap) || 0,
    unknown_sn: Number(reasons.unknown_sn) || 0,
    bad_timestamp: Number(reasons.bad_timestamp) || 0,
  };
  const total = Number(totals.sessions) || Object.values(counts).reduce((a, b) => a + b, 0);
  if (!total) return null;
  const pct = (n) => Math.round((n / total) * 100);
  return (
    <div className="mb-4">
      <div className="flex items-baseline justify-between text-sm mb-1">
        <span className="text-gray-700">
          <span className="font-semibold text-gray-900">{counts.matched}</span> of {total} sessions
          matched ({pct(counts.matched)}%)
        </span>
        <span className="text-xs text-gray-500">
          {formatSecondsShort(totals.matched_seconds)} matched ·{' '}
          {formatSecondsShort(totals.missing_seconds)} not
        </span>
      </div>
      <div className="flex h-3 w-full overflow-hidden rounded-full bg-gray-100">
        {COVERAGE_SEGMENTS.filter((seg) => counts[seg.key] > 0).map((seg) => (
          <div
            key={seg.key}
            style={{ width: `${(counts[seg.key] / total) * 100}%`, backgroundColor: seg.color }}
            title={`${seg.label}: ${counts[seg.key]}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-600 mt-2">
        {COVERAGE_SEGMENTS.filter((seg) => seg.key === 'matched' || counts[seg.key] > 0).map(
          (seg) => (
            <span key={seg.key} className="inline-flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full" style={{ backgroundColor: seg.color }} />
              {seg.label}: {counts[seg.key]}
            </span>
          )
        )}
      </div>
    </div>
  );
}

const COLLAR_LIST_LIMIT = 15;

/** One row per collar: sessions split by match reason, plus Azure and S3 file counts. */
function CollarCoverageList({ rows, behindCount, showAll, onToggleShowAll }) {
  if (rows.length === 0) {
    return <p className="text-sm text-gray-500">No labeled collars in the summary yet.</p>;
  }
  const visible = showAll ? rows : rows.filter((row) => row.behind).slice(0, COLLAR_LIST_LIMIT);
  return (
    <div>
      {visible.length === 0 ? (
        <p className="text-sm text-gray-500">
          No collars are behind. Azure is not ahead of S3, and every session with a serial has a
          dump.
        </p>
      ) : (
        <>
          <div className="hidden sm:grid grid-cols-[9rem_1fr_7rem_9rem] gap-3 text-xs text-gray-500 border-b border-gray-100 pb-1.5">
            <span>Serial</span>
            <span>Sessions with collar data</span>
            <span className="text-right">Matched</span>
            <span className="text-right">Azure → S3 files</span>
          </div>
          <ul className="divide-y divide-gray-100">
            {visible.map((row) => {
              const azureAhead = row.azure_files != null && row.azure_files > row.s3_files;
              return (
                <li
                  key={row.collar_sn}
                  className="grid grid-cols-[9rem_1fr] sm:grid-cols-[9rem_1fr_7rem_9rem] gap-x-3 gap-y-1 items-center py-1.5 text-sm"
                >
                  <span className="font-mono text-xs text-gray-900 truncate" title={row.collar_sn}>
                    {row.collar_sn}
                  </span>
                  <CollarSessionBar row={row} />
                  <span className="text-right tabular-nums text-gray-700 col-start-2 sm:col-start-auto">
                    {row.matched}
                    <span className="text-gray-400"> / {row.sessions}</span>
                  </span>
                  <span
                    className={`text-right tabular-nums ${azureAhead ? 'text-amber-800' : 'text-gray-500'}`}
                    title={azureAhead ? `${row.azure_files - row.s3_files} in Azure not in S3` : undefined}
                  >
                    {row.azure_files == null ? '—' : row.azure_files} → {row.s3_files}
                  </span>
                </li>
              );
            })}
          </ul>
        </>
      )}
      <div className="flex flex-wrap items-center justify-between gap-2 mt-3 text-xs text-gray-600">
        <div className="flex flex-wrap gap-x-4 gap-y-1">
          {COVERAGE_SEGMENTS.map((seg) => (
            <span key={seg.key} className="inline-flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full" style={{ backgroundColor: seg.color }} />
              {seg.label}
            </span>
          ))}
        </div>
        <button
          type="button"
          onClick={onToggleShowAll}
          className="text-gray-500 hover:text-gray-700 underline decoration-dotted underline-offset-2"
        >
          {showAll
            ? `Show only collars that are behind (${behindCount})`
            : `Show all ${rows.length} collars`}
        </button>
      </div>
    </div>
  );
}

/** Sessions on one collar, as a full-width bar split by matched and each miss reason. */
function CollarSessionBar({ row }) {
  const total = row.sessions || 0;
  const reason = missingReasonText(row);
  if (!total) {
    return <span className="text-xs text-gray-400">No app sessions</span>;
  }
  return (
    <div
      className="flex h-2.5 w-full overflow-hidden rounded-full bg-gray-100"
      title={`${row.matched} of ${total} matched${reason !== '—' ? ` · ${reason}` : ''}`}
    >
      {COVERAGE_SEGMENTS.filter((seg) => row[seg.key] > 0).map((seg) => (
        <div
          key={seg.key}
          style={{ width: `${(row[seg.key] / total) * 100}%`, backgroundColor: seg.color }}
        />
      ))}
    </div>
  );
}

function dogAxisLabel(dog) {
  const name = (dog?.name || '').trim() || 'Unnamed';
  const sn = dog?.collar_sn;
  if (!sn || sn === '_unknown') return `${name} · unknown`;
  const short = sn.length > 8 ? sn.slice(-6) : sn;
  return `${name} · ${short}`;
}

const GPS_LABEL_DISPLAY = {
  IndoorBlocked: 'Indoor (blocked)',
  IndoorSeeSky: 'Indoor (see sky)',
  Door: 'Door',
  OutdoorCovered: 'Outdoor (covered)',
  OutdoorOpenSky: 'Outdoor (open sky)',
};

function displayLabel(name) {
  return GPS_LABEL_DISPLAY[name] || name;
}

function CollapsibleTable({ label = 'Show data table', children }) {
  return (
    <details className="mt-4 group">
      <summary className="cursor-pointer list-none text-xs text-gray-500 hover:text-gray-700 inline-flex items-center gap-1 select-none">
        <span className="underline decoration-dotted underline-offset-2">{label}</span>
        <span className="text-gray-400 group-open:hidden">▸</span>
        <span className="text-gray-400 hidden group-open:inline">▾</span>
      </summary>
      <div className="mt-3 overflow-x-auto">{children}</div>
    </details>
  );
}

function ChartCard({ kicker, title, description, children }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-5 h-full">
      {kicker ? (
        <div className="text-xs font-medium uppercase tracking-wide text-gray-400 mb-1">
          {kicker}
        </div>
      ) : null}
      <h3 className="text-lg font-semibold text-gray-900 mb-1">{title}</h3>
      {description ? <p className="text-sm text-gray-500 mb-4">{description}</p> : null}
      {children}
    </div>
  );
}

function DateVolumeTable({ rows }) {
  if (!rows?.length) return null;
  return (
    <CollapsibleTable label="Show date table">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="text-left text-gray-500 border-b">
            <th className="py-2 pr-4 font-medium">Date</th>
            <th className="py-2 pr-4 font-medium">Duration</th>
            <th className="py-2 pr-4 font-medium">Dogs</th>
            <th className="py-2 pr-4 font-medium">Sessions</th>
            <th className="py-2 pr-4 font-medium">Owners</th>
            <th className="py-2 font-medium">Files</th>
          </tr>
        </thead>
        <tbody>
          {[...rows].reverse().map((d) => (
            <tr key={d.date} className="border-b border-gray-100">
              <td className="py-2 pr-4 text-gray-900 font-mono text-xs">{d.date}</td>
              <td className="py-2 pr-4 text-gray-700">{d.human}</td>
              <td className="py-2 pr-4 text-gray-500">{d.dogs}</td>
              <td className="py-2 pr-4 text-gray-500">{d.sessions}</td>
              <td className="py-2 pr-4 text-gray-500">{d.users}</td>
              <td className="py-2 text-gray-500">{d.files}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </CollapsibleTable>
  );
}

function ActivityDurationTable({ rows, labelHeader, formatName }) {
  if (!rows?.length) return null;
  const nameOf = formatName || ((row) => row.label);
  return (
    <CollapsibleTable label={`Show ${labelHeader.toLowerCase()} table`}>
      <table className="min-w-full text-sm">
        <thead>
          <tr className="text-left text-gray-500 border-b">
            <th className="py-2 pr-4 font-medium">{labelHeader}</th>
            <th className="py-2 pr-4 font-medium">Duration</th>
            <th className="py-2 pr-4 font-medium">Seconds</th>
            <th className="py-2 pr-4 font-medium">Dogs</th>
            <th className="py-2 font-medium">Owners</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.label} className="border-b border-gray-100">
              <td className="py-2 pr-4 text-gray-900">{nameOf(row)}</td>
              <td className="py-2 pr-4 text-gray-700">{row.human}</td>
              <td className="py-2 pr-4 text-gray-500">{Number(row.seconds).toFixed(1)}</td>
              <td className="py-2 pr-4 text-gray-500">{row.dogs ?? 0}</td>
              <td className="py-2 text-gray-500">{row.owners ?? 0}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </CollapsibleTable>
  );
}

function LabelerTable({ rows }) {
  if (!rows?.length) return null;
  return (
    <CollapsibleTable label="Show labeler table">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="text-left text-gray-500 border-b">
            <th className="py-2 pr-4 font-medium">Rank</th>
            <th className="py-2 pr-4 font-medium">Labeler</th>
            <th className="py-2 pr-4 font-medium">Duration</th>
            <th className="py-2 pr-4 font-medium">Dogs</th>
            <th className="py-2 pr-4 font-medium">Sessions</th>
            <th className="py-2 font-medium">Files</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((u, i) => (
            <tr key={u.email} className="border-b border-gray-100">
              <td className="py-2 pr-4 text-gray-500">{i + 1}</td>
              <td className="py-2 pr-4 text-gray-900">{u.email}</td>
              <td className="py-2 pr-4 text-gray-700">{u.human}</td>
              <td className="py-2 pr-4 text-gray-500">{u.dogs}</td>
              <td className="py-2 pr-4 text-gray-500">{u.sessions}</td>
              <td className="py-2 text-gray-500">{u.files}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </CollapsibleTable>
  );
}

function formatSecondsShort(seconds) {
  const s = Number(seconds) || 0;
  if (s < 60) return `${s.toFixed(1)}s`;
  const mins = Math.floor(s / 60);
  const rem = s - mins * 60;
  if (mins < 60) return `${mins}m ${rem.toFixed(0)}s`;
  const hours = Math.floor(mins / 60);
  const remMins = mins % 60;
  return `${hours}h ${remMins}m`;
}

function formatUpdatedAt(iso) {
  if (!iso) return null;
  try {
    const d = new Date(iso.endsWith('Z') ? iso : `${iso}Z`);
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleString();
  } catch {
    return iso;
  }
}

function readStoredSummary() {
  try {
    const raw = sessionStorage.getItem(SUMMARY_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed?.data) return null;
    return parsed;
  } catch {
    return null;
  }
}

function writeStoredSummary({ data, generatedAt, cached, stale }) {
  try {
    sessionStorage.setItem(
      SUMMARY_STORAGE_KEY,
      JSON.stringify({
        data,
        generatedAt: generatedAt || null,
        cached: Boolean(cached),
        stale: Boolean(stale),
        savedAt: Date.now(),
      })
    );
  } catch {
    // ignore quota / private mode
  }
}

const LabelingDataDashboard = () => {
  const stored = useMemo(() => readStoredSummary(), []);
  const [data, setData] = useState(stored?.data || null);
  const [status, setStatus] = useState(null);
  const [statusError, setStatusError] = useState(null);
  const [showAllCollars, setShowAllCollars] = useState(false);
  const [processReport, setProcessReport] = useState(null);
  const [processInfo, setProcessInfo] = useState(null);
  const [loading, setLoading] = useState(!stored?.data);
  const [processing, setProcessing] = useState(false);
  const [processNotice, setProcessNotice] = useState(null); // success | error banner after job
  const [promoting, setPromoting] = useState(false);
  const [syncingCollar, setSyncingCollar] = useState(false);
  const [collarMode, setCollarMode] = useState(null);
  const [error, setError] = useState(null);
  const [cached, setCached] = useState(Boolean(stored?.cached));
  const [stale, setStale] = useState(Boolean(stored?.stale));
  const [generatedAt, setGeneratedAt] = useState(stored?.generatedAt || null);
  const [summaryPending, setSummaryPending] = useState(false);
  const [summaryMessage, setSummaryMessage] = useState(null);
  const [expandedUser, setExpandedUser] = useState(null);
  const wasProcessingRef = useRef(false);
  const autoPromoteAttemptedRef = useRef(false);

  const fetchStatus = useCallback(async () => {
    try {
      const response = await axios.get('/api/labeling/status');
      if (response.data.success) {
        const next = response.data.data;
        setStatus(next);
        setStatusError(null);
        const proc = next?.process || null;
        setProcessInfo(proc);
        if (proc?.last_report) {
          setProcessReport(proc.last_report);
        }
        const running = Boolean(proc?.running);
        setProcessing(running);
        setPromoting(running && proc?.job === 'promote-forwards');
        setSyncingCollar(running && proc?.job === 'sync-collar');
        return next;
      }
      setStatusError(response.data.error || 'Status request was not successful');
    } catch (err) {
      // Non-fatal; summary can still load
      console.error('Failed to load labeling status', err);
      setStatusError(
        err?.response
          ? `HTTP ${err.response.status}${err.response.data?.error ? ` · ${err.response.data.error}` : ''}`
          : err?.message || 'Request failed'
      );
    }
    return null;
  }, []);

  const fetchSummary = useCallback(async ({ refresh = false } = {}) => {
    // Keep showing last results while refreshing; only block when we have nothing.
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/api/labeling/summary', {
        params: refresh ? { refresh: 1 } : undefined,
      });
      if (response.data.success) {
        const pending = Boolean(response.data.pending);
        const nextData = response.data.data;
        const nextGenerated = response.data.generated_at || null;
        const nextCached = Boolean(response.data.cached);
        const nextStale = Boolean(response.data.stale) || pending;
        setSummaryPending(pending);
        setSummaryMessage(response.data.message || null);
        setCached(nextCached);
        setStale(nextStale);
        if (nextGenerated) setGeneratedAt(nextGenerated);
        if (nextData) {
          setData(nextData);
          writeStoredSummary({
            data: nextData,
            generatedAt: nextGenerated,
            cached: nextCached,
            stale: nextStale,
          });
        }
      } else {
        setError(response.data.error || 'Failed to load labeling data');
        return false;
      }
    } catch (err) {
      const errorMsg =
        err.response?.data?.error ||
        err.response?.data?.message ||
        err.message ||
        'Failed to load labeling data';
      setError(errorMsg);
      return false;
    } finally {
      setLoading(false);
    }
    return true;
  }, []);

  const processStaging = useCallback(async () => {
    setError(null);
    setProcessNotice(null);
    try {
      const response = await axios.post('/api/labeling/process', {
        dry_run: false,
        clear_output: false,
        async: true,
      });
      if (!response.data.success) {
        throw new Error(response.data.error || 'Process failed');
      }
      wasProcessingRef.current = true;
      setProcessing(true);
      setProcessInfo(
        response.data.data || {
          running: true,
          job: 'process',
          progress: { phase: 'listing', done: 0, total: 0 },
          message: 'Adding new staging files into extracted-txt…',
        }
      );
      setProcessNotice({
        type: 'info',
        text: 'Adding new staging files in the background. Files already in extracted-txt stay put.',
      });
      await fetchStatus();
    } catch (err) {
      if (err.response?.status === 409) {
        wasProcessingRef.current = true;
        setProcessing(true);
        setProcessInfo(err.response.data?.data || { running: true });
        setProcessNotice({
          type: 'info',
          text: 'A process is already running. Waiting for it to finish…',
        });
        await fetchStatus();
        return;
      }
      const errorMsg =
        err.response?.data?.error ||
        err.response?.data?.message ||
        err.message ||
        'Failed to process staging';
      setError(errorMsg);
      setProcessing(false);
    }
  }, [fetchStatus]);

  const compactStaging = useCallback(async () => {
    const health = status?.staging_health || {};
    const dup = health.duplicate_file_refs ?? 0;
    const ok = window.confirm(
      `Remove duplicate copies from staging?\n\nAbout ${dup} extra extracted files will be deleted when a newer email already has the same file at the same size. Raw zips are deleted only for batches that added nothing new. The latest copy stays. Charts do not change until you Process staging.`
    );
    if (!ok) return;
    setError(null);
    setProcessNotice(null);
    try {
      const response = await axios.post('/api/labeling/compact', { async: true });
      if (!response.data.success) {
        throw new Error(response.data.error || 'Compact failed');
      }
      wasProcessingRef.current = true;
      setProcessing(true);
      setProcessInfo(
        response.data.data || {
          running: true,
          job: 'compact-staging',
          progress: { phase: 'listing', done: 0, total: 0 },
          message: 'Listing staging files…',
        }
      );
      await fetchStatus();
    } catch (err) {
      if (err.response?.status === 409) {
        wasProcessingRef.current = true;
        setProcessing(true);
        setProcessInfo(err.response.data?.data || { running: true });
        setProcessNotice({
          type: 'info',
          text: 'A labeling job is already running. Waiting for it to finish…',
        });
        await fetchStatus();
        return;
      }
      const errorMsg =
        err.response?.data?.error ||
        err.response?.data?.message ||
        err.message ||
        'Failed to remove duplicate copies';
      setError(errorMsg);
      setProcessing(false);
    }
  }, [fetchStatus, status]);

  const promoteForwards = useCallback(
    async ({ silent = false } = {}) => {
      setError(null);
      if (!silent) setProcessNotice(null);
      try {
        const response = await axios.post('/api/labeling/promote-forwards', {
          async: true,
        });
        if (!response.data.success) {
          throw new Error(response.data.error || 'Promote failed');
        }
        wasProcessingRef.current = true;
        setProcessing(true);
        setPromoting(true);
        setProcessInfo(
          response.data.data || {
            running: true,
            job: 'promote-forwards',
            message: response.data.message,
          }
        );
        setProcessNotice({
          type: 'info',
          text: silent
            ? 'Small forward batch detected — promoting into staging automatically…'
            : 'Promoting forwarded quarantine batches in the background. Safe to leave this tab.',
        });
        await fetchStatus();
      } catch (err) {
        if (err.response?.status === 409) {
          wasProcessingRef.current = true;
          setProcessing(true);
          setProcessInfo(err.response.data?.data || { running: true });
          setProcessNotice({
            type: 'info',
            text: 'A labeling job is already running. Waiting for it to finish…',
          });
          await fetchStatus();
          return;
        }
        const errorMsg =
          err.response?.data?.error ||
          err.response?.data?.message ||
          err.message ||
          'Failed to promote forwards';
        if (!silent) {
          setError(errorMsg);
        } else {
          setProcessNotice({
            type: 'error',
            text: `Auto-promote failed: ${errorMsg}`,
          });
        }
        setProcessing(false);
        setPromoting(false);
      }
    },
    [fetchStatus]
  );

  const runCollarJob = useCallback(async (inventoryOnly) => {
    setError(null);
    setProcessNotice(null);
    setCollarMode(inventoryOnly ? 'check' : 'sync');
    try {
      const response = await axios.post('/api/labeling/sync-collar', {
        dry_run: false,
        async: true,
        inventory_only: Boolean(inventoryOnly),
      });
      if (!response.data.success) {
        throw new Error(response.data.error || 'Collar sync failed');
      }
      wasProcessingRef.current = true;
      setProcessing(true);
      setSyncingCollar(true);
      setProcessInfo(
        response.data.data || {
          running: true,
          job: 'sync-collar',
          message: response.data.message,
        }
      );
      setProcessNotice({
        type: 'info',
        text: inventoryOnly
          ? 'Checking Azure for labeled collars. This lists ai/ logs and does not copy them.'
          : 'Collar sync started in the background. Copying Azure ai/ dumps into S3 — safe to leave this tab.',
      });
      await fetchStatus();
    } catch (err) {
      if (err.response?.status === 409) {
        wasProcessingRef.current = true;
        setProcessing(true);
        setProcessInfo(err.response.data?.data || { running: true });
        setProcessNotice({
          type: 'info',
          text: 'A labeling job is already running. Waiting for it to finish…',
        });
        await fetchStatus();
        return;
      }
      const errorMsg =
        err.response?.data?.error ||
        err.response?.data?.message ||
        err.message ||
        'Failed to sync collar data';
      setError(errorMsg);
      setProcessing(false);
      setSyncingCollar(false);
      setCollarMode(null);
    }
  }, [fetchStatus]);

  const syncCollar = useCallback(() => runCollarJob(false), [runCollarJob]);
  const checkAzure = useCallback(() => runCollarJob(true), [runCollarJob]);

  useEffect(() => {
    fetchStatus();
    // Prefer cached/last results; only full-screen wait when nothing is stored yet
    fetchSummary({ refresh: false });
  }, [fetchStatus, fetchSummary]);

  // Auto-promote tiny quarantine batches on load; larger ones need a click.
  useEffect(() => {
    const pending = status?.pending_forwards;
    if (!pending || autoPromoteAttemptedRef.current) return;
    if (processing || processInfo?.running) return;
    if (!pending.auto_promote || !(pending.pending_count > 0)) return;
    autoPromoteAttemptedRef.current = true;
    promoteForwards({ silent: true });
  }, [status?.pending_forwards, processing, processInfo?.running, promoteForwards]);

  // If server returned a stale snapshot, poll briefly so background rescan can land
  useEffect(() => {
    if (!stale && !summaryPending) return undefined;
    let cancelled = false;
    let attempts = 0;
    const id = setInterval(async () => {
      attempts += 1;
      // A full scan can take several minutes. Keep the last charts up meanwhile.
      if (cancelled || attempts > 60) {
        clearInterval(id);
        return;
      }
      try {
        const response = await axios.get('/api/labeling/summary');
        if (!response.data?.success || cancelled) return;
        const pending = Boolean(response.data.pending);
        setSummaryPending(pending);
        if (response.data.data && !pending && !response.data.stale) {
          setData(response.data.data);
          setCached(Boolean(response.data.cached));
          setStale(false);
          setGeneratedAt(response.data.generated_at || null);
          writeStoredSummary({
            data: response.data.data,
            generatedAt: response.data.generated_at || null,
            cached: Boolean(response.data.cached),
            stale: false,
          });
          clearInterval(id);
        }
      } catch {
        // keep showing last results
      }
    }, 5000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [stale, summaryPending]);

  // Poll while a background process is running (also resumes after page reload)
  useEffect(() => {
    const running = Boolean(processInfo?.running || processing);
    if (!running) return undefined;

    wasProcessingRef.current = true;
    const id = setInterval(async () => {
      const next = await fetchStatus();
      const stillRunning = Boolean(next?.process?.running);
      if (!stillRunning && wasProcessingRef.current) {
        wasProcessingRef.current = false;
        const proc = next?.process;
        if (proc?.last_error) {
          const jobLabel =
            proc?.job === 'promote-forwards'
              ? 'Promote'
              : proc?.job === 'sync-collar'
                ? 'Collar sync'
                : proc?.job === 'compact-staging'
                  ? 'Remove copies'
                  : 'Process';
          setProcessNotice({
            type: 'error',
            text: `${jobLabel} failed: ${proc.last_error}`,
          });
          setSyncingCollar(false);
          setCollarMode(null);
        } else if (proc?.job === 'promote-forwards') {
          setProcessNotice({
            type: 'success',
            text:
              proc?.message ||
              'Forwards promoted into staging. Click Process staging to include them in charts.',
          });
          setPromoting(false);
        } else if (proc?.job === 'sync-collar') {
          setProcessNotice({
            type: 'success',
            text: proc?.message || 'Collar sync finished. Refreshing coverage…',
          });
          setSyncingCollar(false);
          setCollarMode(null);
          await fetchSummary({ refresh: true });
        } else if (proc?.job === 'compact-staging') {
          setProcessNotice({
            type: 'success',
            text:
              proc?.message ||
              'Duplicate copies removed. Charts stay unchanged until you Process staging.',
          });
          setPromoting(false);
        } else {
          setProcessNotice({
            type: 'info',
            text: 'Processing finished. Refreshing charts…',
          });
          const refreshed = await fetchSummary({ refresh: true });
          setProcessNotice({
            type: refreshed ? 'success' : 'error',
            text: refreshed
              ? proc?.message || 'Processing finished. Charts match the deduped set.'
              : 'Processing finished, but the charts could not be refreshed. Use Refresh.',
          });
        }
      }
    }, PROCESS_POLL_MS);

    return () => clearInterval(id);
  }, [processInfo?.running, processing, fetchStatus, fetchSummary]);

  const totals = data?.totals || {};
  const activities = data?.activities || [];
  const pendingForwards = status?.pending_forwards || null;
  const stagingHealth = status?.staging_health || null;
  const uniqueFiles = stagingHealth?.unique_files_after_dedupe ?? 0;
  const duplicateRefs = stagingHealth?.duplicate_file_refs ?? 0;
  const incompleteSessions = stagingHealth?.incomplete_sessions ?? 0;
  const sizeMismatchSessions = stagingHealth?.size_mismatch_sessions ?? 0;
  const outputFiles = status?.output_files ?? 0;
  const stackedTrees = Boolean(
    stagingHealth &&
      ((stagingHealth.duplicate_ratio || 0) >= 3 || duplicateRefs > 0)
  );
  const chartsBehind = uniqueFiles > 0 && outputFiles < uniqueFiles;
  const showStagingHealth = Boolean(
    stagingHealth &&
      (stackedTrees || chartsBehind || incompleteSessions > 0 || sizeMismatchSessions > 0)
  );
  const progressTotal = Number(processInfo?.progress?.total) || 0;
  const progressDone = Number(processInfo?.progress?.done) || 0;
  const progressPct =
    progressTotal > 0 ? Math.min(100, Math.round((progressDone / progressTotal) * 100)) : null;
  const users = useMemo(() => {
    const list = data?.users || [];
    return [...list].sort(
      (a, b) => (b.total_duration_seconds || 0) - (a.total_duration_seconds || 0)
    );
  }, [data?.users]);
  const labelerKeys = useMemo(() => users.map((u) => u.email).filter(Boolean), [users]);
  const labelerColors = useMemo(() => labelerColorMap(labelerKeys), [labelerKeys]);

  const userContributionData = useMemo(
    () =>
      users.map((u) => ({
        email: u.email,
        label: (u.email || '').split('@')[0] || u.email,
        seconds: u.total_duration_seconds || 0,
        files: u.files || 0,
        sessions: u.sessions || 0,
        dogs: u.dogs || 0,
        human: u.total_duration_human || formatSecondsShort(u.total_duration_seconds),
      })),
    [users]
  );

  const byDate = data?.by_date || [];
  const byDateChartData = useMemo(
    () =>
      byDate.map((d) => ({
        date: d.date,
        label: d.date && d.date.length >= 10 ? d.date.slice(5) : d.date, // MM-DD
        seconds: d.duration_seconds || 0,
        sessions: d.sessions || 0,
        files: d.files || 0,
        users: d.users || 0,
        dogs: d.dogs || 0,
        human: d.duration_human || formatSecondsShort(d.duration_seconds),
      })),
    [byDate]
  );
  const dateLabelerStack = useMemo(
    () => buildDateLabelerStack(byDate, labelerKeys),
    [byDate, labelerKeys]
  );
  const activityLabelerStack = useMemo(
    () => buildActivityLabelerStack(activities, users, labelerKeys),
    [activities, users, labelerKeys]
  );

  const gps = data?.gps || null;
  const gpsTotals = gps?.totals || {};
  const gpsActivities = gps?.activities || [];
  const gpsUsers = useMemo(() => {
    const list = gps?.users || [];
    return [...list].sort(
      (a, b) => (b.total_duration_seconds || 0) - (a.total_duration_seconds || 0)
    );
  }, [gps?.users]);
  const gpsLabelerKeys = useMemo(
    () => gpsUsers.map((u) => u.email).filter(Boolean),
    [gpsUsers]
  );
  const gpsLabelerColors = useMemo(
    () => labelerColorMap(gpsLabelerKeys),
    [gpsLabelerKeys]
  );
  const gpsUserContributionData = useMemo(
    () =>
      gpsUsers.map((u) => ({
        email: u.email,
        label: (u.email || '').split('@')[0] || u.email,
        seconds: u.total_duration_seconds || 0,
        files: u.files || 0,
        sessions: u.sessions || 0,
        dogs: u.dogs || 0,
        human: u.total_duration_human || formatSecondsShort(u.total_duration_seconds),
      })),
    [gpsUsers]
  );
  const gpsByDateChartData = useMemo(
    () =>
      (gps?.by_date || []).map((d) => ({
        date: d.date,
        label: d.date && d.date.length >= 10 ? d.date.slice(5) : d.date,
        seconds: d.duration_seconds || 0,
        sessions: d.sessions || 0,
        files: d.files || 0,
        users: d.users || 0,
        dogs: d.dogs || 0,
        human: d.duration_human || formatSecondsShort(d.duration_seconds),
      })),
    [gps?.by_date]
  );
  const gpsDateLabelerStack = useMemo(
    () => buildDateLabelerStack(gps?.by_date || [], gpsLabelerKeys),
    [gps?.by_date, gpsLabelerKeys]
  );
  const gpsActivityLabelerStack = useMemo(
    () => buildActivityLabelerStack(gpsActivities, gpsUsers, gpsLabelerKeys),
    [gpsActivities, gpsUsers, gpsLabelerKeys]
  );

  const stagingEmails = Object.keys(status?.staging_by_email || {});
  const outputEmails = status?.output_emails || [];
  const unprocessedEmails = stagingEmails.filter((e) => !outputEmails.includes(e));
  const userChartHeight = Math.max(220, userContributionData.length * 48 + 48);
  const gpsUserChartHeight = Math.max(180, gpsUserContributionData.length * 48 + 48);
  const hasGps =
    (gpsTotals.files || 0) > 0 || gpsActivities.length > 0 || (gps?.by_date || []).length > 0;
  const collarCount = useMemo(() => {
    const sns = new Set();
    [...users, ...gpsUsers].forEach((user) => {
      (user.collar_sns || []).forEach((sn) => {
        if (sn) sns.add(sn);
      });
    });
    return sns.size;
  }, [users, gpsUsers]);
  const chartPairClass = hasGps
    ? 'grid grid-cols-1 xl:grid-cols-2 gap-4'
    : 'grid grid-cols-1 gap-4';
  const breadthLabelerCount = useMemo(
    () => new Set([...labelerKeys, ...gpsLabelerKeys]).size,
    [labelerKeys, gpsLabelerKeys]
  );
  const breadthSummary = [
    `${activities.length} posture${activities.length === 1 ? '' : 's'}`,
    hasGps
      ? `${gpsActivities.length} environment${gpsActivities.length === 1 ? '' : 's'}`
      : null,
    `${collarCount} collar${collarCount === 1 ? '' : 's'}`,
    `${breadthLabelerCount} labeler${breadthLabelerCount === 1 ? '' : 's'}`,
  ]
    .filter(Boolean)
    .join(' · ');
  const dogRows = useMemo(() => {
    const list = data?.dogs || [];
    return [...list].sort(
      (a, b) => (b.total_duration_seconds || 0) - (a.total_duration_seconds || 0)
    );
  }, [data?.dogs]);
  const dogChartData = useMemo(
    () =>
      dogRows.slice(0, DOG_CHART_LIMIT).map((dog) => ({
        label: dogAxisLabel(dog),
        name: (dog.name || '').trim() || 'Unnamed',
        breed: dog.breed || '',
        collar_sn: dog.collar_sn,
        seconds: dog.total_duration_seconds || 0,
        sessions: dog.sessions || 0,
        owners: (dog.owners || dog.users || []).join(', '),
        human: dog.total_duration_human || formatSecondsShort(dog.total_duration_seconds),
      })),
    [dogRows]
  );
  const dogChartHeight = Math.max(220, dogChartData.length * 36 + 48);
  const collarCoverage = data?.collar_coverage || null;
  const collarTotals = collarCoverage?.totals || {};
  const azureConfigured = Boolean(status?.collar_sync?.azure_configured);
  const collarUserChart = useMemo(
    () =>
      (collarCoverage?.by_user || []).map((u) => ({
        email: u.email,
        label: shortLabeler(u.email),
        matched: Number(u.matched_seconds) || 0,
        missing: Number(u.missing_seconds) || 0,
        matchedSessions: u.matched_sessions || 0,
        missingSessions: u.missing_sessions || 0,
      })),
    [collarCoverage]
  );
  const collarUserChartHeight = Math.max(180, collarUserChart.length * 48 + 48);
  const clone = status?.collar_sync?.clone || null;
  const azureCheckRunning =
    collarMode === 'check' ||
    (Boolean(syncingCollar) && /Listing Azure/i.test(processInfo?.message || ''));
  const cloneBySn = useMemo(() => {
    const map = {};
    (clone?.by_sn || []).forEach((row) => {
      if (row?.collar_sn) map[row.collar_sn] = row;
    });
    return map;
  }, [clone]);
  const collarPipelineRows = useMemo(() => {
    const rows = [];
    const seen = new Set();
    const inventoryOnly = Boolean(clone?.inventory_only);
    const add = (sn, base) => {
      if (!sn || seen.has(sn)) return;
      seen.add(sn);
      const snap = cloneBySn[sn] || null;
      const azureFiles =
        snap && !(Number(snap.list_errors) > 0) ? Number(snap.azure_files) || 0 : null;
      const s3Files = Number(base?.s3_files ?? snap?.s3_files) || 0;
      const notCloned = snap
        ? inventoryOnly
          ? (Number(snap.copied) || 0) + (Number(snap.errors) || 0)
          : Number(snap.errors) || 0
        : 0;
      const missing = Number(base?.missing) || 0;
      const behind =
        sn !== '_unknown' &&
        (missing > 0 ||
          notCloned > 0 ||
          (azureFiles != null && azureFiles > s3Files));
      rows.push({
        collar_sn: sn,
        sessions: Number(base?.sessions) || 0,
        matched: Number(base?.matched) || 0,
        missing,
        s3_files: s3Files,
        azure_files: azureFiles,
        no_blobs_for_sn: Number(base?.no_blobs_for_sn) || 0,
        time_gap: Number(base?.time_gap) || 0,
        unknown_sn: Number(base?.unknown_sn) || 0,
        bad_timestamp: Number(base?.bad_timestamp) || 0,
        behind,
      });
    };
    (collarCoverage?.by_sn || []).forEach((row) => add(row.collar_sn, row));
    Object.keys(cloneBySn).forEach((sn) => {
      if (!seen.has(sn)) add(sn, {});
    });
    rows.sort(
      (a, b) =>
        b.missing - a.missing ||
        b.sessions - a.sessions ||
        String(a.collar_sn).localeCompare(String(b.collar_sn))
    );
    return rows;
  }, [collarCoverage, clone, cloneBySn]);
  const behindCollarRows = useMemo(
    () => collarPipelineRows.filter((row) => row.behind),
    [collarPipelineRows]
  );
  const missingReasons = collarCoverage?.missing_reasons || {};
  const nextStep = collarNextStep({
    statusLoaded: Boolean(status?.collar_sync),
    statusError,
    azureConfigured,
    clone,
    totals: collarTotals,
    reasons: missingReasons,
  });
  const azureUnreadable = nextStep.kind === 'unreadable' || nextStep.kind === 'not_configured';

  if ((loading || summaryPending) && !data) {
    return (
      <div className="flex items-center justify-center h-full p-8">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 text-blue-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">
            {summaryPending ? 'Building the summary in the background…' : 'Loading labeling data from S3...'}
          </p>
          <p className="text-xs text-gray-400 mt-2">
            {summaryMessage ||
              (summaryPending
                ? 'The site stays up while extracted-txt is scanned. This page updates when the scan finishes.'
                : 'Scanning extracted-txt and summing durations')}
          </p>
        </div>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="flex items-center justify-center h-full p-8">
        <div className="text-center max-w-md">
          <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-2 font-semibold">Error loading labeling data</p>
          <p className="text-gray-600 text-sm mb-4">{error}</p>
          <button
            type="button"
            onClick={() => fetchSummary({ refresh: true })}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col p-6 bg-gray-50 w-full max-w-[1440px] mx-auto" style={{ minHeight: '100vh' }}>
      <div className="flex items-center justify-between mb-6 flex-shrink-0 gap-4">
        <div className="min-w-0">
          <h2 className="text-2xl font-bold text-gray-900">Labeling Data</h2>
          <p className="text-sm text-gray-500 mt-1">
            {generatedAt ? `Updated ${formatUpdatedAt(generatedAt)}` : 'Activity labeling totals'}
            {processInfo?.runtime?.rss_mb != null ? (
              <span
                className={`ml-2 text-xs ${
                  processInfo.runtime.rss_mb >= 2200 ? 'text-amber-700 font-medium' : 'text-gray-400'
                }`}
                title="Resident memory of the web process. A sustained climb during a job is the usual cause of a 503."
              >
                Server {processInfo.runtime.rss_mb} MB
                {processInfo.runtime.peak_rss_mb
                  ? ` · peak ${processInfo.runtime.peak_rss_mb} MB`
                  : ''}
              </span>
            ) : null}
            {loading && data ? (
              <span className="ml-2 inline-flex items-center gap-1 text-xs text-blue-600">
                <RefreshCw className="h-3 w-3 animate-spin" />
                Checking…
              </span>
            ) : summaryPending || stale ? (
              <span className="ml-2 text-xs text-gray-400">Refreshing in background…</span>
            ) : null}
          </p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <button
            type="button"
            onClick={processStaging}
            disabled={processing}
            className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700 disabled:opacity-50"
            title="Adds staging files that are not already in extracted-txt. Does not delete existing output."
          >
            {processing && !syncingCollar ? (
              <RefreshCw className="h-4 w-4 animate-spin" />
            ) : (
              <Play className="h-4 w-4" />
            )}
            {processing && !syncingCollar
              ? processInfo?.job === 'compact-staging'
                ? 'Removing copies…'
                : promoting || processInfo?.job === 'promote-forwards'
                  ? 'Promoting…'
                  : 'Processing…'
              : 'Process staging'}
          </button>
          <button
            type="button"
            onClick={syncCollar}
            disabled={processing || !azureConfigured}
            className="inline-flex items-center gap-2 px-4 py-2 bg-sky-700 text-white rounded-lg text-sm hover:bg-sky-800 disabled:opacity-50"
            title={
              azureConfigured
                ? COLLAR_SYNC_HINT
                : 'Set LABELING_AZURE_SAS_URL (or BLOB_URL + SAS_TOKEN) on the server'
            }
          >
            {syncingCollar ? (
              <RefreshCw className="h-4 w-4 animate-spin" />
            ) : (
              <DownloadCloud className="h-4 w-4" />
            )}
            {syncingCollar ? 'Syncing…' : 'Sync collar data'}
          </button>
          <button
            type="button"
            onClick={() => {
              fetchStatus();
              fetchSummary({ refresh: true });
            }}
            disabled={loading && !data}
            className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>
      </div>

      {error && data ? (
        <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-amber-900">
          Couldn’t refresh summary ({error}). Showing last results.
        </div>
      ) : null}

      {showStagingHealth ? (
        <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-amber-950">
          <div className="font-medium">Staging health</div>
          {stackedTrees ? (
            <p className="mt-1">
              Make is re-uploading each labeler’s full extracted tree. Staging has{' '}
              {stagingHealth.raw_extracted_files} files and about{' '}
              {stagingHealth.unique_files_after_dedupe} are unique ({stagingHealth.duplicate_ratio}×).
              Process staging folds those copies into the charts. It does not stop the next email
              from stacking another tree.
            </p>
          ) : null}
          {chartsBehind ? (
            <p className="mt-2">
              Charts are behind: output has {outputFiles} files and staging has about {uniqueFiles}{' '}
              unique. Process staging to refresh them.
            </p>
          ) : null}
          {incompleteSessions > 0 ? (
            <div className="mt-2">
              <p>
                {incompleteSessions} sessions are missing collar_collected, durations, or
                user_reported in the copy that would be kept. Processing leaves them incomplete.
              </p>
              {(stagingHealth.incomplete_samples || []).length > 0 ? (
                <ul className="mt-1 list-disc pl-5 space-y-0.5 text-xs">
                  {(stagingHealth.incomplete_samples || []).map((sample) => (
                    <li key={`${sample.email}-${sample.timestamp}-${sample.index}-${sample.message_id}`}>
                      {sample.email} · {sample.family} · {sample.timestamp} #{sample.index} · missing{' '}
                      {(sample.missing || []).join(', ') || 'unknown'}
                    </li>
                  ))}
                </ul>
              ) : null}
              {incompleteSessions > (stagingHealth.incomplete_samples || []).length ? (
                <p className="mt-1 text-xs text-amber-900/80">
                  Showing {(stagingHealth.incomplete_samples || []).length} of {incompleteSessions}.
                </p>
              ) : null}
            </div>
          ) : null}
          {sizeMismatchSessions > 0 ? (
            <p className="mt-2">
              {sizeMismatchSessions} sessions have different file sizes across emails. Those copies
              stay in staging until someone inspects them.
            </p>
          ) : null}
          {duplicateRefs > 0 ? (
            <div className="mt-3 flex flex-col sm:flex-row sm:items-center gap-3">
              <button
                type="button"
                onClick={compactStaging}
                disabled={processing}
                className="inline-flex items-center justify-center gap-2 px-3 py-2 bg-white border border-amber-300 rounded-lg text-sm text-amber-950 hover:bg-amber-100 disabled:opacity-50 shrink-0"
              >
                Remove duplicate copies
              </button>
              <p className="text-xs text-amber-900/80">
                Deletes extra extracted files when a newer email already has the same file at the
                same size, and deletes raw zips from batches that added nothing new. Promote already
                skips filenames staging has seen. Make will keep stacking until it uploads only new
                files.
              </p>
            </div>
          ) : null}
        </div>
      ) : null}

      {pendingForwards?.pending_count > 0 && !pendingForwards.auto_promote && !promoting ? (
        <div className="mb-4 p-3 bg-violet-50 border border-violet-200 rounded-lg text-sm text-violet-950 flex flex-col sm:flex-row sm:items-center gap-3">
          <div className="flex-1 min-w-0">
            <div className="font-medium">Forwarded quarantine ready to promote</div>
            <div className="mt-0.5">
              {pendingForwards.pending_count} batch(es) / {pendingForwards.pending_keys} files
              resolved to{' '}
              {(pendingForwards.pending || [])
                .map((b) => b.labeler_email)
                .filter(Boolean)
                .join(', ') || 'labelers'}
              . This is too large to auto-run on page load — promote into staging, then Process
              staging.
            </div>
          </div>
          <button
            type="button"
            onClick={() => promoteForwards()}
            disabled={processing}
            className="inline-flex items-center justify-center gap-2 px-3 py-2 bg-violet-700 text-white rounded-lg text-sm hover:bg-violet-800 disabled:opacity-50 shrink-0"
          >
            <Play className="h-4 w-4" />
            Promote forwards
          </button>
        </div>
      ) : null}

      {(pendingForwards?.unresolved || []).length > 0 ? (
        <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-amber-900">
          {(pendingForwards.unresolved || []).length} forward batch(es) have no recoverable
          original From in meta/body — add <span className="font-mono">Email Body</span> in Make or
          promote via CLI with <span className="font-mono">--map</span>.
        </div>
      ) : null}

      {unprocessedEmails.length > 0 ? (
        <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-amber-900">
          Staging has {unprocessedEmails.length} labeler(s) not in output yet:{' '}
          {unprocessedEmails.join(', ')}. Click <span className="font-medium">Process staging</span> to
          include them in charts.
        </div>
      ) : null}

      {status?.collar_sync && !azureConfigured ? (
        <div className="mb-4 p-3 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-800">
          Collar dump sync is off until the server has{' '}
          <span className="font-mono text-xs">LABELING_AZURE_SAS_URL</span> (or{' '}
          <span className="font-mono text-xs">LABELING_AZURE_BLOB_URL</span> +{' '}
          <span className="font-mono text-xs">LABELING_AZURE_SAS_TOKEN</span>) in{' '}
          <span className="font-mono text-xs">.env</span>. Coverage below still reflects whatever
          is already in <span className="font-mono text-xs">collar-raw/</span>.
        </div>
      ) : null}

      {processing ? (
        <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-900 flex items-start gap-3">
          <RefreshCw className="h-5 w-5 animate-spin flex-shrink-0 mt-0.5" />
          <div className="flex-1 min-w-0">
            <div className="font-medium">
              {syncingCollar || processInfo?.job === 'sync-collar'
                ? azureCheckRunning
                  ? 'Checking Azure'
                  : 'Syncing collar dumps'
                : phaseLabel(processInfo?.progress, processInfo?.job)}
            </div>
            <div className="mt-0.5">
              {processInfo?.progress?.message ||
                processInfo?.message ||
                (promoting
                  ? PROMOTE_PROGRESS
                  : syncingCollar
                    ? azureCheckRunning
                      ? 'Listing Azure ai/ logs for labeled collars…'
                      : COLLAR_SYNC_PROGRESS
                    : 'Copying new staging files into extracted-txt. Existing files stay put.')}
            </div>
            {progressPct != null ? (
              <div className="mt-2">
                <div className="h-1.5 bg-blue-100 rounded">
                  <div
                    className="h-1.5 bg-blue-600 rounded"
                    style={{ width: `${progressPct}%` }}
                  />
                </div>
                <div className="mt-1 text-xs text-blue-800">
                  {progressDone} / {progressTotal}
                </div>
              </div>
            ) : null}
            <div className="mt-1 text-xs text-blue-800">
              {processInfo?.job === 'compact-staging'
                ? 'Staging shrinks in place. Charts stay as they are until you Process staging. '
                : processInfo?.job === 'process'
                  ? 'New files are copied into extracted-txt. Files already there stay put. '
                  : null}
              Safe to close or leave this tab. Started{' '}
              {processInfo?.started_at ? processInfo.started_at.replace('T', ' ').replace('Z', ' UTC') : 'just now'}.
              {processInfo?.runtime?.rss_mb != null
                ? ` Memory ${processInfo.runtime.rss_mb} MB${
                    processInfo.runtime.peak_rss_mb
                      ? ` (peak ${processInfo.runtime.peak_rss_mb} MB)`
                      : ''
                  }.`
                : ''}
            </div>
          </div>
        </div>
      ) : null}

      {!processing && processNotice ? (
        <div
          className={`mb-4 p-4 rounded-lg text-sm flex items-start gap-3 border ${
            processNotice.type === 'success'
              ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
              : processNotice.type === 'error'
                ? 'bg-red-50 border-red-200 text-red-900'
                : 'bg-blue-50 border-blue-200 text-blue-900'
          }`}
        >
          {processNotice.type === 'success' ? (
            <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
          ) : processNotice.type === 'error' ? (
            <AlertCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
          ) : (
            <RefreshCw className="h-5 w-5 flex-shrink-0 mt-0.5" />
          )}
          <div className="flex-1">
            <div>{processNotice.text}</div>
            {processReport &&
            processNotice.type === 'success' &&
            processReport.copied != null &&
            processReport.extracted_duplicates_planned == null ? (
              <div className="mt-1 text-xs opacity-80">
                {processReport.collar_prefix
                  ? `Copied ${processReport.copied || 0} files · listed ${processReport.listed || 0} · ${(processReport.errors || []).length} errors`
                  : (
                    <>
                      Copied {processReport.copied} files · {processReport.sessions} sessions
                      {processReport.skipped_unchanged
                        ? ` · ${processReport.skipped_unchanged} already present`
                        : ''}
                      {processReport.health?.unique_files_after_dedupe != null
                        ? ` · ~${processReport.health.unique_files_after_dedupe} unique after dedupe`
                        : ''}
                      {processReport.incomplete_sessions
                        ? ` · ${processReport.incomplete_sessions} incomplete kept`
                        : ''}
                      {' · '}
                      {(processReport.errors || []).length} errors. Charts match that deduped set.
                    </>
                  )}
              </div>
            ) : null}
            {processReport &&
            processNotice.type === 'success' &&
            processReport.extracted_duplicates_planned != null ? (
              <div className="mt-1 text-xs opacity-80">
                Removed {processReport.extracted_duplicates_removed ?? 0} extracted copies
                {processReport.raw_objects_removed
                  ? ` · ${processReport.raw_objects_removed} raw objects`
                  : ''}
                {' · '}
                {processReport.unique_filenames ?? 0} filenames kept
                {processReport.size_mismatch_copies_kept
                  ? ` · ${processReport.size_mismatch_copies_kept} size mismatches left`
                  : ''}
                . Charts stay unchanged until you Process staging.
              </div>
            ) : null}
          </div>
          <button
            type="button"
            onClick={() => setProcessNotice(null)}
            className="text-xs underline opacity-70 hover:opacity-100"
          >
            Dismiss
          </button>
        </div>
      ) : null}

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-6 items-start">
        <section className="min-w-0">
          <h2 className="text-xl font-semibold text-gray-900">Data pipeline</h2>
          <p className="text-sm text-gray-500 mb-3">
            App labels in staging, whether they are summarized, and whether Azure collar logs for
            those collars are cloned into S3.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 xl:grid-cols-1 gap-px bg-gray-200 border border-gray-200 rounded-lg overflow-hidden mb-4">
            <PipelineStage
              label="App data"
              value={status?.staging_extracted_files ?? 0}
              detail={`${status?.staging_batches ?? 0} batches${
                pendingForwards?.pending_count
                  ? ` · ${pendingForwards.pending_count} forwards waiting`
                  : ''
              }`}
              state={
                unprocessedEmails.length
                  ? 'Ready to summarize'
                  : pendingForwards?.pending_count
                    ? 'Forwards waiting to promote'
                    : 'No new labelers waiting'
              }
              tone={unprocessedEmails.length || pendingForwards?.pending_count ? 'attention' : 'ok'}
            />
            <PipelineStage
              label="Summarized"
              value={status?.output_files ?? totals.files ?? 0}
              detail={
                generatedAt ? `Summary ${formatUpdatedAt(generatedAt)}` : 'Summary not loaded yet'
              }
              state={
                unprocessedEmails.length ? 'Staging not in the summary' : 'Current'
              }
              tone={unprocessedEmails.length ? 'attention' : 'ok'}
            />
            <PipelineStage
              label="Azure"
              value={clone ? clone.azure_files ?? 0 : '—'}
              detail={clone ? 'Labeled collars only' : 'Lists ai/ logs, does not copy'}
              state={
                azureUnreadable && clone
                  ? `Could not read Azure · ${formatUpdatedAt(clone.generated_at)}`
                  : clone?.generated_at
                    ? `Checked ${formatUpdatedAt(clone.generated_at)}`
                    : 'Not checked yet'
              }
              tone={clone && !azureUnreadable ? 'ok' : 'attention'}
              action={
                <button
                  type="button"
                  onClick={checkAzure}
                  disabled={processing || !azureConfigured}
                  className="inline-flex items-center gap-1 text-xs text-blue-700 hover:text-blue-900 disabled:text-gray-400 disabled:cursor-not-allowed"
                  title={
                    azureConfigured
                      ? 'List Azure ai/ logs for labeled collars without copying'
                      : 'Set LABELING_AZURE_SAS_URL on the server'
                  }
                >
                  {azureCheckRunning ? (
                    <RefreshCw className="h-3 w-3 animate-spin" />
                  ) : (
                    <DownloadCloud className="h-3 w-3" />
                  )}
                  {azureCheckRunning ? 'Checking…' : 'Check Azure'}
                </button>
              }
            />
            <PipelineStage
              label="Cloned to S3"
              value={collarTotals.ai_files ?? 0}
              detail={
                !clone
                  ? 'Sync or check Azure to compare'
                  : clone.inventory_only
                    ? `${clone.not_cloned ?? 0} not in S3 · ${clone.skipped_unchanged ?? 0} already there`
                    : `Copied ${clone.copied ?? 0} · ${clone.skipped_unchanged ?? 0} unchanged · ${clone.errors ?? 0} errors`
              }
              state={
                !clone
                  ? 'Not compared to Azure yet'
                  : azureUnreadable
                    ? 'Blocked until Azure can be read'
                    : (clone.not_cloned || 0) === 0
                      ? 'Caught up'
                      : 'Azure has files not in S3'
              }
              tone={!clone || azureUnreadable || (clone.not_cloned || 0) > 0 ? 'attention' : 'ok'}
            />
          </div>
          <CollarNextStep step={nextStep} />
        </section>

        <section className="xl:col-span-2 min-w-0 bg-white border border-gray-200 rounded-lg p-5">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">By collar</h3>
          <p className="text-sm text-gray-500 mb-3">
            Labeled sessions per collar and whether each found a collar log. Collars that are
            behind come first.
          </p>
          <CollarCoverageList
            rows={collarPipelineRows}
            behindCount={behindCollarRows.length}
            showAll={showAllCollars}
            onToggleShowAll={() => setShowAllCollars((v) => !v)}
          />
        </section>
      </div>

      <div className="mb-2">
        <h2 className="text-xl font-semibold text-gray-900">Collar dumps</h2>
        <p className="text-sm text-gray-500">
          Binary <span className="font-mono text-xs">&lt;sn&gt;/ai/*.log</span> from Azure, joined
          to labeled sessions by collar SN + timestamp
          {status?.collar_sync?.last_index_at
            ? ` · last sync ${formatUpdatedAt(status.collar_sync.last_index_at)}`
            : ''}
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <SummaryCard
          icon={CheckCircle2}
          label="Sessions with collar data"
          value={collarTotals.matched ?? 0}
          hint={
            collarTotals.sessions
              ? `${collarTotals.sessions} labeled sessions`
              : 'Run Sync collar data'
          }
        />
        <SummaryCard
          icon={AlertCircle}
          label="Missing dumps"
          value={collarTotals.missing ?? 0}
          hint={
            collarTotals.unknown_sn
              ? `${collarTotals.unknown_sn} with no SN`
              : null
          }
        />
        <SummaryCard
          icon={FolderOpen}
          label="AI files in S3"
          value={collarTotals.ai_files ?? 0}
          hint={collarTotals.sns ? `${collarTotals.sns} collars` : null}
        />
        <SummaryCard
          icon={Clock}
          label="Matched duration"
          value={formatSecondsShort(collarTotals.matched_seconds)}
          hint={
            collarTotals.missing_seconds
              ? `${formatSecondsShort(collarTotals.missing_seconds)} unmatched`
              : null
          }
        />
      </div>

      <div className="bg-white border border-gray-200 rounded-lg p-5 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-1">
          Joined to collar dumps in S3
        </h3>
        <p className="text-sm text-gray-500 mb-3">
          A session matches when its collar has a log in{' '}
          <span className="font-mono text-xs">collar-raw/</span> from around the session time.
          The chart below splits each labeler&apos;s minutes into matched (green) and not
          matched (red).
        </p>
        <CoverageBreakdown totals={collarTotals} reasons={missingReasons} />
        {collarUserChart.length === 0 ? (
          <p className="text-sm text-gray-500">
            No labeled sessions to join yet. Process staging, then Sync collar data.
          </p>
        ) : (
          <>
            <div style={{ height: collarUserChartHeight }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={collarUserChart}
                  layout="vertical"
                  margin={{ top: 8, right: 24, left: 8, bottom: 8 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis
                    type="number"
                    tick={{ fontSize: 12 }}
                    tickFormatter={(v) => formatSecondsShort(v)}
                  />
                  <YAxis type="category" dataKey="label" width={120} tick={{ fontSize: 12 }} />
                  <Tooltip
                    formatter={(value, name, props) => [
                      `${formatSecondsShort(value)} · ${
                        name === 'matched'
                          ? props.payload.matchedSessions
                          : props.payload.missingSessions
                      } sessions`,
                      name === 'matched' ? 'Matched' : 'Missing',
                    ]}
                  />
                  <Legend wrapperStyle={{ fontSize: 12 }} />
                  <Bar dataKey="matched" name="matched" stackId="cov" fill="#34A853" />
                  <Bar dataKey="missing" name="missing" stackId="cov" fill="#EA4335" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <CollapsibleTable label="Show unmatched session samples">
              {(collarCoverage?.unmatched_samples || []).length === 0 ? (
                <p className="text-sm text-gray-500">All labeled sessions have a matching dump.</p>
              ) : (
                <table className="min-w-full text-sm">
                  <thead>
                    <tr className="text-left text-gray-500 border-b">
                      <th className="py-2 pr-4 font-medium">Labeler</th>
                      <th className="py-2 pr-4 font-medium">Family</th>
                      <th className="py-2 pr-4 font-medium">Session</th>
                      <th className="py-2 pr-4 font-medium">Collar SN</th>
                      <th className="py-2 font-medium">Reason</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(collarCoverage?.unmatched_samples || []).map((row, i) => (
                      <tr key={`${row.email}-${row.timestamp}-${i}`} className="border-b border-gray-100">
                        <td className="py-2 pr-4 text-gray-900">{row.email}</td>
                        <td className="py-2 pr-4 text-gray-700">{row.family}</td>
                        <td className="py-2 pr-4 font-mono text-xs text-gray-700">{row.timestamp}</td>
                        <td className="py-2 pr-4 font-mono text-xs text-gray-700">{row.collar_sn}</td>
                        <td className="py-2 text-gray-500">{row.reason}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </CollapsibleTable>
          </>
        )}
      </div>

      <div className={hasGps ? 'grid grid-cols-1 xl:grid-cols-2 gap-6 mb-8' : 'mb-8'}>
        <div>
          <div className="text-base font-semibold text-gray-900">Posture</div>
          <p className="text-sm text-gray-500 mb-3">
            From <span className="font-mono text-xs">activity_session_*</span>
          </p>
          <div className={hasGps ? 'grid grid-cols-2 gap-3' : 'grid grid-cols-2 md:grid-cols-4 gap-4'}>
            <SummaryCard
              icon={Users}
              label="Processed users"
              value={totals.users ?? 0}
              hint={
                stagingEmails.length > (totals.users ?? 0)
                  ? `${stagingEmails.length} in staging`
                  : null
              }
            />
            <SummaryCard icon={Dog} label="Unique dogs" value={totals.dogs ?? 0} />
            <SummaryCard icon={FolderOpen} label="Sessions" value={totals.sessions ?? 0} />
            <SummaryCard icon={FolderOpen} label="Files" value={totals.files ?? 0} />
            <SummaryCard
              icon={Clock}
              label="Labeled duration"
              value={totals.duration_human || formatSecondsShort(totals.duration_seconds)}
            />
          </div>
        </div>
        {hasGps ? (
          <div>
            <div className="text-base font-semibold text-gray-900">Indoor / outdoor</div>
            <p className="text-sm text-gray-500 mb-3">
              From <span className="font-mono text-xs">gps_session_*</span>
            </p>
            <div className="grid grid-cols-2 gap-3">
              <SummaryCard icon={Users} label="GPS labelers" value={gpsTotals.users ?? 0} />
              <SummaryCard icon={Dog} label="GPS dogs" value={gpsTotals.dogs ?? 0} />
              <SummaryCard icon={FolderOpen} label="GPS sessions" value={gpsTotals.sessions ?? 0} />
              <SummaryCard icon={FolderOpen} label="GPS files" value={gpsTotals.files ?? 0} />
              <SummaryCard
                icon={Clock}
                label="GPS duration"
                value={gpsTotals.duration_human || formatSecondsShort(gpsTotals.duration_seconds)}
              />
            </div>
          </div>
        ) : null}
      </div>

      <section className="mb-10">
        <div className="mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Data sync</h2>
          <p className="text-sm text-gray-500 mt-1 max-w-3xl">
            When labeled sessions arrived, and who sent them.
          </p>
        </div>
        <div className={`${chartPairClass} mb-4`}>
          <ChartCard
            kicker="Posture"
            title="By date"
            description="Session-day volume, stacked by labeler"
          >
            <StackedDurationChart
              data={dateLabelerStack}
              seriesKeys={labelerKeys}
              colorMap={labelerColors}
              xKey="label"
              emptyText="No dated sessions found."
            />
            <DateVolumeTable rows={byDateChartData} />
          </ChartCard>
          {hasGps ? (
            <ChartCard
              kicker="Indoor / outdoor"
              title="By date"
              description="Session-day GPS volume, stacked by labeler"
            >
              <StackedDurationChart
                data={gpsDateLabelerStack}
                seriesKeys={gpsLabelerKeys}
                colorMap={gpsLabelerColors}
                xKey="label"
                emptyText="No dated GPS sessions found."
              />
              <DateVolumeTable rows={gpsByDateChartData} />
            </ChartCard>
          ) : null}
        </div>
        <div className={chartPairClass}>
          <ChartCard
            kicker="Posture"
            title="By labeler"
            description="Ranked by labeled duration. Dark bars are distinct dogs (top axis)."
          >
            <LabelerVarietyChart
              data={userContributionData}
              height={userChartHeight}
              colorMap={labelerColors}
              emptyText="No processed users yet. Click Process staging to build extracted-txt from staging."
            />
            <LabelerTable rows={userContributionData} />
          </ChartCard>
          {hasGps ? (
            <ChartCard
              kicker="Indoor / outdoor"
              title="By labeler"
              description="Ranked by GPS labeled duration. Dark bars are distinct dogs (top axis)."
            >
              <LabelerVarietyChart
                data={gpsUserContributionData}
                height={gpsUserChartHeight}
                colorMap={gpsLabelerColors}
                emptyText="No GPS labelers yet."
              />
              <LabelerTable rows={gpsUserContributionData} />
            </ChartCard>
          ) : null}
        </div>
      </section>

      <section className="mb-10">
        <div className="mb-4">
          <h2 className="text-xl font-semibold text-gray-900">How broad the data is</h2>
          <p className="text-sm text-gray-500 mt-1 max-w-3xl">
            Which postures and environments the set actually covers: {breadthSummary}. Each color is a labeler.
          </p>
        </div>
        <div className={chartPairClass}>
          <ChartCard
            kicker="Posture"
            title="By posture"
            description="Each posture, stacked by who labeled it"
          >
            <StackedDurationChart
              data={activityLabelerStack}
              seriesKeys={labelerKeys}
              colorMap={labelerColors}
              xKey="name"
              emptyText="No non-zero activity durations found."
            />
            <ActivityDurationTable rows={activities} labelHeader="Posture" />
          </ChartCard>
          {hasGps ? (
            <ChartCard
              kicker="Indoor / outdoor"
              title="By environment"
              description="Each environment, stacked by who labeled it"
            >
              <StackedDurationChart
                data={gpsActivityLabelerStack}
                seriesKeys={gpsLabelerKeys}
                colorMap={gpsLabelerColors}
                xKey="name"
                emptyText="No non-zero GPS durations found."
              />
              <ActivityDurationTable
                rows={gpsActivities}
                labelHeader="Environment"
                formatName={(row) => displayLabel(row.label)}
              />
            </ChartCard>
          ) : null}
        </div>
        <div className="mt-4">
          <ChartCard
            kicker="Dogs"
            title="Minutes by dog"
            description={`Labeled duration per collar. A few long bars mean minutes are concentrated on those dogs.${
              dogRows.length > DOG_CHART_LIMIT
                ? ` Chart shows the top ${DOG_CHART_LIMIT} of ${dogRows.length}.`
                : ''
            }`}
          >
            {dogChartData.length === 0 ? (
              <p className="text-sm text-gray-500">No dogs found in processed sessions.</p>
            ) : (
              <>
                <div style={{ height: dogChartHeight }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={dogChartData}
                      layout="vertical"
                      margin={{ top: 8, right: 24, left: 8, bottom: 8 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis
                        type="number"
                        tick={{ fontSize: 12 }}
                        tickFormatter={(v) => formatSecondsShort(v)}
                      />
                      <YAxis type="category" dataKey="label" width={140} tick={{ fontSize: 12 }} />
                      <Tooltip
                        formatter={(value, _name, props) => [
                          `${formatSecondsShort(value)} · ${props.payload.sessions} sessions · ${props.payload.owners || 'no owner'}`,
                          props.payload.breed
                            ? `${props.payload.name} · ${props.payload.breed}`
                            : props.payload.name,
                        ]}
                      />
                      <Bar dataKey="seconds" fill="#4285F4" radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <CollapsibleTable label="Show dog table">
                  <table className="min-w-full text-sm">
                    <thead>
                      <tr className="text-left text-gray-500 border-b">
                        <th className="py-2 pr-4 font-medium">Dog</th>
                        <th className="py-2 pr-4 font-medium">Collar SN</th>
                        <th className="py-2 pr-4 font-medium">Breed</th>
                        <th className="py-2 pr-4 font-medium">Owners</th>
                        <th className="py-2 pr-4 font-medium">Sessions</th>
                        <th className="py-2 font-medium">Duration</th>
                      </tr>
                    </thead>
                    <tbody>
                      {dogRows.map((dog) => (
                        <tr key={dog.collar_sn || dog.name} className="border-b border-gray-100">
                          <td className="py-2 pr-4 text-gray-900">{(dog.name || '').trim() || 'Unnamed'}</td>
                          <td className="py-2 pr-4 font-mono text-xs text-gray-700">{dog.collar_sn}</td>
                          <td className="py-2 pr-4 text-gray-500">{dog.breed || '—'}</td>
                          <td className="py-2 pr-4 text-gray-500">
                            {(dog.owners || dog.users || []).join(', ') || '—'}
                          </td>
                          <td className="py-2 pr-4 text-gray-500">{dog.sessions ?? 0}</td>
                          <td className="py-2 text-gray-700">
                            {dog.total_duration_human || formatSecondsShort(dog.total_duration_seconds)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </CollapsibleTable>
              </>
            )}
          </ChartCard>
        </div>
      </section>


      <section>
        <div className="mb-4">
          <h2 className="text-xl font-semibold text-gray-900">By labeler</h2>
          <p className="text-sm text-gray-500 mt-1 max-w-3xl">
            Posture sessions for each person. Expand a row for activities and collar serials.
          </p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-5">
        <div className="space-y-3">
          {users.map((user) => {
            const isOpen = expandedUser === user.email;
            const kinds = user.by_kind || {};
            return (
              <div key={user.email} className="border border-gray-200 rounded-lg overflow-hidden">
                <button
                  type="button"
                  onClick={() => setExpandedUser(isOpen ? null : user.email)}
                  className="w-full flex items-center justify-between gap-4 px-4 py-3 text-left hover:bg-gray-50"
                >
                  <div className="min-w-0">
                    <div className="font-medium text-gray-900 truncate">{user.email}</div>
                    <div className="text-xs text-gray-500 mt-0.5">
                      {user.sessions} sessions · {user.files} files · collars {(user.collar_sns || []).length} ·
                      collar_collected {kinds.collar_collected || 0} ·
                      durations {kinds.durations || 0} · user_reported {kinds.user_reported || 0}
                    </div>
                    {(user.collar_sns || []).length > 0 ? (
                      <div className="text-xs text-gray-400 mt-0.5 truncate">
                        SN: {(user.collar_sns || []).join(', ')}
                      </div>
                    ) : null}
                  </div>
                  <div className="text-right flex-shrink-0">
                    <div className="text-sm font-semibold text-gray-900">
                      {user.total_duration_human || formatSecondsShort(user.total_duration_seconds)}
                    </div>
                    <div className="text-xs text-gray-400">{isOpen ? 'Hide' : 'Show'} activities</div>
                  </div>
                </button>

                {isOpen ? (
                  <div className="px-4 pb-4 border-t border-gray-100 bg-gray-50">
                    {(user.activities || []).length === 0 ? (
                      <p className="text-sm text-gray-500 pt-3">No non-zero durations for this user.</p>
                    ) : (
                      <div className="pt-3 overflow-x-auto">
                        <table className="min-w-full text-sm">
                          <thead>
                            <tr className="text-left text-gray-500 border-b border-gray-200">
                              <th className="py-2 pr-4 font-medium">Activity</th>
                              <th className="py-2 pr-4 font-medium">Duration</th>
                              <th className="py-2 font-medium">Seconds</th>
                            </tr>
                          </thead>
                          <tbody>
                            {user.activities.map((a) => (
                              <tr key={`${user.email}-${a.label}`} className="border-b border-gray-100">
                                <td className="py-2 pr-4 text-gray-900">{a.label}</td>
                                <td className="py-2 pr-4 text-gray-700">{a.human}</td>
                                <td className="py-2 text-gray-500">{a.seconds.toFixed(1)}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}

                    {(user.collars || []).length > 0 ? (
                      <div className="mt-4 space-y-2">
                        <div className="text-xs font-medium text-gray-600 uppercase tracking-wide">
                          By collar SN
                        </div>
                        {user.collars.map((collar) => (
                          <div
                            key={`${user.email}-${collar.collar_sn}`}
                            className="bg-white border border-gray-200 rounded-md px-3 py-2"
                          >
                            <div className="flex items-center justify-between gap-3">
                              <div className="font-mono text-sm text-gray-900">{collar.collar_sn}</div>
                              <div className="text-xs text-gray-500">
                                {collar.sessions} sessions · {collar.files} files ·{' '}
                                {collar.total_duration_human}
                              </div>
                            </div>
                            {(collar.activities || []).length > 0 ? (
                              <div className="mt-1 text-xs text-gray-500">
                                {collar.activities
                                  .map((a) => `${a.name} ${a.human}`)
                                  .join(' · ')}
                              </div>
                            ) : null}
                          </div>
                        ))}
                      </div>
                    ) : null}

                    {Object.keys(user.collar_activity_events || {}).length > 0 ? (
                      <div className="mt-3 text-xs text-gray-500">
                        Collar transitions:{' '}
                        {Object.entries(user.collar_activity_events)
                          .map(([label, count]) => `${label.split(' ')[0]} ${count}`)
                          .join(' · ')}
                      </div>
                    ) : null}
                  </div>
                ) : null}
              </div>
            );
          })}
        </div>
      </div>
      </section>

      <details className="mt-8 group">
        <summary className="cursor-pointer list-none text-xs text-gray-500 hover:text-gray-700 inline-flex items-center gap-1">
          <span className="underline decoration-dotted underline-offset-2">Pipeline & source details</span>
          <span className="text-gray-400 group-open:hidden">▸</span>
          <span className="text-gray-400 hidden group-open:inline">▾</span>
        </summary>
        <div className="mt-3 p-4 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 space-y-2">
          <div>
            <span className="text-gray-500">Source:</span>{' '}
            <span className="font-mono text-xs">
              s3://{data?.bucket}/{data?.prefix}
            </span>
            {cached ? (
              <span className="ml-2 text-xs text-gray-400">
                {stale ? '(stale cache)' : '(cached)'}
              </span>
            ) : null}
          </div>
          {status ? (
            <>
              <div>
                <span className="text-gray-500">Staging:</span>{' '}
                <span className="font-mono">{status.staging_extracted_files ?? 0}</span> extracted
                files in <span className="font-mono">{status.staging_batches ?? 0}</span> Gmail
                batches
                {status.staging_by_family
                  ? ` · activity ${status.staging_by_family.activity || 0} · gps ${status.staging_by_family.gps || 0}`
                  : ''}
                {status.staging_by_email
                  ? ` (${Object.entries(status.staging_by_email)
                      .map(([email, n]) => `${email}: ${n}`)
                      .join(' · ')})`
                  : ''}
              </div>
              <div>
                <span className="text-gray-500">Output:</span>{' '}
                <span className="font-mono">{status.output_files ?? 0}</span> files under{' '}
                <span className="font-mono text-xs">{status.output_prefix}</span>
                {status.output_by_family
                  ? ` · activity ${status.output_by_family.activity || 0} · gps ${status.output_by_family.gps || 0}`
                  : ''}
                {(status.output_emails || []).length
                  ? ` (${status.output_emails.join(', ')})`
                  : ' (empty — click Process staging)'}
              </div>
              {status.staging_health ? (
                <div>
                  Health: ~{status.staging_health.unique_files_after_dedupe} unique /{' '}
                  {status.staging_health.raw_extracted_files} raw
                  {status.staging_health.duplicate_ratio
                    ? ` (${status.staging_health.duplicate_ratio}x)`
                    : ''}
                  {status.staging_health.incomplete_sessions
                    ? ` · incomplete ${status.staging_health.incomplete_sessions}`
                    : ''}
                </div>
              ) : null}
              {status.pending_forwards ? (
                <div>
                  Forwards: {status.pending_forwards.pending_count || 0} pending
                  {status.pending_forwards.already_promoted?.length
                    ? ` · ${status.pending_forwards.already_promoted.length} already promoted`
                    : ''}
                  {status.pending_forwards.unresolved?.length
                    ? ` · ${status.pending_forwards.unresolved.length} unresolved`
                    : ''}
                  {status.forward_batches
                    ? ` · ${status.forward_batches} quarantine batch(es)`
                    : ''}
                </div>
              ) : null}
              {processReport ? (
                <div className="text-xs text-gray-500">
                  {processReport.promoted ? (
                    <>
                      Last promote: {processReport.promoted.length} batch(es), skipped{' '}
                      {(processReport.skipped || []).length}, errors{' '}
                      {(processReport.errors || []).length}
                    </>
                  ) : processReport.extracted_duplicates_planned != null ? (
                    <>
                      Last compact: removed {processReport.extracted_duplicates_removed ?? 0}{' '}
                      extracted copies, raw objects {processReport.raw_objects_removed ?? 0}, kept{' '}
                      {processReport.unique_filenames ?? 0} filenames
                    </>
                  ) : (
                    <>
                      Last process: copied {processReport.copied}, sessions {processReport.sessions},
                      unknown SN {processReport.unknown_sn_sessions}, errors{' '}
                      {(processReport.errors || []).length}
                    </>
                  )}
                </div>
              ) : null}
            </>
          ) : (
            <div className="text-xs text-gray-400">Pipeline status not loaded yet.</div>
          )}
        </div>
      </details>
    </div>
  );
};

function PipelineStage({ label, value, detail, state, tone = 'ok', action }) {
  const stateClass = tone === 'attention' ? 'text-amber-800' : 'text-emerald-800';
  const dotClass = tone === 'attention' ? 'bg-amber-500' : 'bg-emerald-500';
  return (
    <div className="bg-white px-4 py-3 min-w-0">
      <div className="flex items-center justify-between gap-2">
        <span className="text-gray-500 text-xs uppercase tracking-wide">{label}</span>
        {action || null}
      </div>
      <div className="flex items-baseline gap-x-2 flex-wrap mt-0.5">
        <span className="text-xl font-semibold text-gray-900 tabular-nums">{value}</span>
        {state ? (
          <span className={`inline-flex items-center gap-1.5 text-xs ${stateClass}`}>
            <span className={`h-1.5 w-1.5 rounded-full ${dotClass}`} />
            {state}
          </span>
        ) : null}
      </div>
      {detail ? (
        <div className="text-xs text-gray-500 truncate" title={detail}>
          {detail}
        </div>
      ) : null}
    </div>
  );
}

function SummaryCard({ icon: Icon, label, value, hint }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center gap-2 text-gray-500 text-xs uppercase tracking-wide mb-2">
        <Icon className="h-4 w-4" />
        {label}
      </div>
      <div className="text-2xl font-semibold text-gray-900">{value}</div>
      {hint ? <div className="text-xs text-amber-700 mt-1">{hint}</div> : null}
    </div>
  );
}

export default LabelingDataDashboard;
