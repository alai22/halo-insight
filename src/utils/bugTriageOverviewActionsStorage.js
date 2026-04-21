const STORAGE_KEY = 'bug_triage_overview_actions_v1';

/** @typedef {'accepted' | 'dismissed' | 'deferred'} OverviewActionStatus */

/**
 * Per-issue recommendation actions for a single overview fingerprint.
 * @typedef {Object} OverviewIssueActions
 * @property {OverviewActionStatus} [reprior]
 * @property {OverviewActionStatus} [title]
 * @property {OverviewActionStatus} [scorecard]
 * @property {string} [updatedAt]
 */

function loadRaw() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { v: 1, byHash: {} };
    const o = JSON.parse(raw);
    if (!o || typeof o !== 'object' || !o.byHash || typeof o.byHash !== 'object') {
      return { v: 1, byHash: {} };
    }
    return { v: 1, byHash: o.byHash };
  } catch {
    return { v: 1, byHash: {} };
  }
}

function persist(store) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
  } catch (e) {
    console.warn('Failed to persist overview actions', e);
  }
}

export function loadOverviewActionsStore() {
  return loadRaw();
}

export function getOverviewActionsForHash(store, fingerprintHash) {
  if (!fingerprintHash || !store?.byHash) return {};
  return store.byHash[fingerprintHash] || {};
}

/**
 * @param {ReturnType<typeof loadOverviewActionsStore>} store
 * @param {string} fingerprintHash
 * @param {string} issueKeyUpper
 * @param {'reprior' | 'title' | 'scorecard'} slot
 * @param {OverviewActionStatus} status
 */
export function upsertOverviewAction(store, fingerprintHash, issueKeyUpper, slot, status) {
  const key = String(issueKeyUpper || '').trim().toUpperCase();
  const fh = String(fingerprintHash || '').trim();
  if (!key || !fh) return store;
  const next = {
    ...store,
    byHash: { ...store.byHash },
  };
  const prevIssues = next.byHash[fh] || {};
  const prevRow = prevIssues[key] || {};
  next.byHash[fh] = {
    ...prevIssues,
    [key]: {
      ...prevRow,
      [slot]: status,
      updatedAt: new Date().toISOString(),
    },
  };
  persist(next);
  return next;
}
