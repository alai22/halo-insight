import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { visit } from 'unist-util-visit';
import {
  ArrowLeft,
  Bug,
  CheckCircle,
  ChevronDown,
  ChevronRight,
  ClipboardList,
  ExternalLink,
  Filter,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  FileText,
  AlertCircle,
  Copy,
  X,
  RefreshCw,
  Loader2,
  Minus,
} from 'lucide-react';
import {
  PLATFORMS,
  COMPONENTS,
  NEXT_ACTIONS,
} from '../data/bugTriageMockData';
import { rollupBacklogByPriorityAndStatus } from '../utils/backlogRollups';

const STORAGE_KEY = 'bug_triage_decisions';
const OVERVIEW_CACHE_STORAGE_KEY = 'bug_triage_backlog_overview_cache_v1';
/** Cross-tab: only one client should POST for the same fingerprint at a time (best-effort). */
const OVERVIEW_LOCK_STORAGE_KEY = 'bug_triage_backlog_overview_lock_v1';
const OVERVIEW_LOCK_TTL_MS = 120_000;
const OVERVIEW_LOCK_HEARTBEAT_MS = 12_000;

/** Labels for backlog overview Claude steps (matches API `step` ids). */
const OVERVIEW_STEP_LABELS = {
  pass1: 'Themes & duplicates',
  pass2: 'Priority review',
  pass2b: 'Deep priority refine',
  title_scan: 'Title scan',
  title_rewrite: 'Title suggestions',
};

/** Fixed order for the visual phase rail (ids match API `step`). */
const OVERVIEW_PHASE_RAIL = [
  { id: 'pass1', short: 'Themes', sub: 'Pass 1' },
  { id: 'pass2', short: 'Priority', sub: 'Pass 2' },
  { id: 'pass2b', short: 'Deep', sub: 'Refine' },
  { id: 'title_scan', short: 'Scan', sub: 'Titles' },
  { id: 'title_rewrite', short: 'Rewrite', sub: 'Titles' },
];

/**
 * Horizontal phase indicator: done / active / pending / skipped / error.
 */
