import React, { useCallback, useEffect, useState } from 'react';
import { Copy, KeyRound, Trash2 } from 'lucide-react';
import axios from 'axios';
import PartnerDashboard from './PartnerDashboard';

const toLines = (list) => (list || []).join('\n');
const fromLines = (text) =>
  String(text || '')
    .split(/[\s,;]+/)
    .map((s) => s.trim())
    .filter(Boolean);

/** Halo admins: who each partner can see, who can log in, and API keys. */
export default function PartnersAdmin() {
  const [config, setConfig] = useState(null);
  const [error, setError] = useState(null);

  const load = useCallback(() => {
    axios
      .get('/api/labeling/partners', { withCredentials: true })
      .then((r) => setConfig(r.data))
      .catch((err) => setError(err.response?.data?.error || err.message));
  }, []);
  useEffect(load, [load]);

  if (error) return <p className="text-sm text-red-600">{error}</p>;
  if (!config) return <p className="text-sm text-gray-500">Loading partners…</p>;
  return (
    <div className="space-y-10">
      {Object.entries(config.orgs || {}).map(([org, cfg]) => (
        <PartnerOrg key={org} org={org} cfg={cfg} onChange={setConfig} />
      ))}
    </div>
  );
}

function PartnerOrg({ org, cfg, onChange }) {
  const [participants, setParticipants] = useState(toLines(cfg.participants));
  const [logins, setLogins] = useState(toLines(cfg.logins));
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);
  const [newKey, setNewKey] = useState(null);
  const [keyLabel, setKeyLabel] = useState('');
  const [previewKey, setPreviewKey] = useState(0);

  useEffect(() => {
    setParticipants(toLines(cfg.participants));
    setLogins(toLines(cfg.logins));
  }, [cfg.participants, cfg.logins]);

  const dirty = toLines(fromLines(participants)) !== toLines(cfg.participants) || toLines(fromLines(logins)) !== toLines(cfg.logins);

  const save = () => {
    setSaving(true);
    setMessage(null);
    axios
      .put(`/api/labeling/partners/${org}`, { participants: fromLines(participants), logins: fromLines(logins) }, { withCredentials: true })
      .then((r) => {
        onChange(r.data);
        setMessage({ ok: true, text: 'Saved.' });
        setPreviewKey((n) => n + 1);
      })
      .catch((err) => setMessage({ ok: false, text: err.response?.data?.error || err.message }))
      .finally(() => setSaving(false));
  };

  const createKey = () => {
    axios
      .post(`/api/labeling/partners/${org}/keys`, { label: keyLabel }, { withCredentials: true })
      .then((r) => {
        setNewKey(r.data.key);
        setKeyLabel('');
        onChange(r.data);
      })
      .catch((err) => setMessage({ ok: false, text: err.response?.data?.error || err.message }));
  };

  const revoke = (key) => {
    if (!window.confirm(`Revoke the key ending ${key.last4}? Anything using it stops working at once.`)) return;
    axios
      .delete(`/api/labeling/partners/${org}/keys/${key.id}`, { withCredentials: true })
      .then((r) => onChange(r.data))
      .catch((err) => setMessage({ ok: false, text: err.response?.data?.error || err.message }));
  };

  const box = 'w-full h-40 px-3 py-2 text-sm font-mono border border-gray-300 rounded-md';
  return (
    <section>
      <h2 className="text-lg font-semibold text-gray-900">{cfg.name}</h2>
      <p className="text-sm text-gray-500 mt-1 max-w-3xl">
        {cfg.name} sees labeling only from the participant emails listed here, never anyone else's. Staff
        logins get a login link by email and see the page below; API keys give their systems the same data.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
        <label className="block">
          <span className="text-sm font-medium text-gray-800">Participants ({fromLines(participants).length})</span>
          <span className="block text-xs text-gray-500 mb-1">The email each participant labels from, one per line.</span>
          <textarea className={box} value={participants} onChange={(e) => setParticipants(e.target.value)} />
        </label>
        <label className="block">
          <span className="text-sm font-medium text-gray-800">Staff logins ({fromLines(logins).length})</span>
          <span className="block text-xs text-gray-500 mb-1">{cfg.name} staff who can log in to see their participants.</span>
          <textarea className={box} value={logins} onChange={(e) => setLogins(e.target.value)} />
        </label>
      </div>
      <div className="flex items-center gap-3 mt-3">
        <button
          type="button"
          onClick={save}
          disabled={saving || !dirty}
          className="px-3 py-1.5 text-sm rounded-md bg-gray-900 text-white disabled:opacity-40"
        >
          {saving ? 'Saving…' : 'Save'}
        </button>
        {message ? <span className={`text-sm ${message.ok ? 'text-green-700' : 'text-red-600'}`}>{message.text}</span> : null}
      </div>

      <div className="mt-6">
        <h3 className="text-sm font-medium text-gray-800 inline-flex items-center gap-1.5">
          <KeyRound className="h-4 w-4" /> API keys
        </h3>
        {newKey ? (
          <div className="mt-2 p-3 rounded-md bg-amber-50 border border-amber-200 text-sm">
            <div className="text-amber-900 mb-1">Copy this key now and send it to {cfg.name} securely. It won't be shown again.</div>
            <div className="flex items-center gap-2">
              <code className="font-mono text-xs break-all bg-white px-2 py-1 rounded border border-amber-200">{newKey}</code>
              <button
                type="button"
                onClick={() => navigator.clipboard?.writeText(newKey)}
                className="inline-flex items-center gap-1 px-2 py-1 text-xs border border-gray-300 rounded bg-white"
              >
                <Copy className="h-3.5 w-3.5" /> Copy
              </button>
            </div>
          </div>
        ) : null}
        <ul className="mt-2 divide-y divide-gray-100 border border-gray-200 rounded-md bg-white">
          {(cfg.keys || []).length === 0 ? <li className="px-3 py-2 text-sm text-gray-500">No keys yet.</li> : null}
          {(cfg.keys || []).map((k) => (
            <li key={k.id} className="px-3 py-2 text-sm flex items-center gap-3">
              <code className="font-mono text-xs text-gray-700">hlp_{org}_…{k.last4}</code>
              <span className="text-gray-600 flex-1">{k.label || 'Unnamed'}</span>
              <span className="text-xs text-gray-400">{k.created_at ? new Date(k.created_at).toLocaleDateString() : ''}</span>
              <button type="button" onClick={() => revoke(k)} className="text-red-600 hover:text-red-800" aria-label="Revoke key">
                <Trash2 className="h-4 w-4" />
              </button>
            </li>
          ))}
        </ul>
        <div className="flex items-center gap-2 mt-2">
          <input
            value={keyLabel}
            onChange={(e) => setKeyLabel(e.target.value)}
            placeholder="What it's for, e.g. Treat reporting"
            className="px-2 py-1.5 text-sm border border-gray-300 rounded-md w-72"
          />
          <button type="button" onClick={createKey} className="px-3 py-1.5 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50">
            Create key
          </button>
        </div>
      </div>

      <div className="mt-8 border-t border-gray-200 pt-4">
        <div className="text-xs font-medium uppercase tracking-wide text-gray-500">What {cfg.name} sees</div>
        <div className="-mx-4 sm:-mx-6">
          <PartnerDashboard key={previewKey} previewOrg={org} />
        </div>
      </div>
    </section>
  );
}
