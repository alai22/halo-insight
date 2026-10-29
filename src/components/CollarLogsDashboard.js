import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { AlertCircle, Download, FolderOpen, RefreshCw } from 'lucide-react';
import axios from 'axios';

const PAGE_SIZE = 40;
const EMPTY_LIST = [];

const KIND_LABELS = {
  collar: 'Collar',
  hand_carry: 'Hand carry',
  on_shelf: 'On shelf',
  other: 'Other',
};

function formatBytes(value) {
  const n = Number(value) || 0;
  if (n < 1024) return `${n} B`;
  const units = ['KB', 'MB', 'GB'];
  let size = n / 1024;
  let unit = units[0];
  for (let i = 1; i < units.length && size >= 1024; i += 1) {
    size /= 1024;
    unit = units[i];
  }
  return `${size >= 10 ? size.toFixed(0) : size.toFixed(1)} ${unit}`;
}

function formatSession(value) {
  if (!value) return '—';
  return String(value).replace('T', ' ').replace('Z', '');
}

function formatCopied(value) {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return formatSession(value);
  return date.toLocaleString();
}

function sessionDay(value) {
  if (!value) return '';
  return String(value).slice(0, 10);
}

function matchesQuery(parts, query) {
  if (!query) return true;
  const haystack = parts.filter(Boolean).join(' ').toLowerCase();
  return haystack.includes(query);
}