function OverviewPhaseRail({ loading, progress, meta, titlePipelineEnabled = true }) {
  const steps = useMemo(() => {
    if (!titlePipelineEnabled) {
      return OVERVIEW_PHASE_RAIL.filter((s) => !['title_scan', 'title_rewrite'].includes(s.id));
    }
    return OVERVIEW_PHASE_RAIL;
  }, [titlePipelineEnabled]);

  const completedSteps = useMemo(() => {
    if (loading && progress?.completedSteps?.length) return progress.completedSteps;
    if (!loading && meta?.completed_steps?.length) return meta.completed_steps;
    if (progress?.completedSteps?.length) return progress.completedSteps;
    return [];
  }, [loading, progress, meta]);

  const getStatus = useCallback(
    (stepId) => {
      if (completedSteps.includes(stepId)) return 'done';
      if (progress?.step === stepId) {
        if (progress.phase === 'start') return 'active';
        if (progress.phase === 'error') return 'error';
      }
      if (
        stepId === 'pass2b' &&
        completedSteps.includes('title_scan') &&
        !completedSteps.includes('pass2b')
      ) {
        return 'skipped';
      }
      if (
        !loading &&
        stepId === 'pass2b' &&
        meta &&
        meta.priority_deep_pass_applied === false &&
        !completedSteps.includes('pass2b')
      ) {
        return 'skipped';
      }
      return 'pending';
    },
    [completedSteps, progress, loading, meta],
  );

  if (!loading && meta && !meta.completed_steps?.length) {
    return null;
  }

  const gridCols = steps.length <= 3 ? 'grid-cols-3' : 'grid-cols-5';

  return (
    <div className="w-full min-w-0" aria-label="Overview generation phases">
      <p className="text-[10px] font-semibold uppercase tracking-wide text-amber-900/80 mb-2">
        AI run phases
      </p>
      <div className={`grid ${gridCols} gap-1 w-full max-w-3xl mx-auto`}>
        {steps.map((step, i) => {
          const status = getStatus(step.id);
          const circleBase =
            'flex h-9 w-9 shrink-0 items-center justify-center rounded-full border-2 text-xs font-semibold transition-colors';
          let circleClass = `${circleBase} border-slate-300 bg-white text-slate-500`;
          let inner = <span className="text-[10px] tabular-nums">{i + 1}</span>;
          if (status === 'done') {
            circleClass = `${circleBase} border-emerald-500 bg-emerald-500 text-white`;
            inner = <CheckCircle className="h-4 w-4" aria-hidden />;
          } else if (status === 'active') {
            circleClass = `${circleBase} border-amber-500 bg-amber-100 text-amber-900 ring-2 ring-amber-300/80`;
            inner = <Loader2 className="h-4 w-4 animate-spin" aria-hidden />;
          } else if (status === 'error') {
            circleClass = `${circleBase} border-red-400 bg-red-50 text-red-700`;
            inner = <AlertCircle className="h-4 w-4" aria-hidden />;
          } else if (status === 'skipped') {
            circleClass = `${circleBase} border-slate-200 bg-slate-50 text-slate-400 border-dashed`;
            inner = <Minus className="h-4 w-4" aria-hidden />;
          }
          return (
            <div key={step.id} className="flex flex-col items-center min-w-0">
              <div className={circleClass} title={OVERVIEW_STEP_LABELS[step.id] || step.id}>
                {inner}
              </div>
              <span className="mt-1 text-center text-[10px] font-medium leading-tight text-amber-950/90">
                {step.short}
              </span>
              <span className="text-center text-[9px] text-amber-800/70 leading-tight">{step.sub}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

const OVERVIEW_CONSOLE_GROUP = '[BugTriage overview] AI run';

function overviewStepLabel(step) {
  return (step && OVERVIEW_STEP_LABELS[step]) || step || 'unknown';
}

/** Console-only transparency for overview timing (keeps the page UI clean). */
function logOverviewConsole(event, detail) {
  if (detail !== undefined) {
    console.info(OVERVIEW_CONSOLE_GROUP, event, detail);
  } else {
    console.info(OVERVIEW_CONSOLE_GROUP, event);
  }
}

/**
 * Long NDJSON streams often fail mid-body with net::ERR_HTTP2_PROTOCOL_ERROR (still 200) behind
 * reverse proxies; the read() promise then rejects with TypeError "network error".
 */
function isOverviewStreamTransportFailure(err) {
  if (!err || typeof err !== 'object') return false;
  if (err.name === 'AbortError') return false;
  // DOMException in some browsers / WebView
  if (err.name === 'NetworkError') return true;
  const msg = String(err.message || '').toLowerCase();
  if (err.name === 'TypeError' && (msg === 'network error' || msg.includes('network'))) return true;
  if (msg.includes('failed to fetch')) return true;
  if (msg.includes('load failed')) return true;
  if (msg.includes('err_http2') || msg.includes('http2')) return true;
  return false;
}

/**
 * Prefer ?stream=1 for backlog overview: NDJSON progress lines keep bytes moving so reverse proxies
 * are less likely to return 504 than a single JSON body that stays silent until the full run finishes.
 * Transport failures still fall back to one non-stream POST (may also need a higher proxy_read_timeout).
 */

/** Auto-run skips POST when cache matches fingerprint and is newer than this (ms). */
const BACKLOG_OVERVIEW_CACHE_TTL_MS = 60 * 60 * 1000;

function loadOverviewCacheEntry() {
  try {
    const raw = localStorage.getItem(OVERVIEW_CACHE_STORAGE_KEY);
    if (!raw) return null;
    const o = JSON.parse(raw);
    if (
      !o ||
      typeof o.fingerprint !== 'string' ||
      typeof o.overview !== 'string' ||
      typeof o.cachedAt !== 'string'
    ) {
      return null;
    }
    return o;
  } catch {
    return null;
  }
}

function saveOverviewCache(entry) {
  try {
    localStorage.setItem(OVERVIEW_CACHE_STORAGE_KEY, JSON.stringify(entry));
  } catch (e) {
    console.warn('Failed to save backlog overview cache', e);
  }
}

function loadOverviewLockEntry() {
  try {
    const raw = localStorage.getItem(OVERVIEW_LOCK_STORAGE_KEY);
    if (!raw) return null;
    const o = JSON.parse(raw);
    if (
      !o ||
      typeof o.ownerId !== 'string' ||
      typeof o.fingerprint !== 'string' ||
      typeof o.expiresAt !== 'number'
    ) {
      return null;
    }
    return o;
  } catch {
    return null;
  }
}

function saveOverviewLockEntry(entry) {
  try {
    localStorage.setItem(OVERVIEW_LOCK_STORAGE_KEY, JSON.stringify(entry));
  } catch (e) {
    console.warn('Failed to save backlog overview lock', e);
  }
}

/** Returns true if this tab holds the lock for the fingerprint. */
function tryAcquireOverviewLock(fingerprint, ownerId) {
  const now = Date.now();
  const cur = loadOverviewLockEntry();
  if (cur && cur.fingerprint === fingerprint && cur.ownerId === ownerId) {
    saveOverviewLockEntry({
      ...cur,
      expiresAt: now + OVERVIEW_LOCK_TTL_MS,
    });
    return true;
  }
  if (!cur || now > cur.expiresAt || cur.fingerprint !== fingerprint) {
    saveOverviewLockEntry({
      ownerId,
      fingerprint,
      startedAt: new Date().toISOString(),
      expiresAt: now + OVERVIEW_LOCK_TTL_MS,
    });
    return true;
  }
  return false;
}

function renewOverviewLock(ownerId, fingerprint) {
  const cur = loadOverviewLockEntry();
  if (!cur || cur.ownerId !== ownerId || cur.fingerprint !== fingerprint) return;
  saveOverviewLockEntry({
    ...cur,
    expiresAt: Date.now() + OVERVIEW_LOCK_TTL_MS,
  });
}

function clearOverviewLockIfOwner(ownerId) {
  const cur = loadOverviewLockEntry();
  if (cur && cur.ownerId === ownerId) {
    try {
      localStorage.removeItem(OVERVIEW_LOCK_STORAGE_KEY);
    } catch (e) {
      console.warn('Failed to clear backlog overview lock', e);
    }
  }
}

/**
 * Returns cached markdown if fingerprint matches and entry is within TTL; else null.
 * Cross-tab: another tab may populate cache while this tab waits on the lock.
 */
function getValidCachedOverview(fingerprint) {
  const entry = loadOverviewCacheEntry();
  if (!entry || entry.fingerprint !== fingerprint) return null;
  const t = new Date(entry.cachedAt).getTime();
  if (Number.isNaN(t) || Date.now() - t >= BACKLOG_OVERVIEW_CACHE_TTL_MS) return null;
  const timeLabel = new Date(entry.cachedAt).toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit',
  });
  return {
    overview: entry.overview,
    cacheHint: `from cache · ${timeLabel}`,
    meta: entry.meta && typeof entry.meta === 'object' ? entry.meta : null,
    cachedAtMs: t,
  };
}

/** Human label for when the last successful overview was produced (this tab or cache). */
function formatOverviewUpdatedLabel(completedAtMs) {
  if (completedAtMs == null || Number.isNaN(completedAtMs)) return null;
  const delta = Date.now() - completedAtMs;
  if (delta < 90_000) return 'Updated just now';
  return `Updated ${new Date(completedAtMs).toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit',
  })}`;
}

function getOverviewPreviewText(markdown) {
  if (typeof markdown !== 'string' || !markdown.trim()) return '';
  const lines = markdown
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean)
    .filter((s) => !s.startsWith('#'))
    .filter((s) => !s.startsWith('|'))
    .filter((s) => !s.startsWith('---'));
  if (!lines.length) return '';
  const first = lines[0];
  const sentence = first.match(/(.+?[.!?])(?:\s|$)/)?.[1] || first;
  return sentence.length > 160 ? `${sentence.slice(0, 157).trimEnd()}...` : sentence;
}

/** Plain text from a hast node (table cells may wrap content in paragraphs, emphasis, etc.). */
function hastPlainText(node) {
  if (!node) return '';
  if (node.type === 'text') return node.value || '';
  if (node.children && Array.isArray(node.children)) {
    return node.children.map(hastPlainText).join('');
  }
  return '';
}

const _RE_LEADING_REC_ARROW = /^[\u2191\u2193\u25b2\u25bc↑↓]/;
/** Cell is only a Jira issue key (e.g. HALO-26845), optional surrounding whitespace. */
const _RE_BARE_JIRA_ISSUE_KEY = /^\s*([A-Za-z][A-Za-z0-9]{1,19}-\d+)\s*$/;

function _hastClassNameList(value) {
  if (value == null) return [];
  return Array.isArray(value) ? [...value] : String(value).split(/\s+/).filter(Boolean);
}

/**
 * Mark reprioritization table rows (4 cols legacy or 5 cols with Title). Sets row tint and
 * dataOverviewRecKind on the recommendation cell for React styling.
 */
function rehypeAnnotateBacklogOverviewTables() {
  return (tree) => {
    visit(tree, 'element', (node) => {
      if (node.tagName !== 'tr') return;
      const tds = (node.children || []).filter(
        (c) => c.type === 'element' && c.tagName === 'td'
      );
      if (tds.length < 4) return;
      const recIdx = tds.length >= 5 ? 3 : 2;
      tds.forEach((td, i) => {
        td.properties = td.properties || {};
        td.properties.dataOverviewCol = String(i);
      });
      const recCell = tds[recIdx];
      if (!recCell) return;
      const rec = hastPlainText(recCell).trim().toLowerCase();
      if (!rec.startsWith('raise') && !rec.startsWith('lower')) return;
      const kind = rec.startsWith('raise') ? 'raise' : 'lower';
      recCell.properties = recCell.properties || {};
      recCell.properties.dataOverviewRecKind = kind;
      node.properties = node.properties || {};
      const cls = _hastClassNameList(node.properties.className);
      cls.push(kind === 'raise' ? 'overview-priority-raise' : 'overview-priority-lower');
      node.properties.className = cls;
    });
  };
}

/**
 * Place server-generated ### Backlog snapshot and ### By status blocks side-by-side when both exist
 * so narrow stat tables are not stretched to full width.
 */
function rehypeWrapBacklogSnapshotBlocks() {
  return (tree) => {
    if (tree.type !== 'root' || !Array.isArray(tree.children)) return;
    const { children } = tree;

    const h3Key = (node) => {
      if (!node || node.type !== 'element' || node.tagName !== 'h3') return '';
      return hastPlainText(node).trim().toLowerCase();
    };

    const snapIdx = children.findIndex((c) => h3Key(c) === 'backlog snapshot');
    const statusIdx = children.findIndex((c) => h3Key(c) === 'by status');
    if (snapIdx === -1 || statusIdx === -1 || statusIdx <= snapIdx) return;

    const findTableEndExclusive = (startFrom) => {
      for (let t = startFrom; t < children.length; t++) {
        const c = children[t];
        if (c.type === 'element' && c.tagName === 'table') {
          return t + 1;
        }
      }
      return -1;
    };

    const firstTableEnd = findTableEndExclusive(snapIdx + 1);
    if (firstTableEnd === -1 || firstTableEnd > statusIdx) return;

    const secondTableEnd = findTableEndExclusive(statusIdx + 1);
    if (secondTableEnd === -1) return;

    const snapshotCol = (nodes) => ({
      type: 'element',
      tagName: 'div',
      properties: {
        className: 'backlog-overview-snapshot-col min-w-0 shrink-0 max-w-md',
      },
      children: nodes,
    });

    const wrap = {
      type: 'element',
      tagName: 'div',
      properties: {
        className:
          'backlog-overview-snapshot-wrap flex flex-wrap gap-x-8 gap-y-4 items-start mb-4 w-full',
      },
      children: [
        snapshotCol(children.slice(snapIdx, firstTableEnd)),
        snapshotCol(children.slice(statusIdx, secondTableEnd)),
      ],
    };

    tree.children = [...children.slice(0, snapIdx), wrap, ...children.slice(secondTableEnd)];
  };
}

/**
 * Arrow + emphasis in the Recommended priority column; ticket column links when base URL is known.
 */
function createBacklogOverviewMarkdownComponents(jiraBaseUrl) {
  const base = jiraBaseUrl && String(jiraBaseUrl).replace(/\/+$/, '');
  return {
    td({ node, children, ...props }) {
      const col = node?.properties?.dataOverviewCol;
      const titleColClass =
        col === '1'
          ? 'max-w-[min(100%,28rem)] break-words whitespace-normal align-top text-[12px]'
          : '';

      if (col === '0' && base) {
        const raw = hastPlainText(node).trim();
        const m = raw.match(_RE_BARE_JIRA_ISSUE_KEY);
        if (m) {
          const key = m[1].toUpperCase();
          const href = `${base}/browse/${encodeURIComponent(key)}`;
          return (
            <td {...props}>
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="font-mono text-blue-600 underline break-words hover:text-blue-800"
              >
                {key}
              </a>
            </td>
          );
        }
      }

      const recKind = node?.properties?.dataOverviewRecKind;
      if (recKind !== 'raise' && recKind !== 'lower') {
        const cn = [props.className, titleColClass].filter(Boolean).join(' ');
        return (
          <td {...props} className={cn || undefined}>
            {children}
          </td>
        );
      }
      const raw = hastPlainText(node).trim();
      const lower = raw.toLowerCase();
      let extraClass = '';
      let prefix = null;
      if (lower.startsWith('raise')) {
        extraClass = 'text-rose-900 font-medium';
        if (!_RE_LEADING_REC_ARROW.test(raw)) {
          prefix = (
            <span className="mr-1 inline-block font-semibold text-rose-700" aria-hidden>
              ↑
            </span>
          );
        }
      } else if (lower.startsWith('lower')) {
        extraClass = 'text-emerald-900 font-medium';
        if (!_RE_LEADING_REC_ARROW.test(raw)) {
          prefix = (
            <span className="mr-1 inline-block font-semibold text-emerald-800" aria-hidden>
              ↓
            </span>
          );
        }
      }
      if (!extraClass) {
        const cn = [props.className, titleColClass].filter(Boolean).join(' ');
        return (
          <td {...props} className={cn || undefined}>
            {children}
          </td>
        );
      }
      const className = [props.className, titleColClass, extraClass].filter(Boolean).join(' ');
      return (
        <td {...props} className={className}>
          {prefix}
          {children}
        </td>
      );
    },
  };
}

/** Strip to metadata allowed by POST /api/jira/backlog-overview (description used for pass-2b priority refine). */
function slimIssueForOverview(issue) {
  const d =
    typeof issue.description === 'string' && issue.description.trim()
      ? issue.description.trim().slice(0, 2000)
      : undefined;
  return {
    key: issue.key,
    title: issue.title,
    priority: issue.priority,
    status: issue.status,
    issuetype: issue.issuetype,
    component: issue.component,
    components: issue.components,
    labels: issue.labels,
    parentKey: issue.parentKey,
    parentSummary: issue.parentSummary,
    epicKey: issue.epicKey,
    epicSummary: issue.epicSummary,
    sprint: issue.sprint,
    gaBlocker: issue.gaBlocker === true,
    needsMoreInfo: issue.needsMoreInfo === true,
    ...(d !== undefined ? { description: d } : {}),
  };
}

// Statuses hidden by default; user can check them in the filter to show
const DEFAULT_HIDDEN_STATUSES = [
  'Ready for QA',
  'Resolved',
  'Closed',
  'Ready for Merge',
  'In Code Review',
  'In Quality Control',
];

// Status → badge color classes
function getStatusBadgeClasses(status) {
  if (!status) return 'bg-sky-50 text-sky-700';
  const s = status.toLowerCase();
  if (s.includes('open') && !s.includes('ready')) return 'bg-slate-100 text-slate-700';
  if (s.includes('ready for qa') || s.includes('in qa')) return 'bg-amber-100 text-amber-800';
  if (s.includes('ready for merge') || s.includes('merge')) return 'bg-green-100 text-green-800';
  if (s.includes('in progress') || s.includes('development')) return 'bg-blue-100 text-blue-800';
  if (s.includes('blocked')) return 'bg-red-100 text-red-800';
  if (s.includes('done') || s.includes('closed') || s.includes('resolved')) return 'bg-emerald-100 text-emerald-800';
  return 'bg-sky-50 text-sky-700';
}

// Issue type → badge color classes
function getIssuetypeBadgeClasses(issuetype) {
  if (!issuetype) return 'bg-gray-100 text-gray-700';
  const t = issuetype.toLowerCase();
  if (t === 'bug') return 'bg-amber-100 text-amber-800';
  if (t === 'story') return 'bg-blue-100 text-blue-800';
  if (t === 'task') return 'bg-slate-100 text-slate-700';
  if (t === 'epic') return 'bg-purple-100 text-purple-800';
  return 'bg-gray-100 text-gray-700';
}

// Priority → badge color classes
function getPriorityBadgeClasses(priority) {
  if (!priority) return 'bg-gray-100 text-gray-700';
  const p = priority.toLowerCase();
  if (p === 'blocker' || p === 'highest') return 'bg-red-100 text-red-800';
  if (p === 'critical') return 'bg-orange-100 text-orange-900';
  if (p === 'major' || p === 'high') return 'bg-amber-100 text-amber-800';
  if (p === 'medium') return 'bg-slate-100 text-slate-700';
  if (p === 'normal') return 'bg-yellow-100 text-yellow-900';
  if (p === 'minor') return 'bg-emerald-100 text-emerald-800';
  if (p === 'trivial') return 'bg-blue-100 text-blue-800';
  if (p === 'low' || p === 'lowest') return 'bg-gray-100 text-gray-600';
  return 'bg-gray-100 text-gray-700';
}

// Priority → sort rank (higher = more urgent)
function getPriorityRank(priority) {
  if (!priority) return 0;
  const p = priority.toLowerCase();
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

/** Section heading when grouping backlog by priority (matches getPriorityRank buckets). */
function getPrioritySectionLabel(priority) {
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

const loadDecisions = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
};

const saveDecisions = (decisions) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(decisions));
  } catch (e) {
    console.warn('Failed to save bug triage decisions', e);
  }
};

const BugTriageCopilot = () => {
  const [issues, setIssues] = useState([]);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [miniDetailIssue, setMiniDetailIssue] = useState(null);
  const [decisions, setDecisionsState] = useState(loadDecisions);
  const [jiraStatus, setJiraStatus] = useState({ configured: false });
  const [jiraLoading, setJiraLoading] = useState(false);
  const [jiraError, setJiraError] = useState(null);
  const [jiraParentFilterStats, setJiraParentFilterStats] = useState(null);
  const [includeUnparentedTickets, setIncludeUnparentedTickets] = useState(false);
  const [overviewMarkdown, setOverviewMarkdown] = useState(null);
  const [overviewLoading, setOverviewLoading] = useState(false);
  const [overviewError, setOverviewError] = useState(null);
  /** Live step while NDJSON stream is in progress */
  const [overviewProgress, setOverviewProgress] = useState(null);
  const [overviewExpanded, setOverviewExpanded] = useState(false);
  /** Set when overview was restored from localStorage (auto-run only); cleared on fresh POST. */
  const [overviewCacheHint, setOverviewCacheHint] = useState(null);
  const [overviewMeta, setOverviewMeta] = useState(null);
  /** NDJSON `partial` milestone while stream still in flight (for UX copy only). */
  const [overviewPartialMilestone, setOverviewPartialMilestone] = useState(null);
  /** Wall-clock ms when overview last finished successfully (fresh run or valid cache load). */
  const [lastOverviewCompletedAt, setLastOverviewCompletedAt] = useState(null);
  /** Another tab holds the generation lock; this tab is waiting on cache / lock release. */
  const [overviewWaitingForOtherTab, setOverviewWaitingForOtherTab] = useState(false);
  const [showPrioritizationPhilosophy, setShowPrioritizationPhilosophy] = useState(false);
  const [showBacklogMetrics, setShowBacklogMetrics] = useState(false);

  // Check Jira config on mount and load issues when configured
  useEffect(() => {
    fetch('/api/jira/status')
      .then((r) => r.json())
      .then((data) => {
        const configured = data.configured ?? false;
        const base_url = data.base_url ?? null;
        setJiraStatus({ configured, base_url });
      })
      .catch(() => setJiraStatus({ configured: false }));
  }, []);

  const [jiraAncestorKey, setJiraAncestorKey] = useState(''); // e.g. HALO-23306 — only show issues under this (children, grandchildren, etc.)
  const jiraAncestorKeyRef = useRef(jiraAncestorKey);
  jiraAncestorKeyRef.current = jiraAncestorKey;

  const fetchJiraIssues = useCallback(() => {
    if (!jiraStatus.configured) return;
    setJiraError(null);
    setJiraLoading(true);
    const params = new URLSearchParams({ project: 'HALO', max_results: '1000' });
    params.set('require_parent_context', includeUnparentedTickets ? '0' : '1');
    const ancestor = (jiraAncestorKeyRef.current || '').trim();
    if (ancestor) params.set('ancestor_key', ancestor);
    fetch(`/api/jira/issues?${params}`)
      .then((res) => res.json().then((data) => ({ status: res.status, data })))
      .then(({ status, data }) => {
        if (status !== 200 || data.status !== 'success') {
          setJiraError(data.message || 'Failed to load issues from Jira');
          setIssues([]);
          setJiraParentFilterStats(null);
          return;
        }
        setIssues(Array.isArray(data.data) ? data.data : []);
        setJiraParentFilterStats({
          parentFilterApplied: data.parent_filter_applied === true,
          countBefore: Number(data.count_before_parent_filter ?? data.count ?? 0),
          countAfter: Number(data.count_after_parent_filter ?? data.count ?? 0),
          maxResultsRequested: Number.isFinite(Number(data.max_results_requested))
            ? Number(data.max_results_requested)
            : 1000,
        });
      })
      .catch((err) => {
        setJiraError(err.message || 'Failed to fetch Jira issues');
        setIssues([]);
        setJiraParentFilterStats(null);
      })
      .finally(() => setJiraLoading(false));
  }, [jiraStatus.configured, includeUnparentedTickets]);

  // Fetch issues when Jira is configured / parent-context mode changes
  useEffect(() => {
    if (!jiraStatus.configured) return;
    fetchJiraIssues();
  }, [jiraStatus.configured, fetchJiraIssues, includeUnparentedTickets]);

  const setDecisions = (next) => {
    setDecisionsState((prev) => {
      const nextState = typeof next === 'function' ? next(prev) : next;
      saveDecisions(nextState);
      return nextState;
    });
  };

  // Filters
  const [filterComponent, setFilterComponent] = useState('');
  const [filterPlatform, setFilterPlatform] = useState('');
  const [filterCluster, setFilterCluster] = useState('');
  const [sortBy, setSortBy] = useState('priority');
  const [sortDirection, setSortDirection] = useState('desc');
  const [groupByCluster, setGroupByCluster] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const clusters = useMemo(() => {
    const set = new Set();
    issues.forEach((i) => i.clusterLabel && set.add(i.clusterLabel));
    return Array.from(set).sort();
  }, [issues]);

  const componentOptions = useMemo(() => {
    const set = new Set();
    issues.forEach((i) => {
      const comps = i.components?.length ? i.components : (i.component ? [i.component] : []);
      comps.forEach((c) => set.add(c));
    });
    return Array.from(set).sort();
  }, [issues]);

  const statusOptions = useMemo(() => {
    const set = new Set();
    issues.forEach((i) => set.add(i.status != null && i.status !== '' ? i.status : '(No status)'));
    return Array.from(set).sort((a, b) => (a === '(No status)' ? 1 : b === '(No status)' ? -1 : a.localeCompare(b)));
  }, [issues]);

  const [hiddenStatuses, setHiddenStatuses] = useState(() => new Set(DEFAULT_HIDDEN_STATUSES));
  const [showStatusDropdown, setShowStatusDropdown] = useState(false);
  const statusDropdownRef = useRef(null);
  const toggleStatusVisibility = useCallback((status) => {
    const key = status === '(No status)' ? status : status;
    setHiddenStatuses((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }, []);

  useEffect(() => {
    if (!showStatusDropdown) return;
    const onOutside = (e) => {
      if (statusDropdownRef.current && !statusDropdownRef.current.contains(e.target)) {
        setShowStatusDropdown(false);
      }
    };
    document.addEventListener('click', onOutside, true);
    return () => document.removeEventListener('click', onOutside, true);
  }, [showStatusDropdown]);

  const filteredAndSorted = useMemo(() => {
    let list = [...issues];
    if (hiddenStatuses.size > 0) {
      list = list.filter((i) => {
        const s = i.status != null && i.status !== '' ? i.status : '(No status)';
        return !hiddenStatuses.has(s);
      });
    }
    if (filterComponent) {
      list = list.filter((i) => {
        const comps = i.components?.length ? i.components : (i.component ? [i.component] : []);
        return comps.includes(filterComponent);
      });
    }
    if (filterPlatform) list = list.filter((i) => i.platform === filterPlatform);
    if (filterCluster) list = list.filter((i) => i.clusterLabel === filterCluster);

    const mult = sortDirection === 'asc' ? 1 : -1;
    if (sortBy === 'priority') {
      list.sort((a, b) => mult * (getPriorityRank(a.priority) - getPriorityRank(b.priority)));
    } else {
      list.sort(
        (a, b) =>
          mult *
          (new Date(a.updated || a.created).getTime() - new Date(b.updated || b.created).getTime())
      );
    }
    return list;
  }, [
    issues,
    hiddenStatuses,
    filterComponent,
    filterPlatform,
    filterCluster,
    sortBy,
    sortDirection,
  ]);

  const backlogOverviewFingerprint = useMemo(
    () =>
      filteredAndSorted
        .map(
          (i) =>
            `${i.key}|${i.updated || ''}|${i.status || ''}|${(i.title || '').slice(0, 64)}`,
        )
        .join('\n'),
    [filteredAndSorted],
  );

  const filteredAndSortedRef = useRef(filteredAndSorted);
  filteredAndSortedRef.current = filteredAndSorted;
  const overviewLockOwnerIdRef = useRef(null);
  const overviewLockHeartbeatRef = useRef(null);
  const overviewCrossTabWaitCleanupRef = useRef(null);
  const overviewFetchInFlightRef = useRef(false);

  function ensureOverviewLockOwnerId() {
    if (!overviewLockOwnerIdRef.current) {
      overviewLockOwnerIdRef.current =
        typeof crypto !== 'undefined' && crypto.randomUUID
          ? crypto.randomUUID()
          : `owner_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`;
    }
    return overviewLockOwnerIdRef.current;
  }

  const stopOverviewCrossTabWait = useCallback(() => {
    if (overviewCrossTabWaitCleanupRef.current) {
      overviewCrossTabWaitCleanupRef.current();
      overviewCrossTabWaitCleanupRef.current = null;
    }
    setOverviewWaitingForOtherTab(false);
  }, []);

  const runBacklogOverview = useCallback(async (list, signal, fingerprintForCache = null, lockOwnerId = null) => {
    if (!list.length) {
      setOverviewMarkdown(null);
      setOverviewError(null);
      setOverviewProgress(null);
      setOverviewPartialMilestone(null);
      setOverviewLoading(false);
      setOverviewCacheHint(null);
      setOverviewMeta(null);
      return;
    }
    if (overviewFetchInFlightRef.current) {
      if (lockOwnerId) clearOverviewLockIfOwner(lockOwnerId);
      return;
    }
    overviewFetchInFlightRef.current = true;
    setOverviewWaitingForOtherTab(false);
    setOverviewLoading(true);
    setOverviewError(null);
    setOverviewProgress(null);
    setOverviewPartialMilestone(null);
    setOverviewCacheHint(null);
    if (lockOwnerId && fingerprintForCache != null) {
      if (overviewLockHeartbeatRef.current) {
        clearInterval(overviewLockHeartbeatRef.current);
        overviewLockHeartbeatRef.current = null;
      }
      overviewLockHeartbeatRef.current = setInterval(() => {
        renewOverviewLock(lockOwnerId, fingerprintForCache);
      }, OVERVIEW_LOCK_HEARTBEAT_MS);
    }
    const runStartedAt = performance.now();
    const stepStartedAt = Object.create(null);
    let overviewLogGroupOpened = false;
    const slim = list.map(slimIssueForOverview);

    const applyOverviewJsonResponse = (jsonRes, data, traceKind) => {
      if (signal?.aborted) return;
      if (!jsonRes.ok || data.status !== 'success') {
        const errLabel = traceKind === 'fallback' ? 'Fallback error payload' : 'Non-stream error';
        logOverviewConsole(errLabel, {
          wallClockMs: Math.round(performance.now() - runStartedAt),
          httpStatus: jsonRes.status,
          errorCode: data.error_code,
          failedStep: data.failed_step,
          completedSteps: data.completed_steps,
          retryAfterSeconds: data.retry_after_seconds,
        });
        setOverviewError({
          message:
            jsonRes.status === 504
              ? `${data.message?.trim() || 'Gateway timeout (504).'} Large overviews often exceed a ~60s proxy limit when the body is empty until the end. The default request uses NDJSON streaming to keep the link busy; otherwise narrow filters or raise proxy_read_timeout for POST /api/jira/backlog-overview.`
              : data.message || 'Failed to generate backlog overview',
          errorCode: data.error_code,
          failedStep: data.failed_step,
          completedSteps: data.completed_steps,
          retryAfterSeconds: data.retry_after_seconds,
          details: data.details,
        });
        setOverviewMarkdown(null);
        setOverviewMeta(null);
        return;
      }
      const md = typeof data.overview === 'string' ? data.overview : '';
      const meta = data.meta && typeof data.meta === 'object' ? data.meta : null;
      const okLabel = traceKind === 'fallback' ? 'Fallback success' : 'Non-stream success';
      logOverviewConsole(okLabel, {
        wallClockMs: Math.round(performance.now() - runStartedAt),
        overviewChars: md.length,
        overviewIncomplete: meta?.overview_incomplete,
        issueCount: meta?.issue_count,
      });
      setOverviewMarkdown(md);
      setOverviewMeta(meta);
      setLastOverviewCompletedAt(Date.now());
      if (fingerprintForCache != null) {
        saveOverviewCache({
          fingerprint: fingerprintForCache,
          overview: md,
          cachedAt: new Date().toISOString(),
          ...(meta ? { meta } : {}),
        });
      }
    };

    try {
      try {
        console.groupCollapsed(`${OVERVIEW_CONSOLE_GROUP} · ${list.length} issue(s)`);
        overviewLogGroupOpened = true;
        logOverviewConsole('Request started', {
          issues: list.length,
          time: new Date().toISOString(),
        });

        const fetchStartedAt = performance.now();
        const res = await fetch('/api/jira/backlog-overview?stream=1', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/x-ndjson',
          },
          body: JSON.stringify({ issues: slim }),
          signal,
        });
        logOverviewConsole('Response headers', {
          ms: Math.round(performance.now() - fetchStartedAt),
          status: res.status,
        });
        if (signal?.aborted) return;

        const contentType = (res.headers.get('content-type') || '').toLowerCase();
        if (!contentType.includes('ndjson')) {
          const parseStartedAt = performance.now();
          const data = await res.json().catch(() => ({}));
          logOverviewConsole('JSON body parsed', { ms: Math.round(performance.now() - parseStartedAt) });
          if (signal?.aborted) return;
          applyOverviewJsonResponse(res, data, 'initial-json');
          return;
        }

        const reader = res.body?.getReader();
        if (!reader) {
          logOverviewConsole('Streaming unsupported', {
            wallClockMs: Math.round(performance.now() - runStartedAt),
          });
          setOverviewError({ message: 'Streaming not supported in this browser' });
          setOverviewMarkdown(null);
          setOverviewMeta(null);
          return;
        }

        const streamStartedAt = performance.now();
        const decoder = new TextDecoder();
        let buffer = '';
        let finalResult = null;
        let streamEnded = false;
        try {
          while (!streamEnded) {
            const { done, value } = await reader.read();
            if (signal?.aborted) {
              reader.cancel().catch(() => {});
              logOverviewConsole('Aborted during stream', {
                wallClockMs: Math.round(performance.now() - runStartedAt),
              });
              return;
            }
            if (done) {
              streamEnded = true;
              break;
            }
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() ?? '';
            for (const line of lines) {
              if (!line.trim()) continue;
              let ev;
              try {
                ev = JSON.parse(line);
              } catch {
                continue;
              }
              if (ev.type === 'progress') {
                const step = ev.step;
                const phase = ev.phase;
                const label = overviewStepLabel(step);
                if (phase === 'start') {
                  stepStartedAt[step] = performance.now();
                  logOverviewConsole(`Step start · ${label}`, {
                    step,
                    completedSteps: Array.isArray(ev.completed) ? ev.completed : [],
                  });
                } else if (phase === 'done' || phase === 'error') {
                  const t0 = stepStartedAt[step];
                  const durationMs = t0 != null ? Math.round(performance.now() - t0) : null;
                  logOverviewConsole(`Step ${phase} · ${label}`, {
                    step,
                    durationMs,
                    ...(durationMs === 0
                      ? { note: 'start+done in same chunk (timestamps identical in one turn)' }
                      : {}),
                    completedSteps: Array.isArray(ev.completed) ? ev.completed : [],
                  });
                }
                setOverviewProgress({
                  step: ev.step,
                  phase: ev.phase,
                  completedSteps: Array.isArray(ev.completed) ? ev.completed : [],
                });
              }
              if (ev.type === 'partial' && typeof ev.markdown === 'string') {
                setOverviewMarkdown(ev.markdown);
                setOverviewPartialMilestone(typeof ev.milestone === 'string' ? ev.milestone : null);
                logOverviewConsole('Partial markdown', {
                  milestone: ev.milestone,
                  chars: ev.markdown.length,
                });
              }
              if (ev.type === 'result') {
                finalResult = ev;
              }
            }
          }
          if (buffer.trim()) {
            try {
              const ev = JSON.parse(buffer);
              if (ev.type === 'result') finalResult = ev;
              else if (ev.type === 'partial' && typeof ev.markdown === 'string') {
                setOverviewMarkdown(ev.markdown);
                setOverviewPartialMilestone(typeof ev.milestone === 'string' ? ev.milestone : null);
                logOverviewConsole('Partial markdown', {
                  milestone: ev.milestone,
                  chars: ev.markdown.length,
                });
              }
            } catch {
              /* ignore */
            }
          }

          logOverviewConsole('Stream bytes finished', {
            ms: Math.round(performance.now() - streamStartedAt),
          });
        } catch (streamErr) {
          if (signal?.aborted) {
            reader.cancel().catch(() => {});
            throw streamErr;
          }
          if (!isOverviewStreamTransportFailure(streamErr)) {
            reader.cancel().catch(() => {});
            throw streamErr;
          }
          logOverviewConsole(
            'Stream transport error; retrying single JSON POST (no stream) — mitigates HTTP/2 / proxy drops on long bodies',
            {
              name: streamErr.name,
              message: streamErr.message,
              wallClockMs: Math.round(performance.now() - runStartedAt),
            },
          );
          reader.cancel().catch(() => {});
          setOverviewProgress(null);
          const fbFetchAt = performance.now();
          const res2 = await fetch('/api/jira/backlog-overview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ issues: slim }),
            signal,
          });
          logOverviewConsole('Fallback response headers', {
            ms: Math.round(performance.now() - fbFetchAt),
            status: res2.status,
          });
          if (signal?.aborted) return;
          const parseStartedAt = performance.now();
          const data2 = await res2.json().catch(() => ({}));
          logOverviewConsole('Fallback JSON parsed', {
            ms: Math.round(performance.now() - parseStartedAt),
          });
          if (signal?.aborted) return;
          applyOverviewJsonResponse(res2, data2, 'fallback');
          return;
        }

        if (signal?.aborted) return;

        if (!finalResult) {
          logOverviewConsole('No terminal result event', {
            wallClockMs: Math.round(performance.now() - runStartedAt),
          });
          setOverviewError({ message: 'No result from overview service' });
          setOverviewMarkdown(null);
          setOverviewMeta(null);
          return;
        }

        if (finalResult.status === 'error') {
          logOverviewConsole('Terminal result: error', {
            wallClockMs: Math.round(performance.now() - runStartedAt),
            errorCode: finalResult.error_code,
            failedStep: finalResult.failed_step,
            completedSteps: finalResult.completed_steps,
            retryAfterSeconds: finalResult.retry_after_seconds,
          });
          setOverviewError({
            message: finalResult.message || 'Failed to generate backlog overview',
            errorCode: finalResult.error_code,
            failedStep: finalResult.failed_step,
            completedSteps: finalResult.completed_steps,
            retryAfterSeconds: finalResult.retry_after_seconds,
            details: finalResult.details,
          });
          setOverviewMarkdown(null);
          setOverviewMeta(null);
          return;
        }

        const md = typeof finalResult.overview === 'string' ? finalResult.overview : '';
        const meta = finalResult.meta && typeof finalResult.meta === 'object' ? finalResult.meta : null;
        logOverviewConsole('Terminal result: success', {
          wallClockMs: Math.round(performance.now() - runStartedAt),
          overviewChars: md.length,
          overviewIncomplete: meta?.overview_incomplete,
          failedStep: meta?.failed_step,
          issueCount: meta?.issue_count,
          truncated: meta?.truncated,
        });
        setOverviewMarkdown(md);
        setOverviewMeta(meta);
        setLastOverviewCompletedAt(Date.now());
        if (fingerprintForCache != null) {
          saveOverviewCache({
            fingerprint: fingerprintForCache,
            overview: md,
            cachedAt: new Date().toISOString(),
            ...(meta ? { meta } : {}),
          });
        }
      } finally {
        if (overviewLogGroupOpened) {
          logOverviewConsole('Run finished (wall clock)', {
            ms: Math.round(performance.now() - runStartedAt),
          });
          console.groupEnd();
          overviewLogGroupOpened = false;
        }
      }
    } catch (e) {
      if (overviewLogGroupOpened) {
        console.groupEnd();
        overviewLogGroupOpened = false;
      }
      if (e.name === 'AbortError') return;
      if (isOverviewStreamTransportFailure(e) && !signal?.aborted) {
        logOverviewConsole('Transport error (outer catch); retrying JSON POST without stream', {
          name: e.name,
          message: e.message,
          wallClockMs: Math.round(performance.now() - runStartedAt),
        });
        try {
          const fbAt = performance.now();
          const resFb = await fetch('/api/jira/backlog-overview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ issues: slim }),
            signal,
          });
          logOverviewConsole('Outer fallback response headers', {
            ms: Math.round(performance.now() - fbAt),
            status: resFb.status,
          });
          if (signal?.aborted) return;
          const dataFb = await resFb.json().catch(() => ({}));
          applyOverviewJsonResponse(resFb, dataFb, 'fallback');
        } catch (e2) {
          console.info(OVERVIEW_CONSOLE_GROUP, 'Outer fallback failed', {
            name: e2.name,
            message: e2.message,
          });
          setOverviewError({ message: e2.message || e.message || 'Request failed' });
          setOverviewMarkdown(null);
          setOverviewMeta(null);
        }
        return;
      }
      console.info(OVERVIEW_CONSOLE_GROUP, 'Client error', {
        wallClockMs: Math.round(performance.now() - runStartedAt),
        name: e.name,
        message: e.message,
      });
      setOverviewError({ message: e.message || 'Request failed' });
      setOverviewMarkdown(null);
      setOverviewMeta(null);
    } finally {
      overviewFetchInFlightRef.current = false;
      if (overviewLockHeartbeatRef.current) {
        clearInterval(overviewLockHeartbeatRef.current);
        overviewLockHeartbeatRef.current = null;
      }
      if (lockOwnerId) {
        clearOverviewLockIfOwner(lockOwnerId);
      }
      setOverviewLoading(false);
      setOverviewProgress(null);
      setOverviewPartialMilestone(null);
    }
  }, []);

  /** When another tab holds the lock, poll + listen for cache or stale lock, then run or hydrate. */
  const startOverviewCrossTabWait = useCallback(
    (fingerprint, signal) => {
      stopOverviewCrossTabWait();
      setOverviewWaitingForOtherTab(true);
      const tryHydrate = () => {
        if (signal?.aborted) return;
        const cached = getValidCachedOverview(fingerprint);
        if (cached) {
          setOverviewMarkdown(cached.overview);
          setOverviewError(null);
          setOverviewLoading(false);
          setOverviewPartialMilestone(null);
          setOverviewCacheHint(cached.cacheHint);
          setOverviewMeta(cached.meta);
          setLastOverviewCompletedAt(cached.cachedAtMs ?? Date.now());
          stopOverviewCrossTabWait();
          return;
        }
        const ownerId = ensureOverviewLockOwnerId();
        if (tryAcquireOverviewLock(fingerprint, ownerId)) {
          stopOverviewCrossTabWait();
          runBacklogOverview(filteredAndSortedRef.current, signal, fingerprint, ownerId);
        }
      };
      const interval = setInterval(tryHydrate, 2000);
      const onStorage = (e) => {
        if (signal?.aborted) return;
        if (e.key !== OVERVIEW_CACHE_STORAGE_KEY && e.key !== OVERVIEW_LOCK_STORAGE_KEY) return;
        tryHydrate();
      };
      window.addEventListener('storage', onStorage);
      tryHydrate();
      overviewCrossTabWaitCleanupRef.current = () => {
        window.removeEventListener('storage', onStorage);
        clearInterval(interval);
      };
    },
    [runBacklogOverview, stopOverviewCrossTabWait],
  );

  useEffect(() => {
    if (!jiraStatus.configured || jiraLoading) return;
    if (filteredAndSorted.length === 0) {
      setOverviewMarkdown(null);
      setOverviewError(null);
      setOverviewProgress(null);
      setOverviewPartialMilestone(null);
      setOverviewLoading(false);
      setOverviewCacheHint(null);
      setOverviewMeta(null);
      stopOverviewCrossTabWait();
      return;
    }
    const cached = getValidCachedOverview(backlogOverviewFingerprint);
    if (cached) {
      setOverviewMarkdown(cached.overview);
      setOverviewError(null);
      setOverviewLoading(false);
      setOverviewPartialMilestone(null);
      setOverviewCacheHint(cached.cacheHint);
      setOverviewMeta(cached.meta);
      setLastOverviewCompletedAt(cached.cachedAtMs ?? Date.now());
      stopOverviewCrossTabWait();
      return;
    }
    const ownerId = ensureOverviewLockOwnerId();
    const ac = new AbortController();
    const timer = setTimeout(() => {
      if (ac.signal.aborted) return;
      if (!tryAcquireOverviewLock(backlogOverviewFingerprint, ownerId)) {
        startOverviewCrossTabWait(backlogOverviewFingerprint, ac.signal);
        return;
      }
      runBacklogOverview(filteredAndSorted, ac.signal, backlogOverviewFingerprint, ownerId);
    }, 500);
    return () => {
      clearTimeout(timer);
      ac.abort();
      stopOverviewCrossTabWait();
    };
  }, [
    jiraStatus.configured,
    jiraLoading,
    backlogOverviewFingerprint,
    filteredAndSorted,
    runBacklogOverview,
    stopOverviewCrossTabWait,
    startOverviewCrossTabWait,
  ]);

  const backlogOverviewMarkdownComponents = useMemo(
    () => createBacklogOverviewMarkdownComponents(jiraStatus.base_url),
    [jiraStatus.base_url],
  );
  const overviewPreviewText = useMemo(
    () => getOverviewPreviewText(overviewMarkdown),
    [overviewMarkdown],
  );
  const overviewFreshnessLabel = useMemo(
    () => (overviewCacheHint ? 'from cache' : 'fresh'),
    [overviewCacheHint],
  );
  const overviewUpdatedLabel = useMemo(
    () => formatOverviewUpdatedLabel(lastOverviewCompletedAt),
    [lastOverviewCompletedAt],
  );
  const overviewProgressLabel = useMemo(() => {
    if (!overviewProgress?.step) return null;
    const name = OVERVIEW_STEP_LABELS[overviewProgress.step] || overviewProgress.step;
    if (overviewProgress.phase === 'start') return `Running: ${name}…`;
    if (overviewProgress.phase === 'done') return `Finished: ${name}`;
    if (overviewProgress.phase === 'error') return `Skipped: ${name} (error)`;
    return name;
  }, [overviewProgress]);
  const titleSuggestionsCount = useMemo(() => {
    const n = Number(overviewMeta?.title_rewrite_rows);
    return Number.isFinite(n) && n > 0 ? n : 0;
  }, [overviewMeta]);
  const parentFilteredOutCount = useMemo(() => {
    if (!jiraParentFilterStats?.parentFilterApplied) return 0;
    const before = Number(jiraParentFilterStats.countBefore ?? 0);
    const after = Number(jiraParentFilterStats.countAfter ?? 0);
    if (!Number.isFinite(before) || !Number.isFinite(after)) return 0;
    return Math.max(0, before - after);
  }, [jiraParentFilterStats]);

  const visibleBacklogRollups = useMemo(
    () => rollupBacklogByPriorityAndStatus(filteredAndSorted),
    [filteredAndSorted],
  );
  const loadedBacklogRollups = useMemo(() => rollupBacklogByPriorityAndStatus(issues), [issues]);

  const groupedByCluster = useMemo(() => {
    if (!groupByCluster) return null;
    const map = new Map();
    filteredAndSorted.forEach((issue) => {
      const label = issue.clusterLabel || 'No cluster';
      if (!map.has(label)) map.set(label, []);
      map.get(label).push(issue);
    });
    return Array.from(map.entries()).sort((a, b) => a[0].localeCompare(b[0]));
  }, [filteredAndSorted, groupByCluster]);

  /** Consecutive runs by priority rank when sorted by priority (for section dividers). */
  const backlogPriorityGroups = useMemo(() => {
    if (groupByCluster || sortBy !== 'priority' || filteredAndSorted.length === 0) {
      return null;
    }
    const groups = [];
    let currentRank = getPriorityRank(filteredAndSorted[0].priority);
    let current = [filteredAndSorted[0]];
    for (let i = 1; i < filteredAndSorted.length; i++) {
      const issue = filteredAndSorted[i];
      const r = getPriorityRank(issue.priority);
      if (r !== currentRank) {
        groups.push({
          rank: currentRank,
          label: getPrioritySectionLabel(current[0].priority),
          issues: current,
        });
        currentRank = r;
        current = [issue];
      } else {
        current.push(issue);
      }
    }
    groups.push({
      rank: currentRank,
      label: getPrioritySectionLabel(current[0].priority),
      issues: current,
    });
    return groups;
  }, [filteredAndSorted, sortBy, groupByCluster]);

  const summaryData = useMemo(() => {
    const triagedIds = new Set(Object.keys(decisions));
    const byComponent = {};
    const byPlatform = {};
    let gaBlockerCount = 0;
    const clustersReviewed = new Set();
    const overrides = [];
    issues.forEach((i) => {
      if (i.gaBlocker) gaBlockerCount++;
      const comps = i.components?.length ? i.components : (i.component ? [i.component] : []);
      comps.forEach((c) => { byComponent[c] = (byComponent[c] || 0) + 1; });
      byPlatform[i.platform] = (byPlatform[i.platform] || 0) + 1;
      if (triagedIds.has(i.id) && i.clusterLabel) clustersReviewed.add(i.clusterLabel);
      const d = decisions[i.id];
      if (d && (d.reasonForOverride || d.priority || d.component || d.gaBlocker !== undefined || d.nextAction)) {
        overrides.push({ key: i.key, decision: d, issue: i });
      }
    });
    return { byComponent, byPlatform, gaBlockerCount, clustersReviewed: Array.from(clustersReviewed), overrides };
  }, [issues, decisions]);

  const isTriaged = (issueId) => !!decisions[issueId];

  // Detail view
  if (selectedIssue) {
    return (
      <BugTriageDetail
        issue={selectedIssue}
        allIssues={issues}
        decisions={decisions}
        setDecisions={setDecisions}
        onBack={() => setSelectedIssue(null)}
        NEXT_ACTIONS={NEXT_ACTIONS}
        COMPONENTS={COMPONENTS}
        jiraBaseUrl={jiraStatus.base_url || null}
        jiraTicketHref={jiraStatus.base_url ? `${jiraStatus.base_url}/browse/${selectedIssue.key}` : null}
      />
    );
  }

  // Backlog view
  const cardProps = (issue) => ({
    issue,
    triaged: isTriaged(issue.id),
    onClick: () => setMiniDetailIssue(issue),
    jiraBaseUrl: jiraStatus.base_url || null,
    jiraTicketHref: jiraStatus.base_url ? `${jiraStatus.base_url}/browse/${issue.key}` : null,
  });

  const listContent = groupByCluster && groupedByCluster ? (
    <div className="space-y-6">
      {groupedByCluster.map(([clusterLabel, items]) => (
        <div key={clusterLabel}>
          <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
            <ClipboardList className="h-4 w-4" />
            {clusterLabel} ({items.length})
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {items.map((issue) => (
              <BacklogCard key={issue.id} {...cardProps(issue)} />
            ))}
          </div>
        </div>
      ))}
    </div>
  ) : backlogPriorityGroups ? (
    <div className="space-y-8">
      {backlogPriorityGroups.map((g) => (
        <section key={`pri-${g.rank}-${g.label}`} className="min-w-0" aria-label={`${g.label} issues`}>
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1 mb-3 pb-2 border-b border-amber-200/90">
            <span
              className={`inline-flex items-center rounded-md px-2.5 py-1 text-xs font-bold uppercase tracking-wide ${getPriorityBadgeClasses(g.issues[0]?.priority)}`}
            >
              {g.label}
            </span>
            <span className="text-sm text-gray-500">
              {g.issues.length} issue{g.issues.length === 1 ? '' : 's'}
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {g.issues.map((issue) => (
              <BacklogCard key={issue.id} {...cardProps(issue)} />
            ))}
          </div>
        </section>
      ))}
    </div>
  ) : (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
      {filteredAndSorted.map((issue) => (
        <BacklogCard key={issue.id} {...cardProps(issue)} />
      ))}
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-3 py-4 sm:p-6 min-w-0">
      <div className="mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-900 flex items-center gap-2 min-w-0">
          <Bug className="h-6 w-6 sm:h-7 sm:w-7 text-amber-600 shrink-0" />
          <span className="truncate sm:whitespace-normal">Bug Triage Copilot</span>
        </h1>
      </div>

      {/* Jira controls */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-3 sm:p-4 mb-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
          {jiraLoading && (
            <span className="text-sm text-gray-500">Loading…</span>
          )}
          {!jiraLoading && !jiraError && issues.length > 0 && (
            <span className="text-sm text-green-700">{issues.length} issues loaded from Jira</span>
          )}
          {jiraError && (
            <span className="text-sm text-red-600 break-words">{jiraError}</span>
          )}
          {jiraStatus.configured && (
            <>
              <button
                type="button"
                onClick={fetchJiraIssues}
                disabled={jiraLoading}
                className="inline-flex items-center justify-center gap-1.5 px-3 py-2 sm:px-2 sm:py-1 text-sm sm:text-xs text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md disabled:opacity-50 w-full sm:w-auto"
                title="Refresh issues from Jira"
              >
                <RefreshCw className={`h-4 w-4 sm:h-3.5 sm:w-3.5 ${jiraLoading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
              <div className="flex flex-col gap-2 w-full min-w-0 sm:flex-row sm:items-center sm:flex-wrap sm:w-auto">
                <span className="text-sm text-gray-500 shrink-0">Under issue:</span>
                <input
                  type="text"
                  value={jiraAncestorKey}
                  onChange={(e) => setJiraAncestorKey(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && fetchJiraIssues()}
                  placeholder="e.g. HALO-23306"
                  className="px-3 py-2 sm:px-2 sm:py-1 text-sm border border-gray-300 rounded-md w-full min-w-0 sm:w-40 max-w-full font-mono focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  title="Show only children, grandchildren, etc. of this issue"
                />
                <div className="flex flex-wrap items-center gap-2">
                <button
                  type="button"
                  onClick={fetchJiraIssues}
                  disabled={jiraLoading}
                  className="px-3 py-2 sm:px-2 sm:py-1 text-sm sm:text-xs text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50 min-h-[44px] sm:min-h-0"
                >
                  Apply
                </button>
                {jiraAncestorKey.trim() && (
                  <button
                    type="button"
                    onClick={() => {
                      jiraAncestorKeyRef.current = '';
                      setJiraAncestorKey('');
                      fetchJiraIssues();
                    }}
                    disabled={jiraLoading}
                    className="px-3 py-2 sm:px-2 sm:py-1 text-sm sm:text-xs text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md disabled:opacity-50 min-h-[44px] sm:min-h-0"
                  >
                    Clear
                  </button>
                )}
                {jiraAncestorKey.trim() && jiraStatus.base_url && (
                  <a
                    href={`${jiraStatus.base_url}/browse/${jiraAncestorKey.trim()}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm sm:text-xs text-blue-600 hover:underline inline-flex items-center gap-0.5 py-2 sm:py-0"
                  >
                    Open in Jira
                    <ExternalLink className="h-3 w-3 shrink-0" />
                  </a>
                )}
                </div>
              </div>
            </>
          )}
          {!jiraStatus.configured && (
            <span className="text-xs text-gray-500">Jira: configure .env to enable</span>
          )}
        </div>
      </div>

      {/* Filters & sort */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-3 sm:p-4 mb-4 min-w-0">
        <div className="flex flex-col gap-4 sm:flex-row sm:flex-wrap sm:items-center sm:gap-3">
          <span className="text-sm font-medium text-gray-700 flex items-center gap-1 shrink-0">
            <Filter className="h-4 w-4 shrink-0" /> Filters
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:flex lg:flex-wrap lg:items-center gap-2 sm:gap-3 flex-1 min-w-0 w-full lg:w-auto">
          <select
            value={filterComponent}
            onChange={(e) => setFilterComponent(e.target.value)}
            className="w-full min-w-0 lg:w-auto px-3 py-2 sm:px-2 sm:py-1 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 max-w-full"
          >
            <option value="">All components</option>
            {(componentOptions.length ? componentOptions : COMPONENTS).map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <select
            value={filterPlatform}
            onChange={(e) => setFilterPlatform(e.target.value)}
            className="w-full min-w-0 lg:w-auto px-3 py-2 sm:px-2 sm:py-1 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 max-w-full"
          >
            <option value="">All platforms</option>
            {PLATFORMS.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
          <select
            value={filterCluster}
            onChange={(e) => setFilterCluster(e.target.value)}
            className="w-full min-w-0 lg:w-auto px-3 py-2 sm:px-2 sm:py-1 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 max-w-full"
          >
            <option value="">All clusters</option>
            {clusters.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <div className="relative w-full sm:w-auto" ref={statusDropdownRef}>
            <button
              type="button"
              onClick={() => setShowStatusDropdown((v) => !v)}
              className="inline-flex w-full sm:w-auto justify-center sm:justify-start items-center gap-1 px-3 py-2 sm:px-2 sm:py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 focus:ring-2 focus:ring-blue-500 text-gray-700 min-h-[44px] sm:min-h-0"
              title="Show/hide by status"
            >
              Status
              <ChevronDown className={`h-4 w-4 shrink-0 transition-transform ${showStatusDropdown ? 'rotate-180' : ''}`} />
            </button>
            {showStatusDropdown && (
              <div className="absolute left-0 right-0 sm:right-auto top-full mt-1 z-20 min-w-0 sm:min-w-[12rem] max-h-64 overflow-auto py-2 bg-white border border-gray-200 rounded-lg shadow-lg">
                <div className="px-3 py-1 text-xs font-medium text-gray-500 uppercase">Show issues with status</div>
                {statusOptions.length > 0 ? (
                  statusOptions.map((status) => (
                    <label
                      key={status}
                      className="flex items-center gap-2 px-3 py-1.5 hover:bg-gray-50 cursor-pointer text-sm text-gray-700"
                    >
                      <input
                        type="checkbox"
                        checked={!hiddenStatuses.has(status)}
                        onChange={() => toggleStatusVisibility(status)}
                        className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                      />
                      {status}
                    </label>
                  ))
                ) : (
                  <p className="px-3 py-2 text-sm text-gray-500">Load issues to see statuses</p>
                )}
                <p className="px-3 pt-2 mt-1 border-t border-gray-100 text-xs text-gray-500">
                  By default, Ready for QA, Resolved, and In Progress are hidden.
                </p>
              </div>
            )}
          </div>
          </div>
          <div className="hidden sm:block h-5 w-px shrink-0 bg-gray-300 self-stretch sm:self-auto" aria-hidden />
          <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto pt-1 border-t border-gray-200 sm:border-t-0 sm:pt-0">
            <ArrowUpDown className="h-4 w-4 text-gray-500 shrink-0" />
            <span className="text-sm text-gray-600 shrink-0">Sort:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="flex-1 min-w-[8rem] sm:flex-none px-3 py-2 sm:px-2 sm:py-1 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 max-w-full"
            >
              <option value="priority">Priority</option>
              <option value="updated">Recency</option>
            </select>
            <button
              type="button"
              onClick={() => setSortDirection((d) => (d === 'asc' ? 'desc' : 'asc'))}
              className="p-2.5 sm:p-1.5 text-gray-600 hover:bg-gray-100 rounded-md min-h-[44px] min-w-[44px] sm:min-h-0 sm:min-w-0 flex items-center justify-center shrink-0"
              title={sortDirection === 'asc' ? 'Descending' : 'Ascending'}
            >
              {sortDirection === 'asc' ? <ArrowUp className="h-4 w-4" /> : <ArrowDown className="h-4 w-4" />}
            </button>
          </div>
          <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer py-1 min-h-[44px] sm:min-h-0">
            <input
              type="checkbox"
              checked={groupByCluster}
              onChange={(e) => setGroupByCluster(e.target.checked)}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 shrink-0"
            />
            Group by cluster
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer py-1 min-h-[44px] sm:min-h-0">
            <input
              type="checkbox"
              checked={includeUnparentedTickets}
              onChange={(e) => setIncludeUnparentedTickets(e.target.checked)}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 shrink-0"
            />
            Include unparented tickets
          </label>
        </div>
      </div>

      {jiraStatus.configured && (
        <div className="mb-4 bg-slate-50 border border-slate-200 rounded-lg overflow-hidden min-w-0">
          <button
            type="button"
            onClick={() => setShowBacklogMetrics((s) => !s)}
            className="w-full flex items-center gap-2 px-3 py-2.5 text-left text-sm font-medium text-slate-800 hover:bg-slate-100/80"
            aria-expanded={showBacklogMetrics}
          >
            {showBacklogMetrics ? (
              <ChevronDown className="h-4 w-4 shrink-0 rotate-180" aria-hidden />
            ) : (
              <ChevronDown className="h-4 w-4 shrink-0" aria-hidden />
            )}
            Backlog metrics
          </button>
          {showBacklogMetrics && (
            <div className="px-3 pb-3 pt-2 border-t border-slate-200/80 space-y-4 text-xs text-slate-700">
              <section className="min-w-0">
                <h3 className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-1.5">
                  Data flow
                </h3>
                <dl className="space-y-1">
                  <div className="flex flex-col sm:flex-row sm:gap-2 sm:items-baseline">
                    <dt className="text-slate-500 shrink-0 sm:w-44">Fetch cap (requested)</dt>
                    <dd className="font-medium text-slate-900 tabular-nums">
                      {jiraParentFilterStats?.maxResultsRequested ?? 1000}
                    </dd>
                  </div>
                  <div className="flex flex-col sm:flex-row sm:gap-2 sm:items-baseline">
                    <dt className="text-slate-500 shrink-0 sm:w-44">Mapped from Jira (pages)</dt>
                    <dd className="font-medium text-slate-900 tabular-nums">
                      {jiraParentFilterStats
                        ? jiraParentFilterStats.parentFilterApplied
                          ? jiraParentFilterStats.countBefore
                          : jiraParentFilterStats.countAfter
                        : jiraLoading
                          ? '…'
                          : '—'}
                    </dd>
                  </div>
                  <div className="flex flex-col sm:flex-row sm:gap-2 sm:items-baseline">
                    <dt className="text-slate-500 shrink-0 sm:w-44">After parent/epic filter</dt>
                    <dd className="font-medium text-slate-900 tabular-nums">
                      {jiraParentFilterStats?.parentFilterApplied
                        ? jiraParentFilterStats.countAfter
                        : '— (include unparented is on)'}
                    </dd>
                  </div>
                  <div className="flex flex-col sm:flex-row sm:gap-2 sm:items-baseline">
                    <dt className="text-slate-500 shrink-0 sm:w-44">Loaded in app</dt>
                    <dd className="font-medium text-slate-900 tabular-nums">{issues.length}</dd>
                  </div>
                  <div className="flex flex-col sm:flex-row sm:gap-2 sm:items-baseline">
                    <dt className="text-slate-500 shrink-0 sm:w-44">Visible (filters)</dt>
                    <dd className="font-medium text-slate-900 tabular-nums">
                      {filteredAndSorted.length}
                      <span className="font-normal text-slate-500 ml-1">
                        (status / component / platform / cluster)
                      </span>
                    </dd>
                  </div>
                  {overviewMeta && (
                    <>
                      <div className="flex flex-col sm:flex-row sm:gap-2 sm:items-baseline pt-1 border-t border-slate-200/60">
                        <dt className="text-slate-500 shrink-0 sm:w-44">Submitted to AI overview</dt>
                        <dd className="font-medium text-slate-900 tabular-nums">
                          {Number.isFinite(Number(overviewMeta.submitted_count_after_parent_filter))
                            ? Number(overviewMeta.submitted_count_after_parent_filter)
                            : overviewMeta.submitted_count ?? '—'}
                        </dd>
                      </div>
                      <div className="flex flex-col sm:flex-row sm:gap-2 sm:items-baseline">
                        <dt className="text-slate-500 shrink-0 sm:w-44">Analyzed batch (cap)</dt>
                        <dd className="font-medium text-slate-900 tabular-nums">
                          {overviewMeta.issue_count ?? '—'}
                          {overviewMeta.truncated ? (
                            <span className="font-normal text-amber-800 ml-1">
                              (truncated from {overviewMeta.submitted_count ?? '—'} submitted)
                            </span>
                          ) : null}
                        </dd>
                      </div>
                    </>
                  )}
                </dl>
              </section>

              <section className="min-w-0">
                <h3 className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-1">
                  Visible backlog
                </h3>
                <p className="text-[11px] text-slate-500 mb-1.5">
                  Counts from Jira fields only — not from AI.
                </p>
                <div className="flex flex-wrap gap-2 items-start">
                  <div className="min-w-0 flex-1 basis-[min(100%,14rem)] sm:basis-[calc(50%-0.25rem)]">
                    <p className="text-[10px] font-semibold uppercase tracking-wide text-slate-500 mb-1">
                      By priority
                    </p>
                    <div className="overflow-x-auto border border-slate-200 rounded-md bg-white">
                      <table className="w-full text-left text-[11px] sm:text-xs border-collapse">
                        <thead>
                          <tr className="bg-slate-100/90">
                            <th className="px-2 py-1.5 font-semibold text-slate-700">Priority</th>
                            <th className="px-2 py-1.5 font-semibold text-slate-700 text-right">Count</th>
                          </tr>
                        </thead>
                        <tbody>
                          {visibleBacklogRollups.byPriority.length === 0 ? (
                            <tr>
                              <td colSpan={2} className="px-2 py-2 text-slate-500">
                                No issues in view
                              </td>
                            </tr>
                          ) : (
                            visibleBacklogRollups.byPriority.map((row) => (
                              <tr key={row.label} className="border-t border-slate-100">
                                <td className="px-2 py-1.5 text-slate-800">{row.label}</td>
                                <td className="px-2 py-1.5 text-right tabular-nums text-slate-900">
                                  {row.count}
                                </td>
                              </tr>
                            ))
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                  <div className="min-w-0 flex-1 basis-[min(100%,14rem)] sm:basis-[calc(50%-0.25rem)]">
                    <p className="text-[10px] font-semibold uppercase tracking-wide text-slate-500 mb-1">
                      By status
                    </p>
                    <div className="overflow-x-auto border border-slate-200 rounded-md bg-white max-h-40 overflow-y-auto">
                      <table className="w-full text-left text-[11px] sm:text-xs border-collapse">
                        <thead className="sticky top-0">
                          <tr className="bg-slate-100/90">
                            <th className="px-2 py-1.5 font-semibold text-slate-700">Status</th>
                            <th className="px-2 py-1.5 font-semibold text-slate-700 text-right">Count</th>
                          </tr>
                        </thead>
                        <tbody>
                          {visibleBacklogRollups.byStatus.length === 0 ? (
                            <tr>
                              <td colSpan={2} className="px-2 py-2 text-slate-500">
                                No issues in view
                              </td>
                            </tr>
                          ) : (
                            visibleBacklogRollups.byStatus.map((row) => (
                              <tr key={row.label} className="border-t border-slate-100">
                                <td className="px-2 py-1.5 text-slate-800 break-words">{row.label}</td>
                                <td className="px-2 py-1.5 text-right tabular-nums text-slate-900">
                                  {row.count}
                                </td>
                              </tr>
                            ))
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </section>

              {issues.length > 0 && filteredAndSorted.length !== issues.length && (
                <section className="min-w-0">
                  <h3 className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-1">
                    Loaded vs visible
                  </h3>
                  <p className="text-[11px] text-slate-500 mb-1.5">
                    Same rollups for the full loaded list ({issues.length} issues).
                  </p>
                  <div className="flex flex-wrap gap-2 items-start">
                    <div className="min-w-0 flex-1 basis-[min(100%,14rem)] sm:basis-[calc(50%-0.25rem)] overflow-x-auto border border-slate-200 rounded-md bg-white">
                      <table className="w-full text-left text-[11px] border-collapse">
                        <thead>
                          <tr className="bg-slate-100/90">
                            <th className="px-2 py-1 font-semibold">Priority</th>
                            <th className="px-2 py-1 font-semibold text-right">#</th>
                          </tr>
                        </thead>
                        <tbody>
                          {loadedBacklogRollups.byPriority.map((row) => (
                            <tr key={`ld-${row.label}`} className="border-t border-slate-100">
                              <td className="px-2 py-1">{row.label}</td>
                              <td className="px-2 py-1 text-right tabular-nums">{row.count}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                    <div className="min-w-0 flex-1 basis-[min(100%,14rem)] sm:basis-[calc(50%-0.25rem)] overflow-x-auto border border-slate-200 rounded-md bg-white max-h-32 overflow-y-auto">
                      <table className="w-full text-left text-[11px] border-collapse">
                        <thead>
                          <tr className="bg-slate-100/90">
                            <th className="px-2 py-1 font-semibold">Status</th>
                            <th className="px-2 py-1 font-semibold text-right">#</th>
                          </tr>
                        </thead>
                        <tbody>
                          {loadedBacklogRollups.byStatus.map((row) => (
                            <tr key={`ls-${row.label}`} className="border-t border-slate-100">
                              <td className="px-2 py-1 break-words">{row.label}</td>
                              <td className="px-2 py-1 text-right tabular-nums">{row.count}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </section>
              )}

              {overviewMeta?.snapshot_stats && typeof overviewMeta.snapshot_stats === 'object' && (
                <section className="min-w-0">
                  <h3 className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-1">
                    AI batch snapshot (deterministic)
                  </h3>
                  <p className="text-[11px] text-slate-500 mb-1.5">
                    Same subset as the markdown snapshot tables under Priority review; can be smaller than visible
                    backlog if the analysis cap applied.
                  </p>
                  <p className="text-xs font-medium text-slate-800 tabular-nums mb-1">
                    Total in batch: {overviewMeta.snapshot_stats.total ?? '—'}
                  </p>
                  <div className="flex flex-wrap gap-2 items-start">
                    <div className="min-w-0 flex-1 basis-[min(100%,14rem)] sm:basis-[calc(50%-0.25rem)] overflow-x-auto border border-slate-200 rounded-md bg-white">
                      <table className="w-full text-left text-[11px] border-collapse">
                        <thead>
                          <tr className="bg-slate-100/90">
                            <th className="px-2 py-1 font-semibold">Priority</th>
                            <th className="px-2 py-1 font-semibold text-right">#</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(overviewMeta.snapshot_stats.by_priority || {})
                            .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
                            .map(([label, n]) => (
                              <tr key={`ss-p-${label}`} className="border-t border-slate-100">
                                <td className="px-2 py-1 break-words">{label}</td>
                                <td className="px-2 py-1 text-right tabular-nums">{n}</td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>
                    <div className="min-w-0 flex-1 basis-[min(100%,14rem)] sm:basis-[calc(50%-0.25rem)] overflow-x-auto border border-slate-200 rounded-md bg-white max-h-32 overflow-y-auto">
                      <table className="w-full text-left text-[11px] border-collapse">
                        <thead>
                          <tr className="bg-slate-100/90">
                            <th className="px-2 py-1 font-semibold">Status</th>
                            <th className="px-2 py-1 font-semibold text-right">#</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(overviewMeta.snapshot_stats.by_status || {})
                            .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
                            .map(([label, n]) => (
                              <tr key={`ss-s-${label}`} className="border-t border-slate-100">
                                <td className="px-2 py-1 break-words">{label}</td>
                                <td className="px-2 py-1 text-right tabular-nums">{n}</td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </section>
              )}

              {overviewMeta?.scorecard_enabled && (
                <section className="min-w-0 mt-3 pt-2 border-t border-slate-200/80">
                  <h3 className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-1">
                    Scorecard triage
                  </h3>
                  <p className="text-[11px] text-slate-500 mb-2">
                    14-point scorecard (v2): five dimensions summed on the server; GA verdict and implied Jira
                    priority follow the rules below. Config hash identifies the framework version for comparing
                    runs.
                  </p>
                  {Array.isArray(overviewMeta.scorecard_threshold_summary) &&
                    overviewMeta.scorecard_threshold_summary.length > 0 && (
                      <ul className="list-disc pl-4 mb-2 text-[11px] text-slate-600 space-y-0.5">
                        {overviewMeta.scorecard_threshold_summary.map((line, idx) => (
                          <li key={idx}>{line}</li>
                        ))}
                      </ul>
                    )}
                  <dl className="grid gap-1 text-[11px] sm:text-xs text-slate-700 mb-3">
                    <div className="flex flex-wrap gap-x-2">
                      <dt className="text-slate-500">Schema</dt>
                      <dd className="font-mono tabular-nums">
                        {overviewMeta.scorecard_schema_version ?? '—'}
                      </dd>
                    </div>
                    <div className="flex flex-wrap gap-x-2">
                      <dt className="text-slate-500">Config hash</dt>
                      <dd className="font-mono text-[10px] break-all">
                        {overviewMeta.scorecard_config_hash || '—'}
                      </dd>
                    </div>
                    <div className="flex flex-wrap gap-x-2">
                      <dt className="text-slate-500">Shortlist / scored keys</dt>
                      <dd className="tabular-nums">
                        {overviewMeta.scorecard_shortlist_size ?? '—'} /{' '}
                        {overviewMeta.scorecard_scored_keys ?? '—'}
                      </dd>
                    </div>
                  </dl>
                  {Array.isArray(overviewMeta.scorecard_errors) &&
                    overviewMeta.scorecard_errors.length > 0 && (
                      <div className="mb-3 text-[11px] text-amber-900 bg-amber-50 border border-amber-200/80 rounded-md px-2 py-1.5">
                        <span className="font-semibold">Parse notes: </span>
                        {overviewMeta.scorecard_errors.join(' · ')}
                      </div>
                    )}
                  {(() => {
                    const sc = overviewMeta.scorecards_by_key;
                    if (!sc || typeof sc !== 'object') return null;
                    const entries = Object.entries(sc);
                    const withRec = entries.filter(([, v]) => v && v.recommendation);
                    const rest = entries.filter(([, v]) => !v || !v.recommendation);
                    const rowBlock = (key, v) => (
                      <details
                        key={key}
                        className="border border-slate-200 rounded-md bg-white mb-1.5 px-2 py-1"
                        open={Boolean(v.recommendation)}
                      >
                        <summary className="cursor-pointer text-[11px] font-medium text-slate-800">
                          {key}
                          {v.recommendation ? (
                            <span className="ml-2 font-normal text-slate-600">
                              {v.recommendation.action} → {v.recommendation.target} (total {v.raw_total}/14, GA:{' '}
                              {v.ga_verdict}, implied {v.implied_priority})
                            </span>
                          ) : (
                            <span className="ml-2 font-normal text-slate-500">
                              no rank-delta recommendation (total {v.raw_total}/14, GA: {v.ga_verdict}, implied{' '}
                              {v.implied_priority})
                            </span>
                          )}
                        </summary>
                        <div className="mt-1.5 text-[10px] text-slate-600 grid grid-cols-2 sm:grid-cols-3 gap-x-2 gap-y-0.5">
                          <span>feature_importance {v.feature_importance}/4</span>
                          <span>reach {v.reach}/3</span>
                          <span>technical_severity {v.technical_severity}/3</span>
                          <span>workaround_quality {v.workaround_quality}/2</span>
                          <span>regression_risk {v.regression_risk}/2</span>
                          <span className="col-span-2 sm:col-span-3 font-medium text-slate-700">
                            raw_total {v.raw_total}/14 · GA {v.ga_verdict} · implied Jira {v.implied_priority}
                          </span>
                          {(v.llm_raw_total != null && v.llm_raw_total !== v.raw_total) ||
                          (v.llm_ga_verdict && v.llm_ga_verdict !== v.ga_verdict) ||
                          (v.llm_jira_priority &&
                            String(v.llm_jira_priority).toLowerCase().replace(/\s+/g, '') !==
                              String(v.implied_priority || '').toLowerCase()) ? (
                            <span className="col-span-2 sm:col-span-3 text-amber-800">
                              LLM fields: raw_total {v.llm_raw_total ?? '—'}, ga {v.llm_ga_verdict ?? '—'}, jira{' '}
                              {v.llm_jira_priority ?? '—'} (server values above win for Raise/Lower)
                            </span>
                          ) : null}
                        </div>
                        {v.recommendation?.reason ? (
                          <p className="mt-1 text-[10px] text-slate-600 break-words">{v.recommendation.reason}</p>
                        ) : null}
                      </details>
                    );
                    return (
                      <div className="max-h-64 overflow-y-auto pr-0.5">
                        {withRec.length ? (
                          <p className="text-[10px] font-semibold text-slate-500 mb-1">Recommendations</p>
                        ) : null}
                        {withRec.map(([k, v]) => rowBlock(k, v))}
                        {rest.length ? (
                          <details className="mt-2 text-[11px]">
                            <summary className="cursor-pointer text-slate-600">
                              Other scored tickets ({rest.length})
                            </summary>
                            <div className="mt-1">{rest.map(([k, v]) => rowBlock(k, v))}</div>
                          </details>
                        ) : null}
                      </div>
                    );
                  })()}
                </section>
              )}
            </div>
          )}
        </div>
      )}

      {/* Triage Summary toggle & panel */}
      <div className="mb-4">
        <button
          type="button"
          onClick={() => setShowSummary((s) => !s)}
          className="text-sm font-medium text-blue-600 hover:text-blue-800 flex items-center gap-1"
        >
          {showSummary ? <ChevronDown className="h-4 w-4 rotate-180" /> : <ChevronDown className="h-4 w-4" />}
          Triage Summary
        </button>
        {showSummary && (
          <div className="mt-2 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="p-3 bg-white rounded border border-gray-200">
                <div className="text-xs text-gray-500 uppercase">GA blockers</div>
                <div className="text-xl font-semibold text-gray-900">{summaryData.gaBlockerCount}</div>
              </div>
              <div className="p-3 bg-white rounded border border-gray-200">
                <div className="text-xs text-gray-500 uppercase">By component</div>
                <ul className="text-sm text-gray-700 mt-1">
                  {Object.entries(summaryData.byComponent)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 5)
                    .map(([c, n]) => (
                      <li key={c}>{c}: {n}</li>
                    ))}
                </ul>
              </div>
              <div className="p-3 bg-white rounded border border-gray-200">
                <div className="text-xs text-gray-500 uppercase">By platform</div>
                <ul className="text-sm text-gray-700 mt-1">
                  {Object.entries(summaryData.byPlatform).map(([p, n]) => (
                    <li key={p}>{p}: {n}</li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="mb-2">
              <div className="text-xs text-gray-500 uppercase">Clusters with triaged issues</div>
              <div className="text-sm text-gray-700 mt-1">
                {summaryData.clustersReviewed.length
                  ? summaryData.clustersReviewed.join(', ')
                  : 'None yet'}
              </div>
            </div>
            {summaryData.overrides.length > 0 && (
              <div className="mb-2">
                <div className="text-xs text-gray-500 uppercase">Issues with overrides</div>
                <ul className="text-sm text-gray-700 mt-1 space-y-1">
                  {summaryData.overrides.map(({ key, decision }) => (
                    <li key={key}>
                      {key}: {decision.reasonForOverride || 'Override recorded'}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            <button
              type="button"
              onClick={() => {
                const payload = {
                  decisions,
                  summary: summaryData,
                  exportedAt: new Date().toISOString(),
                };
                navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
              }}
              className="flex items-center gap-2 px-3 py-2 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              <Copy className="h-4 w-4" /> Copy summary as JSON
            </button>
          </div>
        )}
      </div>

      {/* Backlog list */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-3 sm:p-4 min-w-0">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          {jiraLoading
            ? 'Backlog (Loading…)'
            : `Backlog (${filteredAndSorted.length} of ${issues.length} issues)`}
        </h2>
        {jiraParentFilterStats?.parentFilterApplied && !includeUnparentedTickets && (
          <p className="mb-3 text-xs text-gray-600">
            Showing tickets with parent/epic context only.
            {parentFilteredOutCount > 0 ? ` Filtered out ${parentFilteredOutCount} unparented tickets.` : ''}
          </p>
        )}

        {!jiraLoading && filteredAndSorted.length > 0 && (
          <div className="mb-4 bg-amber-50/60 border border-amber-200 rounded-lg overflow-hidden">
            <div className="flex flex-wrap items-start justify-between gap-2 p-3">
              <div className="min-w-0 flex-1 space-y-1.5">
                <div className="flex flex-wrap items-center gap-2 min-w-0 w-full">
                  <button
                    type="button"
                    onClick={() => setOverviewExpanded((e) => !e)}
                    className="flex items-center gap-2 text-left min-w-0 flex-1"
                    aria-expanded={overviewExpanded}
                  >
                    {overviewExpanded ? (
                      <ChevronDown className="h-4 w-4 text-amber-900 shrink-0 rotate-180 transition-transform" aria-hidden />
                    ) : (
                      <ChevronDown className="h-4 w-4 text-amber-900 shrink-0 transition-transform" aria-hidden />
                    )}
                    <span className="text-sm font-semibold text-amber-950">AI backlog overview</span>
                    {!overviewExpanded && overviewLoading && !overviewError && (
                      <span className="text-xs font-normal text-amber-800 truncate">
                        — {overviewMarkdown ? 'Partial · ' : ''}
                        {overviewProgressLabel || 'generating…'}
                      </span>
                    )}
                    {!overviewExpanded && overviewWaitingForOtherTab && !overviewLoading && !overviewError && (
                      <span className="text-xs font-medium text-amber-900 truncate">
                        — another tab is generating this overview…
                      </span>
                    )}
                    {!overviewExpanded && overviewError && !overviewLoading && (
                      <span className="text-xs font-normal text-red-700 truncate">— error (expand to view)</span>
                    )}
                    {!overviewExpanded &&
                      overviewMarkdown &&
                      !overviewLoading &&
                      !overviewError &&
                      !overviewWaitingForOtherTab && (
                        <span className="text-xs font-semibold text-amber-950 truncate">
                          — Summary ready — expand the panel or tap View summary
                        </span>
                      )}
                  </button>
                  {!overviewExpanded &&
                    overviewMarkdown &&
                    !overviewLoading &&
                    !overviewError &&
                    !overviewWaitingForOtherTab && (
                    <button
                      type="button"
                      onClick={() => setOverviewExpanded(true)}
                      className="shrink-0 text-xs font-semibold px-2.5 py-1 rounded-md border border-amber-600 bg-amber-200/90 text-amber-950 shadow-sm hover:bg-amber-300/90 focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-500"
                    >
                      View summary
                    </button>
                  )}
                </div>
                <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs">
                  <span className="text-amber-900">
                    Cards below pull Jira fields directly; AI recommendations are advisory.
                  </span>
                  {jiraParentFilterStats?.parentFilterApplied && !includeUnparentedTickets && (
                    <span className="text-amber-900/90">
                      Parent/epic-linked tickets only.
                    </span>
                  )}
                  {!overviewLoading && !overviewError && overviewMarkdown && (
                    <span className="inline-flex items-center rounded-full border border-amber-300 bg-white px-2 py-0.5 text-[11px] font-medium text-amber-900">
                      {overviewFreshnessLabel}
                    </span>
                  )}
                  {!overviewLoading && !overviewError && overviewMarkdown && overviewUpdatedLabel && (
                    <span className="inline-flex items-center rounded-full border border-emerald-300/90 bg-emerald-50 px-2 py-0.5 text-[11px] font-semibold text-emerald-950">
                      {overviewUpdatedLabel}
                    </span>
                  )}
                  {!overviewLoading && !overviewError && titleSuggestionsCount > 0 && (
                    <span className="inline-flex items-center rounded-full border border-amber-300 bg-amber-100/70 px-2 py-0.5 text-[11px] font-medium text-amber-950">
                      title suggestions: {titleSuggestionsCount}
                    </span>
                  )}
                  {!overviewLoading && !overviewError && overviewMeta?.title_rewrite_no_candidates && (
                    <span
                      className="inline-flex items-center rounded-full border border-dashed border-amber-400 bg-white px-2 py-0.5 text-[11px] font-medium text-amber-900"
                      title="Title scan ran; no issue keys were selected for proposed rewrites."
                    >
                      title rewrite: no candidates
                    </span>
                  )}
                  {overviewCacheHint && !overviewLoading && !overviewError && (
                    <span className="text-amber-800/85">{overviewCacheHint}</span>
                  )}
                </div>
                {overviewMarkdown && !overviewError && (
                  <p className="text-xs text-amber-900/90">
                    Fetch pipeline, visible vs analyzed counts, and deterministic priority/status tables: expand{' '}
                    <strong>Backlog metrics</strong> above.
                    {overviewLoading ? ' (AI batch counts fill in when generation finishes.)' : ''}
                  </p>
                )}
                {!overviewLoading && !overviewError && overviewMeta?.truncated && (
                  <p className="text-xs text-amber-800/90">
                    Analysis cap: batch smaller than submitted — see Backlog metrics.
                  </p>
                )}
                {!overviewLoading && !overviewError && overviewMeta?.overview_incomplete && (
                  <p className="text-xs text-amber-900 font-medium border border-amber-300/80 bg-amber-100/50 rounded px-2 py-1.5">
                    Partial overview: {overviewMeta.incomplete_reason || 'Later steps were skipped after pass 2.'}{' '}
                    {overviewMeta.omitted_sections?.length
                      ? `(Omitted: ${overviewMeta.omitted_sections.join(', ')})`
                      : ''}
                  </p>
                )}
                {!overviewExpanded && overviewPreviewText && !overviewError && (
                  <p className="text-xs text-amber-900/90 truncate">
                    {overviewPreviewText}
                  </p>
                )}
              </div>
              <div className="flex items-center gap-2 shrink-0 pt-0.5">
                {overviewExpanded && overviewLoading && (
                  <span className="text-xs text-amber-900 flex items-center gap-1 min-w-0">
                    <RefreshCw className="h-3.5 w-3.5 animate-spin shrink-0" aria-hidden />
                    <span className="truncate">{overviewProgressLabel || 'Generating…'}</span>
                  </span>
                )}
                <button
                  type="button"
                  disabled={overviewLoading}
                  onClick={() => {
                    if (overviewLoading) return;
                    const ownerId = ensureOverviewLockOwnerId();
                    if (!tryAcquireOverviewLock(backlogOverviewFingerprint, ownerId)) {
                      startOverviewCrossTabWait(backlogOverviewFingerprint);
                      return;
                    }
                    runBacklogOverview(
                      filteredAndSorted,
                      undefined,
                      backlogOverviewFingerprint,
                      ownerId,
                    );
                  }}
                  className="text-xs px-2 py-1 rounded border border-amber-300 bg-white text-amber-950 hover:bg-amber-100 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Regenerate
                </button>
              </div>
            </div>
            <div className="px-3 pb-3 border-t border-amber-200/60 bg-gradient-to-b from-amber-50/50 to-transparent">
              {(overviewLoading || overviewMarkdown || overviewMeta) && !overviewError && (
                <OverviewPhaseRail
                  loading={overviewLoading}
                  progress={overviewProgress}
                  meta={overviewMeta}
                  titlePipelineEnabled={
                    overviewMeta == null || overviewMeta.title_rewrite_enabled !== false
                  }
                />
              )}
            </div>
            <div className="px-3 pb-2">
              <button
                type="button"
                onClick={() => setShowPrioritizationPhilosophy((s) => !s)}
                className="text-xs text-amber-900 hover:text-amber-950 underline underline-offset-2"
                aria-expanded={showPrioritizationPhilosophy}
              >
                {showPrioritizationPhilosophy ? 'Hide' : 'How prioritization works'}
              </button>
            </div>
            {showPrioritizationPhilosophy && (
              <div className="mx-3 mb-3 rounded-md border border-amber-200/80 bg-white/80 px-3 py-2.5">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-amber-900">How prioritization works</h3>
                <ul className="mt-1.5 list-disc pl-4 space-y-1 text-xs text-amber-950/95">
                  <li>Canonical Jira ladder: Blocker, Critical, Major, Normal, Minor, Trivial.</li>
                  <li>Recommendations use Raise / Lower wording for Jira priority only.</li>
                  <li>Blocker is the ceiling; a current Blocker is never raised further.</li>
                  <li>Halo core risk gets more weight: containment, geofence behavior, pairing, and safety-relevant location accuracy.</li>
                  <li>Peripheral UX flows (like profile photo / optional onboarding polish) are usually not escalated without core safety impact.</li>
                </ul>
              </div>
            )}
            {overviewExpanded && (
              <div className="px-4 pb-4 pt-0 border-t border-amber-200/70 space-y-3">
                {overviewCacheHint && overviewMarkdown && !overviewLoading && !overviewError && (
                  <p className="text-xs text-amber-800/85">{overviewCacheHint}</p>
                )}
                {overviewMarkdown && !overviewError && (
                  <p className="text-xs text-amber-900/95">
                    Pass depth and counts: see <strong>Backlog metrics</strong> (Data flow + AI batch snapshot).
                    {overviewLoading ? ' Batch snapshot appears after generation completes.' : ''}
                  </p>
                )}
                {!overviewLoading && !overviewError && overviewMeta?.truncated && (
                  <p className="text-xs text-amber-800/90">
                    Analysis cap: see Backlog metrics for submitted vs analyzed.
                  </p>
                )}
                {!overviewLoading && !overviewError && overviewMeta?.overview_incomplete && (
                  <p className="text-xs text-amber-900 font-medium border border-amber-300/80 bg-amber-100/50 rounded px-2 py-1.5">
                    Partial overview: {overviewMeta.incomplete_reason || 'Later steps were skipped after pass 2.'}{' '}
                    {overviewMeta.omitted_sections?.length
                      ? `(Omitted: ${overviewMeta.omitted_sections.join(', ')})`
                      : ''}
                  </p>
                )}
                {overviewLoading && overviewMarkdown && !overviewError && (
                  <div
                    className="flex items-center gap-2 rounded-md border border-amber-200/90 bg-amber-100/50 px-3 py-2 text-xs text-amber-950"
                    role="status"
                    aria-live="polite"
                  >
                    <RefreshCw className="h-3.5 w-3.5 animate-spin shrink-0" aria-hidden />
                    <span>
                      Showing partial overview — still running{overviewProgressLabel ? `: ${overviewProgressLabel}` : '…'}
                      {overviewPartialMilestone ? (
                        <span className="ml-1 font-mono text-[10px] opacity-75">({overviewPartialMilestone})</span>
                      ) : null}
                    </span>
                  </div>
                )}
                {overviewError && (
                  <div className="flex items-start justify-between gap-2 rounded-md bg-red-50 border border-red-200 px-3 py-2">
                    <div className="text-sm text-red-800 flex-1 space-y-1" role="alert">
                      <p>{overviewError.message}</p>
                      {overviewError.failedStep && (
                        <p className="text-xs text-red-900/90">
                          Failed step:{' '}
                          <strong>{OVERVIEW_STEP_LABELS[overviewError.failedStep] || overviewError.failedStep}</strong>
                          {overviewError.completedSteps?.length
                            ? ` · Completed: ${overviewError.completedSteps.join(', ')}`
                            : ''}
                        </p>
                      )}
                      {overviewError.retryAfterSeconds != null && Number.isFinite(overviewError.retryAfterSeconds) && (
                        <p className="text-xs text-red-900/90">
                          Suggested wait: ~{Math.ceil(overviewError.retryAfterSeconds)}s before retry.
                        </p>
                      )}
                      {overviewError.errorCode && (
                        <p className="text-[11px] text-red-700/90 font-mono">{overviewError.errorCode}</p>
                      )}
                    </div>
                    <button
                      type="button"
                      onClick={() => setOverviewError(null)}
                      className="p-1 rounded text-red-700 hover:bg-red-100 shrink-0"
                      aria-label="Dismiss error"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                )}
                {overviewMarkdown && (
                  <div
                    className="markdown-content text-gray-800 text-sm overflow-x-auto max-w-full [&_h2]:mt-8 [&_h2]:text-base [&_h2]:font-semibold [&_h2]:mb-1 [&_h2]:text-gray-900 [&_h2:first-of-type]:mt-3 [&_h3]:text-sm [&_h3]:font-semibold [&_h3]:text-gray-800 [&_h3]:mt-4 [&_h3]:mb-1 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 [&_p]:my-1 [&_a]:text-blue-600 [&_a]:underline [&_a]:break-words [&_table]:mb-4 [&_table]:w-auto [&_table]:max-w-full [&_table]:min-w-max [&_table]:border-collapse [&_table]:text-sm [&_th]:border [&_th]:border-amber-300/80 [&_th]:bg-amber-100/90 [&_th]:px-2 [&_th]:py-1.5 [&_th]:text-left [&_th]:font-semibold [&_th]:text-amber-950 [&_td]:border [&_td]:border-amber-200 [&_td]:px-2 [&_td]:py-1.5 [&_td]:align-top [&_td]:text-gray-800 [&_.backlog-overview-snapshot-col_td]:whitespace-nowrap [&_.backlog-overview-snapshot-col_th]:whitespace-nowrap [&_tr.overview-priority-raise>td]:!bg-rose-50/90 [&_tr.overview-priority-raise>td]:!border-rose-100/85 [&_tr.overview-priority-lower>td]:!bg-emerald-50/80 [&_tr.overview-priority-lower>td]:!border-emerald-100/80 [&>table]:min-w-[min(100%,36rem)]"
                  >
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      rehypePlugins={[rehypeWrapBacklogSnapshotBlocks, rehypeAnnotateBacklogOverviewTables]}
                      components={backlogOverviewMarkdownComponents}
                    >
                      {overviewMarkdown}
                    </ReactMarkdown>
                  </div>
                )}
                {!overviewMarkdown && overviewLoading && (
                  <p className="text-xs text-amber-900/80">Analyzing filtered backlog with Claude…</p>
                )}
              </div>
            )}
          </div>
        )}

        {jiraLoading ? (
          <div className="flex flex-col items-center justify-center py-12 text-gray-500">
            <RefreshCw className="h-8 w-8 animate-spin text-gray-400 mb-3" />
            <p className="text-sm">Loading tickets…</p>
          </div>
        ) : filteredAndSorted.length === 0 ? (
          <div className="text-sm text-gray-500 py-8 text-center">
            No issues match the current filters. Adjust filters to see more.
          </div>
        ) : (
          listContent
        )}
      </div>

      {/* Mini detail drawer */}
      {miniDetailIssue && (
        <MiniDetailDrawer
          issue={miniDetailIssue}
          decisions={decisions}
          setDecisions={setDecisions}
          COMPONENTS={COMPONENTS}
          onClose={() => setMiniDetailIssue(null)}
          onFullEdit={() => {
            setSelectedIssue(miniDetailIssue);
            setMiniDetailIssue(null);
          }}
          jiraBaseUrl={jiraStatus.base_url || null}
          jiraTicketHref={jiraStatus.base_url ? `${jiraStatus.base_url}/browse/${miniDetailIssue.key}` : null}
        />
      )}
    </div>
  );
};

/** Parent issue and/or Epic Link from Jira (see jira_client _map_jira_issue_to_triage). */
function IssueParentEpicMeta({ issue, jiraBaseUrl, compact = false }) {
  const parentKey = issue.parentKey;
  const parentSummary = issue.parentSummary;
  const epicKey = issue.epicKey;
  const epicSummary = issue.epicSummary;
  const showEpic = epicKey && epicKey !== parentKey;
  if (!parentKey && !showEpic) return null;

  const browse = (key) => (jiraBaseUrl ? `${jiraBaseUrl}/browse/${key}` : null);
  const linkClass = compact
    ? 'text-blue-600 hover:text-blue-800 hover:underline font-mono'
    : 'text-blue-600 hover:text-blue-800 hover:underline font-mono text-sm';

  return (
    <div
      className={
        compact
          ? 'text-xs text-gray-600 space-y-0.5 mt-1.5'
          : 'text-sm text-gray-700 space-y-1.5 mt-2'
      }
    >
      {parentKey && (
        <div className="flex flex-wrap items-baseline gap-x-1 gap-y-0">
          <span className="text-gray-500 shrink-0 font-medium">Parent</span>
          {browse(parentKey) ? (
            <a
              href={browse(parentKey)}
              target="_blank"
              rel="noopener noreferrer"
              className={linkClass}
              onClick={(e) => e.stopPropagation()}
            >
              {parentKey}
            </a>
          ) : (
            <span className="font-mono text-gray-800">{parentKey}</span>
          )}
          {parentSummary && (
            <span className="text-gray-600 line-clamp-2 min-w-0" title={parentSummary}>
              — {parentSummary}
            </span>
          )}
        </div>
      )}
      {showEpic && (
        <div className="flex flex-wrap items-baseline gap-x-1 gap-y-0">
          <span className="text-gray-500 shrink-0 font-medium">Epic</span>
          {browse(epicKey) ? (
            <a
              href={browse(epicKey)}
              target="_blank"
              rel="noopener noreferrer"
              className={linkClass}
              onClick={(e) => e.stopPropagation()}
            >
              {epicKey}
            </a>
          ) : (
            <span className="font-mono text-gray-800">{epicKey}</span>
          )}
          {epicSummary && (
            <span className="text-gray-600 line-clamp-2 min-w-0" title={epicSummary}>
              — {epicSummary}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

function BacklogCard({ issue, triaged, onClick, jiraTicketHref, jiraBaseUrl }) {
  const rec = issue.aiRecommendation || {};
  const primaryText = rec.shortSummary ?? issue.title;
  const showTitleSecondary = rec.shortSummary != null && rec.shortSummary !== issue.title;
  const jiraComponents =
    issue.components?.length > 0
      ? issue.components
      : issue.component
        ? [issue.component]
        : [];

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
      className="p-4 rounded-lg border-2 border-gray-200 bg-white hover:border-gray-300 hover:shadow-md transition-all cursor-pointer flex flex-col h-full text-left"
    >
      <div className="flex items-center gap-2 flex-wrap mb-1">
        {jiraTicketHref ? (
          <a
            href={jiraTicketHref}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="font-mono text-sm text-blue-600 hover:text-blue-800 hover:underline inline-flex items-center gap-1"
            title="Open in Jira"
          >
            {issue.key}
            <ExternalLink className="h-3 w-3 shrink-0" />
          </a>
        ) : (
          <span className="font-mono text-sm text-gray-500">{issue.key}</span>
        )}
        {triaged && (
          <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full flex items-center gap-1">
            <CheckCircle className="h-3 w-3" /> Triaged
          </span>
        )}
        {issue.gaBlocker && (
          <span className="px-2 py-0.5 bg-red-100 text-red-700 text-xs rounded-full">GA blocker</span>
        )}
        {issue.needsMoreInfo && (
          <span className="px-2 py-0.5 bg-amber-100 text-amber-700 text-xs rounded-full">Needs more info</span>
        )}
        {issue.issuetype && (
          <span className={`px-2 py-0.5 text-xs rounded font-medium ${getIssuetypeBadgeClasses(issue.issuetype)}`} title="Issue type">
            {issue.issuetype}
          </span>
        )}
        {issue.priority && (
          <span className={`px-2 py-0.5 text-xs rounded font-medium ${getPriorityBadgeClasses(issue.priority)}`} title="Jira priority">
            {issue.priority}
          </span>
        )}
        {issue.status && (
          <span className={`px-2 py-0.5 text-xs rounded ${getStatusBadgeClasses(issue.status)}`} title="Status">
            {issue.status}
          </span>
        )}
      </div>
      {jiraComponents.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-1.5" aria-label="Jira components">
          {jiraComponents.map((c) => (
            <span
              key={c}
              className="px-2 py-0.5 text-xs font-medium rounded-md bg-indigo-50 text-indigo-900 border border-indigo-100"
              title="Jira component"
            >
              {c}
            </span>
          ))}
        </div>
      )}
      <IssueParentEpicMeta issue={issue} jiraBaseUrl={jiraBaseUrl} compact />
      <div
        className="font-medium text-gray-900 line-clamp-4 mb-0.5"
        title={issue.title || primaryText}
      >
        {primaryText}
      </div>
      {showTitleSecondary && (
        <div className="text-xs text-gray-500 line-clamp-2 mb-2" title={issue.title}>
          {issue.title}
        </div>
      )}
      {!showTitleSecondary && <div className="mb-2" />}
      {(issue.assignee || issue.sprint) && (
        <div className="text-xs text-gray-600 flex flex-wrap gap-x-3 gap-y-0.5 mt-1">
          {issue.assignee && <span title="Assignee">{issue.assignee}</span>}
          {issue.sprint && <span title="Sprint" className="text-violet-600">{issue.sprint}</span>}
        </div>
      )}
      {(rec.category != null || rec.component != null || rec.priority != null) && (
        <div className="mt-auto pt-2 border-t border-gray-100">
          <div className="text-xs text-gray-500 uppercase mb-0.5">Recommended</div>
          <div className="text-sm text-gray-700 flex flex-wrap gap-x-2 gap-y-0">
            {rec.category != null && <span className="text-blue-700">Category: {rec.category}</span>}
            {rec.component != null && <span className="text-blue-700">Component: {rec.component}</span>}
            {rec.priority != null && <span className="text-gray-600">Priority: {rec.priority}</span>}
          </div>
        </div>
      )}
    </div>
  );
}

function MiniDetailDrawer({ issue, decisions, setDecisions, COMPONENTS, onClose, onFullEdit, jiraTicketHref, jiraBaseUrl }) {
  const decision = decisions[issue.id] || {};
  const rec = issue.aiRecommendation || {};
  const getValue = (field) => {
    if (decision[field] !== undefined) return decision[field];
    if (field === 'category') return rec.category;
    if (field === 'component') return rec.component;
    return undefined;
  };
  const [showOverride, setShowOverride] = useState({});
  const [overrideReasons, setOverrideReasons] = useState({});
  const [overrideValue, setOverrideValue] = useState({ category: '', component: '' });

  const recordAccept = (field, value) => {
    setDecisions((prev) => ({
      ...prev,
      [issue.id]: {
        ...prev[issue.id],
        [field]: value,
        triagedAt: new Date().toISOString(),
      },
    }));
    setShowOverride((s) => ({ ...s, [field]: false }));
  };

  const recordOverride = (field, value, reason) => {
    setDecisions((prev) => ({
      ...prev,
      [issue.id]: {
        ...prev[issue.id],
        [field]: value,
        reasonForOverride: reason || prev[issue.id]?.reasonForOverride,
        triagedAt: new Date().toISOString(),
      },
    }));
    setOverrideReasons((r) => ({ ...r, [field]: '' }));
    setShowOverride((s) => ({ ...s, [field]: false }));
  };

  return (
    <>
      <div
        className="fixed inset-0 bg-black/30 z-40"
        role="button"
        tabIndex={0}
        onClick={onClose}
        onKeyDown={(e) => e.key === 'Escape' && onClose()}
        aria-label="Close drawer"
      />
      <div className="fixed top-0 right-0 bottom-0 w-full max-w-md bg-white shadow-xl z-50 flex flex-col border-l border-gray-200 overflow-hidden">
        <div className="p-4 border-b border-gray-200 flex items-center justify-between shrink-0">
          <h2 className="text-lg font-semibold text-gray-900">Quick triage</h2>
          <button
            type="button"
            onClick={onClose}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-md"
            aria-label="Close"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          <div>
            {jiraTicketHref ? (
              <a
                href={jiraTicketHref}
                target="_blank"
                rel="noopener noreferrer"
                className="font-mono text-sm text-blue-600 hover:text-blue-800 hover:underline inline-flex items-center gap-1"
                title="Open in Jira"
              >
                {issue.key}
                <ExternalLink className="h-3.5 w-3.5 shrink-0" />
              </a>
            ) : (
              <p className="font-mono text-sm text-gray-500">{issue.key}</p>
            )}
            <IssueParentEpicMeta issue={issue} jiraBaseUrl={jiraBaseUrl} />
            {rec.shortSummary ? (
              <>
                <h3 className="font-medium text-gray-900 mt-1">{rec.shortSummary}</h3>
                <p className="text-xs text-gray-500 mt-0.5" title={issue.title}>{issue.title}</p>
              </>
            ) : (
              <h3 className="font-medium text-gray-900 mt-1">{issue.title}</h3>
            )}
            {issue.description && (
              <p className="text-sm text-gray-600 mt-2 line-clamp-3">{issue.description}</p>
            )}
            <div className="flex flex-wrap gap-2 mt-2">
              {issue.priority && (
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${getPriorityBadgeClasses(issue.priority)}`} title="Priority">{issue.priority}</span>
              )}
              {issue.status && (
                <span className="px-2 py-0.5 bg-sky-50 text-sky-700 rounded text-xs" title="Status">{issue.status}</span>
              )}
              <span className="px-2 py-0.5 bg-gray-100 rounded text-xs">{issue.platform}</span>
              {(issue.components?.length ? issue.components : (issue.component ? [issue.component] : [])).map((c) => (
                <span key={c} className="px-2 py-0.5 bg-gray-100 rounded text-xs">{c}</span>
              ))}
              {issue.clusterLabel && (
                <span className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded text-xs">{issue.clusterLabel}</span>
              )}
            </div>
          </div>

          <div className="border-t border-gray-200 pt-4">
            <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center gap-1">
              <AlertCircle className="h-4 w-4 text-blue-600" />
              Recommended
            </h4>
            <div className="space-y-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-medium text-gray-600 w-20">Category</span>
                <span className="text-sm text-gray-900">{getValue('category') ?? rec.category ?? '—'}</span>
                {getValue('category') === undefined && rec.category != null && (
                  <>
                    {!showOverride.category ? (
                      <div className="flex gap-1">
                        <button
                          type="button"
                          onClick={() => recordAccept('category', rec.category)}
                          className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded hover:bg-green-200"
                        >
                          Accept
                        </button>
                        <button
                          type="button"
                          onClick={() => setShowOverride((s) => ({ ...s, category: true }))}
                          className="px-2 py-1 text-xs bg-amber-100 text-amber-800 rounded hover:bg-amber-200"
                        >
                          Override
                        </button>
                      </div>
                    ) : (
                      <div className="flex flex-wrap items-center gap-2">
                        <input
                          type="text"
                          placeholder="Category"
                          value={overrideValue.category}
                          onChange={(e) => setOverrideValue((v) => ({ ...v, category: e.target.value }))}
                          className="px-2 py-1 text-sm border border-gray-300 rounded w-28"
                        />
                        <input
                          type="text"
                          placeholder="Reason"
                          value={overrideReasons.category || ''}
                          onChange={(e) => setOverrideReasons((r) => ({ ...r, category: e.target.value }))}
                          className="px-2 py-1 text-sm border border-gray-300 rounded w-24"
                        />
                        <button
                          type="button"
                          onClick={() => recordOverride('category', overrideValue.category, overrideReasons.category)}
                          className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
                        >
                          Save
                        </button>
                        <button
                          type="button"
                          onClick={() => setShowOverride((s) => ({ ...s, category: false }))}
                          className="p-1 text-gray-500 hover:text-gray-700"
                        >
                          <X className="h-4 w-4" />
                        </button>
                      </div>
                    )}
                  </>
                )}
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-medium text-gray-600 w-20">Component</span>
                <span className="text-sm text-gray-900">{getValue('component') ?? rec.component ?? '—'}</span>
                {getValue('component') === undefined && rec.component != null && (
                  <>
                    {!showOverride.component ? (
                      <div className="flex gap-1">
                        <button
                          type="button"
                          onClick={() => recordAccept('component', rec.component)}
                          className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded hover:bg-green-200"
                        >
                          Accept
                        </button>
                        <button
                          type="button"
                          onClick={() => setShowOverride((s) => ({ ...s, component: true }))}
                          className="px-2 py-1 text-xs bg-amber-100 text-amber-800 rounded hover:bg-amber-200"
                        >
                          Override
                        </button>
                      </div>
                    ) : (
                      <div className="flex flex-wrap items-center gap-2">
                        <select
                          value={overrideValue.component}
                          onChange={(e) => setOverrideValue((v) => ({ ...v, component: e.target.value }))}
                          className="px-2 py-1 text-sm border border-gray-300 rounded"
                        >
                          <option value="">Select...</option>
                          {COMPONENTS.map((c) => (
                            <option key={c} value={c}>{c}</option>
                          ))}
                        </select>
                        <input
                          type="text"
                          placeholder="Reason"
                          value={overrideReasons.component || ''}
                          onChange={(e) => setOverrideReasons((r) => ({ ...r, component: e.target.value }))}
                          className="px-2 py-1 text-sm border border-gray-300 rounded w-24"
                        />
                        <button
                          type="button"
                          onClick={() => recordOverride('component', overrideValue.component, overrideReasons.component)}
                          className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
                        >
                          Save
                        </button>
                        <button
                          type="button"
                          onClick={() => setShowOverride((s) => ({ ...s, component: false }))}
                          className="p-1 text-gray-500 hover:text-gray-700"
                        >
                          <X className="h-4 w-4" />
                        </button>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onFullEdit}
              className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg"
            >
              <ChevronRight className="h-4 w-4" />
              Full edit
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

function BugTriageDetail({ issue, allIssues, decisions, setDecisions, onBack, NEXT_ACTIONS, COMPONENTS, jiraTicketHref, jiraBaseUrl }) {
  const decision = decisions[issue.id] || {};
  const rec = useMemo(() => issue.aiRecommendation || {}, [issue.aiRecommendation]);
  const getValue = (field) => {
    if (decision[field] !== undefined) return decision[field];
    if (field === 'category') return rec.category;
    if (field === 'component') return rec.component;
    if (field === 'priority') return rec.priority;
    if (field === 'gaBlocker') return rec.gaBlocker;
    if (field === 'nextAction') return rec.suggestedNextAction;
    return undefined;
  };
  const [overrideReasons, setOverrideReasons] = useState({});
  const [showOverride, setShowOverride] = useState({});

  const duplicateIssues = useMemo(() => {
    const keys = rec.duplicateCandidates || issue.relatedIssueIds || [];
    return keys
      .map((k) => allIssues.find((i) => i.key === k || i.id === k))
      .filter(Boolean);
  }, [allIssues, issue, rec]);

  const recordAccept = (field, value) => {
    setDecisions((prev) => ({
      ...prev,
      [issue.id]: {
        ...prev[issue.id],
        [field]: value,
        triagedAt: new Date().toISOString(),
      },
    }));
    setShowOverride((s) => ({ ...s, [field]: false }));
  };

  const recordOverride = (field, value, reason) => {
    setDecisions((prev) => ({
      ...prev,
      [issue.id]: {
        ...prev[issue.id],
        [field]: value,
        reasonForOverride: reason || prev[issue.id]?.reasonForOverride,
        triagedAt: new Date().toISOString(),
      },
    }));
    setOverrideReasons((r) => ({ ...r, [field]: '' }));
    setShowOverride((s) => ({ ...s, [field]: false }));
  };

  return (
    <div className="px-3 py-4 sm:p-6 max-w-4xl mx-auto min-w-0">
      <button
        type="button"
        onClick={onBack}
        className="mb-4 flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors min-h-[44px] sm:min-h-0"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to backlog
      </button>

      <div className="space-y-6">
        {/* Core summary */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Summary
          </h2>
          <h1 className="text-xl font-bold text-gray-900 mb-2">{issue.title}</h1>
          {jiraTicketHref ? (
            <a
              href={jiraTicketHref}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-600 hover:text-blue-800 hover:underline font-mono mb-2 inline-flex items-center gap-1"
              title="Open in Jira"
            >
              {issue.key}
              <ExternalLink className="h-3.5 w-3.5 shrink-0" />
            </a>
          ) : (
            <p className="text-sm text-gray-500 font-mono mb-2">{issue.key}</p>
          )}
          <IssueParentEpicMeta issue={issue} jiraBaseUrl={jiraBaseUrl} />
          {(issue.priority || issue.status) && (
            <div className="flex flex-wrap gap-2 mb-2">
              {issue.priority && (
                <span className={`px-2 py-1 rounded text-sm font-medium ${getPriorityBadgeClasses(issue.priority)}`} title="Priority">{issue.priority}</span>
              )}
              {issue.status && (
                <span className="px-2 py-1 bg-sky-50 text-sky-700 rounded text-sm" title="Status">{issue.status}</span>
              )}
            </div>
          )}
          {issue.description && (
            <p className="text-gray-700 mb-2">{issue.description}</p>
          )}
          {issue.expectedVsActual && (
            <div className="mt-2 p-3 bg-amber-50 border border-amber-200 rounded text-sm">
              <strong>Expected vs actual:</strong> {issue.expectedVsActual}
            </div>
          )}
          {issue.reproSteps && issue.reproSteps.length > 0 && (
            <div className="mt-3">
              <div className="text-sm font-medium text-gray-700 mb-1">Repro steps</div>
              <ol className="list-decimal list-inside text-sm text-gray-600 space-y-1">
                {issue.reproSteps.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ol>
            </div>
          )}
          <div className="mt-3 flex flex-wrap gap-2 text-sm">
            <span className="px-2 py-1 bg-gray-100 rounded">{issue.platform}</span>
            {(issue.components?.length ? issue.components : (issue.component ? [issue.component] : [])).map((c) => (
              <span key={c} className="px-2 py-1 bg-gray-100 rounded">{c}</span>
            ))}
            {issue.clusterLabel && (
              <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded">{issue.clusterLabel}</span>
            )}
          </div>
        </div>

        {/* AI recommendations + Accept/Override */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-blue-600" />
            AI recommendations
          </h2>
          {rec.rationale && (
            <p className="text-sm text-gray-600 mb-4 p-3 bg-blue-50 rounded border border-blue-100">
              <strong>Why:</strong> {rec.rationale}
            </p>
          )}
          <div className="space-y-4">
            <RecommendationRow
              label="Category"
              recommended={rec.category}
              value={getValue('category')}
              onAccept={() => recordAccept('category', rec.category)}
              onOverride={(v, reason) => recordOverride('category', v, reason)}
              showOverride={showOverride.category}
              setShowOverride={(v) => setShowOverride((s) => ({ ...s, category: v }))}
              overrideReason={overrideReasons.category}
              setOverrideReason={(v) => setOverrideReasons((r) => ({ ...r, category: v }))}
            />
            <RecommendationRow
              label="Component"
              recommended={rec.component}
              value={getValue('component')}
              onAccept={() => recordAccept('component', rec.component)}
              onOverride={(v, reason) => recordOverride('component', v, reason)}
              showOverride={showOverride.component}
              setShowOverride={(v) => setShowOverride((s) => ({ ...s, component: v }))}
              overrideReason={overrideReasons.component}
              setOverrideReason={(v) => setOverrideReasons((r) => ({ ...r, component: v }))}
              options={COMPONENTS}
            />
            <RecommendationRow
              label="Priority"
              recommended={rec.priority}
              value={getValue('priority')}
              onAccept={() => recordAccept('priority', rec.priority)}
              onOverride={(v, reason) => recordOverride('priority', v, reason)}
              showOverride={showOverride.priority}
              setShowOverride={(v) => setShowOverride((s) => ({ ...s, priority: v }))}
              overrideReason={overrideReasons.priority}
              setOverrideReason={(v) => setOverrideReasons((r) => ({ ...r, priority: v }))}
              options={['P0', 'P1', 'P2', 'P3']}
            />
            <RecommendationRow
              label="GA blocker"
              recommended={rec.gaBlocker != null ? (rec.gaBlocker ? 'Yes' : 'No') : '—'}
              value={getValue('gaBlocker') != null ? (getValue('gaBlocker') ? 'Yes' : 'No') : undefined}
              onAccept={() => recordAccept('gaBlocker', rec.gaBlocker)}
              onOverride={(v, reason) => recordOverride('gaBlocker', v === 'Yes', reason)}
              showOverride={showOverride.gaBlocker}
              setShowOverride={(v) => setShowOverride((s) => ({ ...s, gaBlocker: v }))}
              overrideReason={overrideReasons.gaBlocker}
              setOverrideReason={(v) => setOverrideReasons((r) => ({ ...r, gaBlocker: v }))}
              options={['Yes', 'No']}
            />
            <RecommendationRow
              label="Suggested next action"
              recommended={rec.suggestedNextAction}
              value={getValue('nextAction')}
              onAccept={() => recordAccept('nextAction', rec.suggestedNextAction)}
              onOverride={(v, reason) => recordOverride('nextAction', v, reason)}
              showOverride={showOverride.nextAction}
              setShowOverride={(v) => setShowOverride((s) => ({ ...s, nextAction: v }))}
              overrideReason={overrideReasons.nextAction}
              setOverrideReason={(v) => setOverrideReasons((r) => ({ ...r, nextAction: v }))}
              options={NEXT_ACTIONS}
            />
          </div>
          {rec.confidence && (
            <p className="text-xs text-gray-500 mt-2">Confidence: {rec.confidence}</p>
          )}
        </div>

        {/* Duplicates / cluster */}
        {(duplicateIssues.length > 0 || issue.clusterLabel) && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Duplicates & cluster</h2>
            {issue.clusterLabel && (
              <p className="text-sm text-gray-600 mb-2">
                <strong>Cluster:</strong> {issue.clusterLabel}
              </p>
            )}
            {duplicateIssues.length > 0 && (
              <div className="text-sm">
                <strong>Possible duplicates:</strong>
                <ul className="mt-2 space-y-1">
                  {duplicateIssues.map((dup) => (
                    <li key={dup.id}>
                      <button
                        type="button"
                        className="text-blue-600 hover:underline"
                        onClick={() => {}}
                      >
                        {dup.key}: {dup.title}
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Reason for override (global) */}
        {(decision.reasonForOverride || Object.keys(decision).some((k) => k !== 'triagedAt' && decision[k] !== undefined)) && (
          <div className="bg-gray-50 rounded-lg border border-gray-200 p-4">
            <div className="text-sm font-medium text-gray-700 mb-1">Your decisions</div>
            {decision.reasonForOverride && (
              <p className="text-sm text-gray-600">Reason for override: {decision.reasonForOverride}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function RecommendationRow({
  label,
  recommended,
  value,
  onAccept,
  onOverride,
  showOverride,
  setShowOverride,
  overrideReason,
  setOverrideReason,
  options,
}) {
  const [overrideValue, setOverrideValue] = useState(options && options[0] ? options[0] : '');
  const displayValue = value !== undefined && value !== null ? String(value) : recommended ?? '—';

  const handleSaveOverride = () => {
    if (options && options.length) {
      if (options.includes('Yes') && options.includes('No')) {
        onOverride(overrideValue, overrideReason);
      } else {
        onOverride(overrideValue, overrideReason);
      }
    } else {
      onOverride(overrideValue, overrideReason);
    }
  };

  return (
    <div className="flex flex-wrap items-start gap-2 py-2 border-b border-gray-100 last:border-0">
      <div className="w-32 text-sm font-medium text-gray-700 shrink-0">{label}</div>
      <div className="flex-1 min-w-0">
        <span className="text-gray-900">{displayValue}</span>
        {recommended != null && value === undefined && (
          <span className="text-gray-400 text-xs ml-2">(recommended: {String(recommended)})</span>
        )}
      </div>
      <div className="flex items-center gap-2 shrink-0">
        {!showOverride ? (
          <>
            <button
              type="button"
              onClick={onAccept}
              className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded hover:bg-green-200"
            >
              Accept
            </button>
            <button
              type="button"
              onClick={() => setShowOverride(true)}
              className="px-2 py-1 text-xs bg-amber-100 text-amber-800 rounded hover:bg-amber-200"
            >
              Override
            </button>
          </>
        ) : (
          <div className="flex flex-wrap items-center gap-2">
            {options && options.length > 0 ? (
              <select
                value={overrideValue}
                onChange={(e) => setOverrideValue(e.target.value)}
                className="px-2 py-1 text-sm border border-gray-300 rounded"
              >
                <option value="">Select...</option>
                {options.map((o) => (
                  <option key={o} value={o}>{o}</option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                placeholder="New value"
                value={overrideValue}
                onChange={(e) => setOverrideValue(e.target.value)}
                className="px-2 py-1 text-sm border border-gray-300 rounded w-32"
              />
            )}
            <input
              type="text"
              placeholder="Reason for override"
              value={overrideReason || ''}
              onChange={(e) => setOverrideReason(e.target.value)}
              className="px-2 py-1 text-sm border border-gray-300 rounded w-40"
            />
            <button
              type="button"
              onClick={handleSaveOverride}
              className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
            >
              Save override
            </button>
            <button type="button" onClick={() => setShowOverride(false)} className="p-1 text-gray-500 hover:text-gray-700">
              <X className="h-4 w-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default BugTriageCopilot;
