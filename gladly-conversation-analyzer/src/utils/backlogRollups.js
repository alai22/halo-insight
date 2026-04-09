/**
 * Deterministic priority/status counts from Jira-shaped issue lists (no LLM).
 * Priority buckets match BugTriageCopilot backlog section labels.
 */

const PRIORITY_SECTION_ORDER = [
  'Blocker',
  'Critical',
  'Major',
  'Medium',
  'Normal',
  'Low',
  'Minor',
  'Trivial',
  '(No priority)',
];

function getPriorityRank(priority) {
  if (!priority) return 0;
  const p = String(priority).toLowerCase();
  if (p === 'blocker' || p === 'highest') return 100;
  if (p === 'critical') return 90;
  if (p === 'major' || p === 'high') return 70;
  if (p === 'medium') return 50;
  if (p === 'normal') return 45;
  if (p === 'low') return 25;
  if (p === 'minor') return 20;
  if (p === 'lowest' || p === 'trivial') return 10;
  return 0;
}

function prioritySectionLabel(priority) {
  const r = getPriorityRank(priority);
  if (r === 0) return '(No priority)';
  if (r >= 100) return 'Blocker';
  if (r >= 90) return 'Critical';
  if (r >= 70) return 'Major';
  if (r >= 50) return 'Medium';
  if (r >= 45) return 'Normal';
  if (r >= 25) return 'Low';
  if (r >= 20) return 'Minor';
  if (r >= 10) return 'Trivial';
  return '(No priority)';
}

function statusLabel(status) {
  return status != null && status !== '' ? status : '(No status)';
}

/**
 * @param {Array<{ priority?: string|null, status?: string|null }>} issues
 * @returns {{ byPriority: Array<{ label: string, count: number }>, byStatus: Array<{ label: string, count: number }> }}
 */
export function rollupBacklogByPriorityAndStatus(issues) {
  const priMap = new Map();
  const stMap = new Map();
  for (const i of issues || []) {
    const pl = prioritySectionLabel(i?.priority);
    priMap.set(pl, (priMap.get(pl) || 0) + 1);
    const sk = statusLabel(i?.status);
    stMap.set(sk, (stMap.get(sk) || 0) + 1);
  }

  const byPriority = Array.from(priMap.entries()).map(([label, count]) => ({ label, count }));
  byPriority.sort((a, b) => {
    const ia = PRIORITY_SECTION_ORDER.indexOf(a.label);
    const ib = PRIORITY_SECTION_ORDER.indexOf(b.label);
    const ua = ia === -1;
    const ub = ib === -1;
    if (!ua && !ub) return ia - ib;
    if (ua && ub) return b.count - a.count || a.label.localeCompare(b.label);
    return ua ? 1 : -1;
  });

  const byStatus = Array.from(stMap.entries())
    .map(([label, count]) => ({ label, count }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));

  return { byPriority, byStatus };
}