const CollarLogsDashboard = () => {
  const [payload, setPayload] = useState(null);
  const [generatedAt, setGeneratedAt] = useState(null);
  const [stale, setStale] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dataset, setDataset] = useState('all');
  const [kind, setKind] = useState('all');
  const [query, setQuery] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [tab, setTab] = useState('files');
  const [page, setPage] = useState(0);
  const [downloading, setDownloading] = useState(null);
  const [downloadError, setDownloadError] = useState(null);

  const fetchIndex = useCallback(async ({ refresh = false } = {}) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/api/labeling/ml-processed', {
        params: refresh ? { refresh: 1 } : {},
      });
      if (!response.data?.success) {
        throw new Error(response.data?.error || 'Failed to load collar logs');
      }
      setPayload(response.data.data);
      setGeneratedAt(response.data.generated_at || null);
      setStale(Boolean(response.data.stale));
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to load collar logs');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchIndex();
  }, [fetchIndex]);

  const sessions = payload?.sessions || EMPTY_LIST;
  const datasets = payload?.datasets || EMPTY_LIST;
  const totals = payload?.totals || {};
  const needle = query.trim().toLowerCase();

  const filteredSessions = useMemo(() => {
    return sessions.filter((row) => {
      if (dataset !== 'all' && row.dataset !== dataset) return false;
      if (kind !== 'all' && row.kind !== kind) return false;
      const day = sessionDay(row.session_at);
      if (dateFrom && day && day < dateFrom) return false;
      if (dateTo && day && day > dateTo) return false;
      if (dateFrom && !day) return false;
      if (dateTo && !day) return false;
      return matchesQuery(
        [row.collar_sn, row.dog_name, row.labeler, row.filename, row.source_log, row.source_zip, row.dataset],
        needle
      );
    });
  }, [sessions, dataset, kind, dateFrom, dateTo, needle]);

  const filteredCollars = useMemo(() => {
    const counts = new Map();
    filteredSessions.forEach((row) => {
      if (row.kind !== 'collar' || !row.collar_sn) return;
      const current = counts.get(row.collar_sn) || {
        collar_sn: row.collar_sn,
        dog_name: row.dog_name,
        labelers: new Set(),
        datasets: new Set(),
        sessions: 0,
        bytes: 0,
        first_session: row.session_at,
        last_session: row.session_at,
      };
      current.sessions += 1;
      current.bytes += row.bytes || 0;
      if (row.dog_name) current.dog_name = row.dog_name;
      if (row.labeler) current.labelers.add(row.labeler);
      if (row.dataset) current.datasets.add(row.dataset);
      if (row.session_at && (!current.first_session || row.session_at < current.first_session)) {
        current.first_session = row.session_at;
      }
      if (row.session_at && (!current.last_session || row.session_at > current.last_session)) {
        current.last_session = row.session_at;
      }
      counts.set(row.collar_sn, current);
    });
    return Array.from(counts.values())
      .map((row) => ({
        ...row,
        labelers: Array.from(row.labelers).sort(),
        datasets: Array.from(row.datasets).sort(),
      }))
      .sort((a, b) => b.sessions - a.sessions || a.collar_sn.localeCompare(b.collar_sn));
  }, [filteredSessions]);

  const filteredMissing = useMemo(() => {
    const rows = payload?.missing?.sessions || [];
    return rows.filter((row) => {
      const day = sessionDay(row.start);
      if (dateFrom && day && day < dateFrom) return false;
      if (dateTo && day && day > dateTo) return false;
      return matchesQuery(
        [row.collar_sn, row.dog_name, row.labeler, row.session, row.near_miss_log],
        needle
      );
    });
  }, [payload, dateFrom, dateTo, needle]);

  const pageCount = Math.max(1, Math.ceil(filteredSessions.length / PAGE_SIZE));
  const safePage = Math.min(page, pageCount - 1);
  const pageRows = filteredSessions.slice(safePage * PAGE_SIZE, safePage * PAGE_SIZE + PAGE_SIZE);

  useEffect(() => {
    setPage(0);
  }, [dataset, kind, query, dateFrom, dateTo]);

  const downloadFile = async (key) => {
    if (!key) return;
    setDownloading(key);
    setDownloadError(null);
    try {
      const response = await axios.get('/api/labeling/ml-processed/download', { params: { key } });
      const url = response.data?.url;
      if (!url) throw new Error(response.data?.error || 'No download URL');
      const opened = window.open(url, '_blank', 'noopener,noreferrer');
      if (!opened) window.location.assign(url);
    } catch (err) {
      setDownloadError(err.response?.data?.error || err.message || 'Download failed');
    } finally {
      setDownloading(null);
    }
  };

  if (loading && !payload) {
    return (
      <div className="flex items-center justify-center h-full p-8">
        <div className="text-center max-w-md">
          <RefreshCw className="h-8 w-8 text-blue-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading collar logs from S3…</p>
          <p className="text-xs text-gray-400 mt-2">
            The first scan reads each log’s JSON sidecar. Later visits use a cached index.
          </p>
        </div>
      </div>
    );
  }

  if (error && !payload) {
    return (
      <div className="flex items-center justify-center h-full p-8">
        <div className="text-center max-w-md">
          <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-2 font-semibold">Error loading collar logs</p>
          <p className="text-gray-600 text-sm mb-4">{error}</p>
          <button
            type="button"
            onClick={() => fetchIndex({ refresh: true })}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col p-6 bg-gray-50" style={{ minHeight: '100vh' }}>
      <div className="flex items-start justify-between mb-6 gap-4">
        <div className="min-w-0">
          <h2 className="text-2xl font-bold text-gray-900">Collar logs</h2>
          <p className="text-sm text-gray-500 mt-1">
            Files copied into{' '}
            <span className="font-mono text-xs">
              s3://{payload?.bucket}/{payload?.prefix}
            </span>
            . Each processing folder is listed separately, so one log in all three datasets counts three times.
            {generatedAt ? ` · updated ${formatCopied(generatedAt)}` : ''}
            {loading && payload ? (
              <span className="ml-2 inline-flex items-center gap-1 text-xs text-blue-600">
                <RefreshCw className="h-3 w-3 animate-spin" />
                Refreshing…
              </span>
            ) : stale ? (
              <span className="ml-2 text-xs text-gray-400">Refreshing in background…</span>
            ) : null}
          </p>
        </div>
        <button
          type="button"
          onClick={() => fetchIndex({ refresh: true })}
          disabled={loading}
          className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50 disabled:opacity-50 shrink-0"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {error && payload ? (
        <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-amber-900">
          Couldn’t refresh the index ({error}). Showing the last results.
        </div>
      ) : null}
      {downloadError ? (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
          {downloadError}
        </div>
      ) : null}

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
        <SummaryCard label="Sessions" value={totals.sessions ?? 0} hint={`${totals.collar_sessions ?? 0} collar · ${totals.bench_sessions ?? 0} bench`} />
        <SummaryCard label="Collars" value={totals.collars ?? 0} />
        <SummaryCard label="Copied size" value={formatBytes(totals.bytes)} />
        <SummaryCard
          label="Missing sessions"
          value={totals.missing_sessions ?? 0}
          hint={totals.missing_collars ? `${totals.missing_collars} collars in the gap report` : null}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
        {datasets.map((row) => {
          const active = dataset === row.id;
          return (
            <button
              key={row.id}
              type="button"
              onClick={() => setDataset(active ? 'all' : row.id)}
              className={`text-left p-4 rounded-lg border transition-colors ${
                active ? 'bg-emerald-50 border-emerald-300' : 'bg-white border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center gap-2 text-xs uppercase tracking-wide text-gray-500 mb-1">
                <FolderOpen className="h-3.5 w-3.5" />
                Dataset
              </div>
              <div className="font-mono text-sm text-gray-900 break-all">{row.id}</div>
              <div className="mt-2 text-sm text-gray-600">
                {row.collar_sessions} collar sessions · {row.collars} collars
                {row.bench_sessions ? ` · ${row.bench_sessions} bench` : ''}
              </div>
              <div className="mt-1 text-xs text-gray-500">
                {row.session_date_min || '—'} → {row.session_date_max || '—'} · {formatBytes(row.bytes)}
                {row.unparsed ? ` · ${row.unparsed} unrecognized` : ''}
              </div>
            </button>
          );
        })}
      </div>

      <div className="bg-white border border-gray-200 rounded-lg p-4 mb-4">
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-3">
          <label className="text-xs text-gray-500">
            Dataset
            <select
              value={dataset}
              onChange={(e) => setDataset(e.target.value)}
              className="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-900"
            >
              <option value="all">All datasets</option>
              {datasets.map((row) => (
                <option key={row.id} value={row.id}>
                  {row.id}
                </option>
              ))}
            </select>
          </label>
          <label className="text-xs text-gray-500">
            Kind
            <select
              value={kind}
              onChange={(e) => setKind(e.target.value)}
              className="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-900"
            >
              <option value="all">All kinds</option>
              {Object.entries(KIND_LABELS).map(([id, label]) => (
                <option key={id} value={id}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label className="text-xs text-gray-500">
            From
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-900"
            />
          </label>
          <label className="text-xs text-gray-500">
            To
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-900"
            />
          </label>
          <label className="text-xs text-gray-500">
            Search
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Collar, dog, labeler, file"
              className="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-900"
            />
          </label>
        </div>
      </div>

      <div className="flex items-center gap-2 mb-3">
        {[
          ['files', `Files (${filteredSessions.length})`],
          ['collars', `Collars (${filteredCollars.length})`],
          ['gaps', `Not copied (${filteredMissing.length})`],
        ].map(([id, label]) => (
          <button
            key={id}
            type="button"
            onClick={() => setTab(id)}
            className={`px-3 py-1.5 rounded-lg text-sm ${
              tab === id ? 'bg-gray-900 text-white' : 'bg-white border border-gray-300 text-gray-700'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {tab === 'files' ? (
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-500">
                <tr>
                  <th className="px-3 py-2 font-medium">Session</th>
                  <th className="px-3 py-2 font-medium">Collar</th>
                  <th className="px-3 py-2 font-medium">Dog</th>
                  <th className="px-3 py-2 font-medium">Labeler</th>
                  <th className="px-3 py-2 font-medium">Dataset</th>
                  <th className="px-3 py-2 font-medium">Size</th>
                  <th className="px-3 py-2 font-medium">Copied</th>
                  <th className="px-3 py-2 font-medium">File</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {pageRows.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-3 py-8 text-center text-gray-500">
                      No files match these filters.
                    </td>
                  </tr>
                ) : (
                  pageRows.map((row) => (
                    <tr key={`${row.dataset}-${row.filename}`} className="align-top">
                      <td className="px-3 py-2 whitespace-nowrap">
                        <div>{formatSession(row.session_at)}</div>
                        <div className="text-xs text-gray-400">{KIND_LABELS[row.kind] || row.kind}</div>
                      </td>
                      <td className="px-3 py-2 font-mono text-xs whitespace-nowrap">{row.collar_sn || '—'}</td>
                      <td className="px-3 py-2 whitespace-nowrap">{row.dog_name || '—'}</td>
                      <td className="px-3 py-2 text-xs">{row.labeler || '—'}</td>
                      <td className="px-3 py-2 font-mono text-xs">{row.dataset}</td>
                      <td className="px-3 py-2 whitespace-nowrap">{formatBytes(row.bytes)}</td>
                      <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-500">
                        {formatCopied(row.last_modified)}
                      </td>
                      <td className="px-3 py-2">
                        <div className="font-mono text-xs text-gray-700 break-all max-w-xs">{row.filename}</div>
                        {row.source_zip ? (
                          <div className="text-xs text-gray-400 mt-0.5">{row.source_zip}</div>
                        ) : null}
                        <div className="mt-1 flex gap-2">
                          <DownloadButton
                            label="CSV"
                            busy={downloading === row.csv_key}
                            disabled={!row.csv_key || Boolean(downloading)}
                            onClick={() => downloadFile(row.csv_key)}
                          />
                          <DownloadButton
                            label="JSON"
                            busy={downloading === row.json_key}
                            disabled={!row.json_key || Boolean(downloading)}
                            onClick={() => downloadFile(row.json_key)}
                          />
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          <div className="flex items-center justify-between px-3 py-2 border-t border-gray-100 text-xs text-gray-500">
            <span>
              {filteredSessions.length === 0
                ? '0 files'
                : `${safePage * PAGE_SIZE + 1}–${Math.min(filteredSessions.length, (safePage + 1) * PAGE_SIZE)} of ${filteredSessions.length}`}
            </span>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={safePage === 0}
                onClick={() => setPage(safePage - 1)}
                className="px-2 py-1 border border-gray-300 rounded disabled:opacity-40"
              >
                Previous
              </button>
              <button
                type="button"
                disabled={safePage >= pageCount - 1}
                onClick={() => setPage(safePage + 1)}
                className="px-2 py-1 border border-gray-300 rounded disabled:opacity-40"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      ) : null}

      {tab === 'collars' ? (
        <div className="bg-white border border-gray-200 rounded-lg overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-500">
              <tr>
                <th className="px-3 py-2 font-medium">Collar</th>
                <th className="px-3 py-2 font-medium">Dog</th>
                <th className="px-3 py-2 font-medium">Sessions</th>
                <th className="px-3 py-2 font-medium">Size</th>
                <th className="px-3 py-2 font-medium">First</th>
                <th className="px-3 py-2 font-medium">Last</th>
                <th className="px-3 py-2 font-medium">Labelers</th>
                <th className="px-3 py-2 font-medium">Datasets</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredCollars.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-3 py-8 text-center text-gray-500">
                    No collars match these filters.
                  </td>
                </tr>
              ) : (
                filteredCollars.map((row) => (
                  <tr key={row.collar_sn}>
                    <td className="px-3 py-2 font-mono text-xs">{row.collar_sn}</td>
                    <td className="px-3 py-2">{row.dog_name || '—'}</td>
                    <td className="px-3 py-2">{row.sessions}</td>
                    <td className="px-3 py-2">{formatBytes(row.bytes)}</td>
                    <td className="px-3 py-2 whitespace-nowrap text-xs">{formatSession(row.first_session)}</td>
                    <td className="px-3 py-2 whitespace-nowrap text-xs">{formatSession(row.last_session)}</td>
                    <td className="px-3 py-2 text-xs">{(row.labelers || []).join(', ') || '—'}</td>
                    <td className="px-3 py-2 font-mono text-xs">{(row.datasets || []).join(', ')}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      ) : null}

      {tab === 'gaps' ? (
        <div className="space-y-4">
          <p className="text-sm text-gray-500">
            Labeled sessions that do not have a matching copied log. This comes from{' '}
            <span className="font-mono text-xs">ml-processed/missing-collar-logs/</span>.
          </p>
          {(payload?.missing?.by_collar || []).length > 0 ? (
            <div className="bg-white border border-gray-200 rounded-lg overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-500">
                  <tr>
                    <th className="px-3 py-2 font-medium">Collar</th>
                    <th className="px-3 py-2 font-medium">Dog</th>
                    <th className="px-3 py-2 font-medium">Missing sessions</th>
                    <th className="px-3 py-2 font-medium">Minutes</th>
                    <th className="px-3 py-2 font-medium">Range</th>
                    <th className="px-3 py-2 font-medium">Labelers</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {payload.missing.by_collar.map((row) => (
                    <tr key={row.collar_sn}>
                      <td className="px-3 py-2 font-mono text-xs">{row.collar_sn}</td>
                      <td className="px-3 py-2">{row.dog_name || '—'}</td>
                      <td className="px-3 py-2">{row.sessions ?? '—'}</td>
                      <td className="px-3 py-2">{row.minutes ?? '—'}</td>
                      <td className="px-3 py-2 text-xs whitespace-nowrap">
                        {formatSession(row.first)} → {formatSession(row.last)}
                      </td>
                      <td className="px-3 py-2 text-xs">{row.labelers || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : null}
          <div className="bg-white border border-gray-200 rounded-lg overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-500">
                <tr>
                  <th className="px-3 py-2 font-medium">Start</th>
                  <th className="px-3 py-2 font-medium">Collar</th>
                  <th className="px-3 py-2 font-medium">Dog</th>
                  <th className="px-3 py-2 font-medium">Labeler</th>
                  <th className="px-3 py-2 font-medium">Minutes</th>
                  <th className="px-3 py-2 font-medium">Session</th>
                  <th className="px-3 py-2 font-medium">Near miss</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {filteredMissing.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-3 py-8 text-center text-gray-500">
                      No missing sessions match these filters.
                    </td>
                  </tr>
                ) : (
                  filteredMissing.map((row) => (
                    <tr key={`${row.collar_sn}-${row.session}-${row.start}`}>
                      <td className="px-3 py-2 whitespace-nowrap text-xs">{formatSession(row.start)}</td>
                      <td className="px-3 py-2 font-mono text-xs">{row.collar_sn}</td>
                      <td className="px-3 py-2">{row.dog_name || '—'}</td>
                      <td className="px-3 py-2 text-xs">{row.labeler || '—'}</td>
                      <td className="px-3 py-2">{row.minutes ?? '—'}</td>
                      <td className="px-3 py-2 font-mono text-xs">{row.session}</td>
                      <td className="px-3 py-2 text-xs text-gray-500">
                        {row.near_miss_log || '—'}
                        {row.near_miss_seconds != null && row.near_miss_seconds !== ''
                          ? ` (${row.near_miss_seconds}s)`
                          : ''}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      ) : null}

      {(payload?.unparsed || []).length > 0 ? (
        <details className="mt-4 text-sm text-gray-600">
          <summary className="cursor-pointer text-gray-500">
            {payload.unparsed.length} file{payload.unparsed.length === 1 ? '' : 's'} with unrecognized names
          </summary>
          <ul className="mt-2 font-mono text-xs space-y-1">
            {payload.unparsed.map((row) => (
              <li key={row.key}>
                {row.dataset}/{row.filename}
              </li>
            ))}
          </ul>
        </details>
      ) : null}
    </div>
  );
};

function SummaryCard({ label, value, hint }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="text-gray-500 text-xs uppercase tracking-wide mb-2">{label}</div>
      <div className="text-2xl font-semibold text-gray-900">{value}</div>
      {hint ? <div className="text-xs text-gray-500 mt-1">{hint}</div> : null}
    </div>
  );
}

function DownloadButton({ label, busy, disabled, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="inline-flex items-center gap-1 text-xs text-blue-700 hover:text-blue-900 disabled:opacity-40"
    >
      <Download className="h-3 w-3" />
      {busy ? '…' : label}
    </button>
  );
}

export default CollarLogsDashboard;
