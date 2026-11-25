import React, { useEffect, useMemo, useState } from 'react';
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { ChevronLeft, RefreshCw } from 'lucide-react';
import axios from 'axios';

const LABEL_COLORS = [
  '#4285F4', '#EA4335', '#FBBC04', '#34A853', '#FF6D01', '#9334E6', '#00ACC1', '#64B5F6',
  '#F28B82', '#81C784', '#FFB74D', '#BA68C8', '#1A237E', '#AD1457', '#827717', '#00695C',
  '#5D4037', '#546E7A', '#F06292', '#7CB342',
];

function dayOffset(days) {
  const d = new Date();
  d.setDate(d.getDate() - days);
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

const PRESETS = [
  { key: 'all', label: 'All time', start: () => '', end: () => '' },
  { key: '7', label: 'Last 7 days', start: () => dayOffset(6), end: () => dayOffset(0) },
  { key: '14', label: 'Last 14 days', start: () => dayOffset(13), end: () => dayOffset(0) },
  { key: '30', label: 'Last 30 days', start: () => dayOffset(29), end: () => dayOffset(0) },
];

function fmtMin(minutes) {
  const m = Number(minutes) || 0;
  if (m === 0) return '0';
  return m < 10 ? m.toFixed(1) : String(Math.round(m));
}

function fmtDay(day) {
  if (!day) return '—';
  const d = new Date(`${day}T00:00:00`);
  return Number.isNaN(d.getTime()) ? day : d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
}

function usePartnerGet(path, params, enabled = true) {
  const [state, setState] = useState({ loading: enabled, data: null, error: null });
  const key = JSON.stringify([path, params]);
  useEffect(() => {
    if (!enabled) return undefined;
    let cancelled = false;
    setState((s) => ({ ...s, loading: true, error: null }));
    const clean = Object.fromEntries(Object.entries(params).filter(([, v]) => v));
    axios
      .get(path, { params: clean, withCredentials: true })
      .then((r) => !cancelled && setState({ loading: false, data: r.data, error: null }))
      .catch(
        (err) =>
          !cancelled &&
          setState({ loading: false, data: null, error: err.response?.data?.error || err.message || 'Could not load' })
      );
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, enabled]);
  return state;
}

/**
 * Labeling progress for a partner's own participants (e.g. Treat Therapeutics).
 * previewOrg: a Halo admin viewing what that partner sees.
 */
export default function PartnerDashboard({ previewOrg = null }) {
  const [presetKey, setPresetKey] = useState('all');
  const [selected, setSelected] = useState(null);
  const preset = PRESETS.find((p) => p.key === presetKey) || PRESETS[0];
  const params = { start: preset.start(), end: preset.end(), org: previewOrg || '' };
  const list = usePartnerGet('/api/partner/v1/participants', params);
  const body = list.data;
  const participants = body?.participants || [];
  const labels = body?.labels || [];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-6">
      <div className="flex flex-wrap items-end justify-between gap-3 mb-5">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            {body?.organization ? `${body.organization} participants` : 'Participants'}
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Labeled minutes for each participant, against {body?.target_minutes_per_label ?? 3} minutes per label.
            {body?.data_as_of ? ` Data as of ${new Date(body.data_as_of).toLocaleString()}.` : ''}
          </p>
        </div>
        <div className="inline-flex rounded-md border border-gray-200 overflow-hidden text-sm">
          {PRESETS.map((p) => (
            <button
              key={p.key}
              type="button"
              onClick={() => setPresetKey(p.key)}
              className={`px-3 py-1.5 ${presetKey === p.key ? 'bg-gray-900 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'}`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {list.error ? <p className="text-sm text-red-600 mb-4">{list.error}</p> : null}
      {list.loading && !body ? (
        <p className="text-sm text-gray-500 inline-flex items-center gap-2">
          <RefreshCw className="h-4 w-4 animate-spin" /> Loading…
        </p>
      ) : null}

      {selected ? (
        <ParticipantDetail
          person={participants.find((p) => p.email === selected) || { email: selected, labels: {} }}
          labels={labels}
          params={params}
          onBack={() => setSelected(null)}
        />
      ) : body ? (
        <ParticipantTable rows={participants} onOpen={setSelected} />
      ) : null}
    </div>
  );
}

function ParticipantTable({ rows, onOpen }) {
  if (!rows.length) {
    return <p className="text-sm text-gray-500">No participants are listed yet. Ask Halo to add them.</p>;
  }
  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="text-left text-gray-500 border-b border-gray-200">
            <th className="py-2.5 px-4 font-medium">Participant</th>
            <th className="py-2.5 pr-4 font-medium">Dog</th>
            <th className="py-2.5 pr-4 font-medium text-right">Minutes</th>
            <th className="py-2.5 pr-4 font-medium text-right">Sessions</th>
            <th className="py-2.5 pr-4 font-medium">Labels at target</th>
            <th className="py-2.5 pr-4 font-medium">Last contribution</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((p) => (
            <tr
              key={p.email}
              onClick={() => onOpen(p.email)}
              className="border-b border-gray-100 last:border-0 hover:bg-gray-50 cursor-pointer"
            >
              <td className="py-2.5 px-4">
                <div className="text-gray-900 font-medium">{p.name || p.email}</div>
                {p.name ? <div className="text-xs text-gray-500">{p.email}</div> : null}
              </td>
              <td className="py-2.5 pr-4 text-gray-700">{p.dogs.join(', ') || '—'}</td>
              <td className="py-2.5 pr-4 text-right tabular-nums">{fmtMin(p.minutes)}</td>
              <td className="py-2.5 pr-4 text-right tabular-nums">{p.sessions}</td>
              <td className="py-2.5 pr-4">
                <div className="flex items-center gap-2">
                  <div className="w-24 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-green-500"
                      style={{ width: `${(p.labels_done / Math.max(1, p.labels_total)) * 100}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-600 tabular-nums">
                    {p.labels_done}/{p.labels_total}
                  </span>
                </div>
              </td>
              <td className="py-2.5 pr-4 text-gray-700 whitespace-nowrap">{fmtDay(p.last_contribution)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ParticipantDetail({ person, labels, params, onBack }) {
  const path = `/api/partner/v1/participants/${encodeURIComponent(person.email)}`;
  const daily = usePartnerGet(`${path}/daily`, params);
  const sessions = usePartnerGet(`${path}/sessions`, params);
  const names = useMemo(() => Object.fromEntries(labels.map((l) => [l.key, l.name])), [labels]);
  const [limit, setLimit] = useState(50);

  const chart = useMemo(() => {
    const days = daily.data?.days || [];
    const totals = {};
    days.forEach((d) => Object.entries(d.labels).forEach(([k, v]) => (totals[k] = (totals[k] || 0) + v)));
    const keys = Object.keys(totals).sort((a, b) => totals[b] - totals[a]);
    const rows = days.map((d) => ({ day: d.date.slice(5), ...Object.fromEntries(keys.map((k) => [k, d.labels[k] || 0])) }));
    return { keys, rows };
  }, [daily.data]);

  const groups = [
    { key: 'posture', title: 'Postures' },
    { key: 'environment', title: 'Environments' },
  ];
  const rows = sessions.data?.sessions || [];

  return (
    <div className="space-y-6">
      <div>
        <button type="button" onClick={onBack} className="inline-flex items-center gap-1 text-sm text-blue-700 hover:text-blue-900">
          <ChevronLeft className="h-4 w-4" /> All participants
        </button>
        <h2 className="text-xl font-semibold text-gray-900 mt-2">{person.name || person.email}</h2>
        <p className="text-sm text-gray-500">
          {person.name ? `${person.email} · ` : ''}
          {fmtMin(person.minutes)} min · {person.sessions ?? 0} sessions · {person.labels_done ?? 0}/
          {person.labels_total ?? labels.length} labels at target
          {person.dogs?.length ? ` · 🐶 ${person.dogs.join(', ')}` : ''}
        </p>
      </div>

      <section className="bg-white border border-gray-200 rounded-lg p-5">
        <h3 className="font-semibold text-gray-900 mb-3">Minutes by label</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {groups.map((g) => (
            <table key={g.key} className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="py-1.5 font-medium">{g.title}</th>
                  <th className="py-1.5 font-medium text-right">Have</th>
                  <th className="py-1.5 font-medium text-right">Still need</th>
                </tr>
              </thead>
              <tbody>
                {labels
                  .filter((l) => l.group === g.key)
                  .map((l) => {
                    const v = person.labels?.[l.key] || { minutes: 0, remaining_minutes: 3, done: false };
                    return (
                      <tr key={l.key} className="border-b border-gray-100 last:border-0">
                        <td className="py-1.5 text-gray-900">{l.name}</td>
                        <td className="py-1.5 text-right tabular-nums">{fmtMin(v.minutes)}</td>
                        <td className={`py-1.5 text-right tabular-nums ${v.done ? 'text-green-700' : 'text-amber-700'}`}>
                          {v.done ? '✓ Done' : fmtMin(v.remaining_minutes)}
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>
          ))}
        </div>
        {Object.keys(person.other_labels || {}).length ? (
          <p className="text-xs text-gray-500 mt-3">
            Other labels:{' '}
            {Object.entries(person.other_labels)
              .map(([k, v]) => `${k} ${fmtMin(v)} min`)
              .join(' · ')}
          </p>
        ) : null}
      </section>

      <section className="bg-white border border-gray-200 rounded-lg p-5">
        <h3 className="font-semibold text-gray-900 mb-3">Minutes by day</h3>
        {daily.loading ? (
          <p className="text-sm text-gray-500">Loading…</p>
        ) : daily.error ? (
          <p className="text-sm text-red-600">{daily.error}</p>
        ) : !chart.rows.length ? (
          <p className="text-sm text-gray-500">No contributions in this range.</p>
        ) : (
          <div style={{ height: 360 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chart.rows} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="day" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 12 }} label={{ value: 'min', angle: -90, position: 'insideLeft', fontSize: 12 }} />
                <Tooltip formatter={(v, name) => [`${fmtMin(v)} min`, name]} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                {chart.keys.map((k, i) => (
                  <Bar key={k} dataKey={k} name={names[k] || k} stackId="d" fill={LABEL_COLORS[i % LABEL_COLORS.length]} />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </section>

      <section className="bg-white border border-gray-200 rounded-lg p-5">
        <h3 className="font-semibold text-gray-900 mb-3">Sessions</h3>
        {sessions.loading ? (
          <p className="text-sm text-gray-500">Loading…</p>
        ) : sessions.error ? (
          <p className="text-sm text-red-600">{sessions.error}</p>
        ) : !rows.length ? (
          <p className="text-sm text-gray-500">No sessions in this range.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="py-2 pr-4 font-medium">When</th>
                  <th className="py-2 pr-4 font-medium">Type</th>
                  <th className="py-2 pr-4 font-medium">Dog</th>
                  <th className="py-2 pr-4 font-medium text-right">Minutes</th>
                  <th className="py-2 font-medium">Labels</th>
                </tr>
              </thead>
              <tbody>
                {rows.slice(0, limit).map((s) => (
                  <tr key={`${s.model}-${s.session_id}`} className="border-b border-gray-100 align-top">
                    <td className="py-2 pr-4 whitespace-nowrap">
                      {s.started_at ? new Date(s.started_at).toLocaleString() : '—'}
                    </td>
                    <td className="py-2 pr-4 text-gray-600">{s.model === 'activity' ? 'Postures' : 'Indoor/outdoor'}</td>
                    <td className="py-2 pr-4 text-gray-700">{s.dog || '—'}</td>
                    <td className="py-2 pr-4 text-right tabular-nums">{fmtMin(s.minutes)}</td>
                    <td className="py-2 text-gray-500">
                      {Object.entries(s.labels)
                        .map(([k, v]) => `${names[k] || k} ${fmtMin(v)}`)
                        .join(' · ') || '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {rows.length > limit ? (
              <button type="button" onClick={() => setLimit((n) => n + 50)} className="mt-3 text-sm text-blue-700">
                Show more ({rows.length - limit} left)
              </button>
            ) : null}
          </div>
        )}
      </section>
    </div>
  );
}
