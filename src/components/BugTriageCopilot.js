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
} from 'lucide-react';
import {
  PLATFORMS,
  COMPONENTS,
  NEXT_ACTIONS,
} from '../data/bugTriageMockData';

const STORAGE_KEY = 'bug_triage_decisions';

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
 * Arrow + emphasis in the Jira priority recommendation column; ticket column links when base URL is known.
 */
function createBacklogOverviewMarkdownComponents(jiraBaseUrl) {
  const base = jiraBaseUrl && String(jiraBaseUrl).replace(/\/+$/, '');
  return {
    td({ node, children, ...props }) {
      const col = node?.properties?.dataOverviewCol;

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
        return <td {...props}>{children}</td>;
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
        return <td {...props}>{children}</td>;
      }
      const className = [props.className, extraClass].filter(Boolean).join(' ');
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
  if (p === 'critical') return 'bg-red-200 text-red-900';
  if (p === 'major' || p === 'high') return 'bg-amber-100 text-amber-800';
  if (p === 'medium') return 'bg-slate-100 text-slate-700';
  if (p === 'normal') return 'bg-sky-100 text-sky-800';
  if (p === 'minor') return 'bg-emerald-100 text-emerald-800';
  if (p === 'low' || p === 'lowest' || p === 'trivial') return 'bg-gray-100 text-gray-600';
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
  const [overviewMarkdown, setOverviewMarkdown] = useState(null);
  const [overviewLoading, setOverviewLoading] = useState(false);
  const [overviewError, setOverviewError] = useState(null);
  const [overviewExpanded, setOverviewExpanded] = useState(false);

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
    const ancestor = (jiraAncestorKeyRef.current || '').trim();
    if (ancestor) params.set('ancestor_key', ancestor);
    fetch(`/api/jira/issues?${params}`)
      .then((res) => res.json().then((data) => ({ status: res.status, data })))
      .then(({ status, data }) => {
        if (status !== 200 || data.status !== 'success') {
          setJiraError(data.message || 'Failed to load issues from Jira');
          setIssues([]);
          return;
        }
        setIssues(Array.isArray(data.data) ? data.data : []);
      })
      .catch((err) => {
        setJiraError(err.message || 'Failed to fetch Jira issues');
        setIssues([]);
      })
      .finally(() => setJiraLoading(false));
  }, [jiraStatus.configured]);

  // Fetch issues when Jira is configured
  useEffect(() => {
    if (!jiraStatus.configured) return;
    fetchJiraIssues();
  }, [jiraStatus.configured, fetchJiraIssues]);

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

  const runBacklogOverview = useCallback(async (list, signal) => {
    if (!list.length) {
      setOverviewMarkdown(null);
      setOverviewError(null);
      setOverviewLoading(false);
      return;
    }
    setOverviewLoading(true);
    setOverviewError(null);
    try {
      const slim = list.map(slimIssueForOverview);
      const res = await fetch('/api/jira/backlog-overview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ issues: slim }),
        signal,
      });
      const data = await res.json().catch(() => ({}));
      if (signal?.aborted) return;
      if (!res.ok || data.status !== 'success') {
        setOverviewError(data.message || 'Failed to generate backlog overview');
        setOverviewMarkdown(null);
        return;
      }
      setOverviewMarkdown(typeof data.overview === 'string' ? data.overview : '');
    } catch (e) {
      if (e.name === 'AbortError') return;
      setOverviewError(e.message || 'Request failed');
      setOverviewMarkdown(null);
    } finally {
      setOverviewLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!jiraStatus.configured || jiraLoading) return;
    if (filteredAndSorted.length === 0) {
      setOverviewMarkdown(null);
      setOverviewError(null);
      setOverviewLoading(false);
      return;
    }
    const ac = new AbortController();
    const timer = setTimeout(() => {
      runBacklogOverview(filteredAndSorted, ac.signal);
    }, 500);
    return () => {
      clearTimeout(timer);
      ac.abort();
    };
  }, [jiraStatus.configured, jiraLoading, backlogOverviewFingerprint, filteredAndSorted, runBacklogOverview]);

  const backlogOverviewMarkdownComponents = useMemo(
    () => createBacklogOverviewMarkdownComponents(jiraStatus.base_url),
    [jiraStatus.base_url],
  );

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
        </div>
      </div>

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

        {!jiraLoading && filteredAndSorted.length > 0 && (
          <div className="mb-4 bg-amber-50/60 border border-amber-200 rounded-lg overflow-hidden">
            <div className="flex flex-wrap items-center justify-between gap-2 p-3">
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
                {!overviewExpanded && overviewLoading && (
                  <span className="text-xs font-normal text-amber-800 truncate">
                    — generating…
                  </span>
                )}
                {!overviewExpanded && overviewError && !overviewLoading && (
                  <span className="text-xs font-normal text-red-700 truncate">— error (expand to view)</span>
                )}
                {!overviewExpanded && overviewMarkdown && !overviewLoading && !overviewError && (
                  <span className="text-xs font-normal text-amber-800/90 truncate">— ready, click to expand</span>
                )}
              </button>
              <div className="flex items-center gap-2 shrink-0">
                {overviewExpanded && overviewLoading && (
                  <span className="text-xs text-amber-900 flex items-center gap-1">
                    <RefreshCw className="h-3.5 w-3.5 animate-spin shrink-0" aria-hidden />
                    Generating…
                  </span>
                )}
                <button
                  type="button"
                  disabled={overviewLoading}
                  onClick={() => runBacklogOverview(filteredAndSorted)}
                  className="text-xs px-2 py-1 rounded border border-amber-300 bg-white text-amber-950 hover:bg-amber-100 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Regenerate
                </button>
              </div>
            </div>
            {overviewExpanded && (
              <div className="px-4 pb-4 pt-0 border-t border-amber-200/70 space-y-3">
                {overviewError && (
                  <div className="flex items-start justify-between gap-2 rounded-md bg-red-50 border border-red-200 px-3 py-2">
                    <p className="text-sm text-red-800 flex-1" role="alert">
                      {overviewError}
                    </p>
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
                    className="markdown-content text-gray-800 text-sm overflow-x-auto max-w-full [&_h2]:mt-8 [&_h2]:text-base [&_h2]:font-semibold [&_h2]:mb-1 [&_h2]:text-gray-900 [&_h2:first-of-type]:mt-3 [&_h3]:text-sm [&_h3]:font-semibold [&_h3]:text-gray-800 [&_h3]:mt-4 [&_h3]:mb-1 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 [&_p]:my-1 [&_a]:text-blue-600 [&_a]:underline [&_a]:break-words [&_table]:mb-4 [&_table]:w-auto [&_table]:max-w-full [&_table]:min-w-0 [&_table]:border-collapse [&_table]:text-sm [&_th]:border [&_th]:border-amber-300/80 [&_th]:bg-amber-100/90 [&_th]:px-2 [&_th]:py-1.5 [&_th]:text-left [&_th]:font-semibold [&_th]:text-amber-950 [&_td]:border [&_td]:border-amber-200 [&_td]:px-2 [&_td]:py-1.5 [&_td]:align-top [&_td]:text-gray-800 [&_.backlog-overview-snapshot-col_td]:whitespace-nowrap [&_.backlog-overview-snapshot-col_th]:whitespace-nowrap [&_tr.overview-priority-raise>td]:!bg-rose-50/90 [&_tr.overview-priority-raise>td]:!border-rose-100/85 [&_tr.overview-priority-lower>td]:!bg-emerald-50/80 [&_tr.overview-priority-lower>td]:!border-emerald-100/80 [&>table]:min-w-[min(100%,36rem)]"
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
