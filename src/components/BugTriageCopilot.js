import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
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
    const params = new URLSearchParams({ project: 'HALO', max_results: '500' });
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
  const [filterGaBlocker, setFilterGaBlocker] = useState(false);
  const [filterComponent, setFilterComponent] = useState('');
  const [filterPlatform, setFilterPlatform] = useState('');
  const [filterCluster, setFilterCluster] = useState('');
  const [filterNeedsMoreInfo, setFilterNeedsMoreInfo] = useState(false);
  const [sortBy, setSortBy] = useState('updated');
  const [sortDirection, setSortDirection] = useState('desc');
  const [groupByCluster, setGroupByCluster] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [viewMode, setViewMode] = useState('detailed'); // 'compact' | 'detailed'

  const clusters = useMemo(() => {
    const set = new Set();
    issues.forEach((i) => i.clusterLabel && set.add(i.clusterLabel));
    return Array.from(set).sort();
  }, [issues]);

  const filteredAndSorted = useMemo(() => {
    let list = [...issues];
    if (filterGaBlocker) list = list.filter((i) => i.gaBlocker);
    if (filterComponent) list = list.filter((i) => i.component === filterComponent);
    if (filterPlatform) list = list.filter((i) => i.platform === filterPlatform);
    if (filterCluster) list = list.filter((i) => i.clusterLabel === filterCluster);
    if (filterNeedsMoreInfo) list = list.filter((i) => i.needsMoreInfo);

    const mult = sortDirection === 'asc' ? 1 : -1;
    list.sort(
      (a, b) =>
        mult *
        (new Date(a.updated || a.created).getTime() - new Date(b.updated || b.created).getTime())
    );
    return list;
  }, [
    issues,
    filterGaBlocker,
    filterComponent,
    filterPlatform,
    filterCluster,
    filterNeedsMoreInfo,
    sortBy,
    sortDirection,
  ]);

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

  const summaryData = useMemo(() => {
    const triagedIds = new Set(Object.keys(decisions));
    const byComponent = {};
    const byPlatform = {};
    let gaBlockerCount = 0;
    const clustersReviewed = new Set();
    const overrides = [];
    issues.forEach((i) => {
      if (i.gaBlocker) gaBlockerCount++;
      byComponent[i.component] = (byComponent[i.component] || 0) + 1;
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
        jiraTicketHref={jiraStatus.base_url ? `${jiraStatus.base_url}/browse/${selectedIssue.key}` : null}
      />
    );
  }

  // Backlog view
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
              <BacklogCard
                key={issue.id}
                issue={issue}
                triaged={isTriaged(issue.id)}
                viewMode={viewMode}
                onClick={() => setMiniDetailIssue(issue)}
                jiraTicketHref={jiraStatus.base_url ? `${jiraStatus.base_url}/browse/${issue.key}` : null}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  ) : (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
      {filteredAndSorted.map((issue) => (
        <BacklogCard
          key={issue.id}
          issue={issue}
          triaged={isTriaged(issue.id)}
          viewMode={viewMode}
          onClick={() => setMiniDetailIssue(issue)}
          jiraTicketHref={jiraStatus.base_url ? `${jiraStatus.base_url}/browse/${issue.key}` : null}
        />
      ))}
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Bug className="h-7 w-7 text-amber-600" />
          Bug Triage Copilot
        </h1>
        <p className="text-gray-600 mt-1">
          Review and triage bugs with AI suggestions (Jira HALO)
        </p>
      </div>

      {/* Jira controls */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-4">
        <div className="flex flex-wrap items-center gap-3">
          {jiraLoading && (
            <span className="text-sm text-gray-500">Loading…</span>
          )}
          {!jiraLoading && !jiraError && issues.length > 0 && (
            <span className="text-sm text-green-700">{issues.length} issues loaded from Jira</span>
          )}
          {jiraError && (
            <span className="text-sm text-red-600">{jiraError}</span>
          )}
          {jiraStatus.configured && (
            <>
              <button
                type="button"
                onClick={fetchJiraIssues}
                disabled={jiraLoading}
                className="inline-flex items-center gap-1 px-2 py-1 text-xs text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded disabled:opacity-50"
                title="Refresh issues from Jira"
              >
                <RefreshCw className={`h-3.5 w-3.5 ${jiraLoading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-sm text-gray-500">Under issue:</span>
                <input
                  type="text"
                  value={jiraAncestorKey}
                  onChange={(e) => setJiraAncestorKey(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && fetchJiraIssues()}
                  placeholder="e.g. HALO-23306"
                  className="px-2 py-1 text-sm border border-gray-300 rounded-md w-36 font-mono focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  title="Show only children, grandchildren, etc. of this issue"
                />
                <button
                  type="button"
                  onClick={fetchJiraIssues}
                  disabled={jiraLoading}
                  className="px-2 py-1 text-xs text-white bg-blue-600 hover:bg-blue-700 rounded disabled:opacity-50"
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
                    className="px-2 py-1 text-xs text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded disabled:opacity-50"
                  >
                    Clear
                  </button>
                )}
                {jiraAncestorKey.trim() && jiraStatus.base_url && (
                  <a
                    href={`${jiraStatus.base_url}/browse/${jiraAncestorKey.trim()}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-blue-600 hover:underline inline-flex items-center gap-0.5"
                  >
                    Open in Jira
                    <ExternalLink className="h-3 w-3" />
                  </a>
                )}
              </div>
            </>
          )}
          {!jiraStatus.configured && (
            <span className="text-xs text-gray-500">Jira: configure .env to enable</span>
          )}
        </div>
      </div>

      {/* Filters & sort */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-4">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-sm font-medium text-gray-700 flex items-center gap-1">
            <Filter className="h-4 w-4" /> Filters
          </span>
          <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
            <input
              type="checkbox"
              checked={filterGaBlocker}
              onChange={(e) => setFilterGaBlocker(e.target.checked)}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            GA blocker
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
            <input
              type="checkbox"
              checked={filterNeedsMoreInfo}
              onChange={(e) => setFilterNeedsMoreInfo(e.target.checked)}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            Needs more info
          </label>
          <select
            value={filterComponent}
            onChange={(e) => setFilterComponent(e.target.value)}
            className="px-2 py-1 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All components</option>
            {COMPONENTS.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <select
            value={filterPlatform}
            onChange={(e) => setFilterPlatform(e.target.value)}
            className="px-2 py-1 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All platforms</option>
            {PLATFORMS.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
          <select
            value={filterCluster}
            onChange={(e) => setFilterCluster(e.target.value)}
            className="px-2 py-1 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All clusters</option>
            {clusters.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <div className="h-5 border-l border-gray-300" />
          <div className="flex items-center gap-2">
            <ArrowUpDown className="h-4 w-4 text-gray-500" />
            <span className="text-sm text-gray-600">Sort:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-2 py-1 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            >
              <option value="updated">Recency</option>
            </select>
            <button
              type="button"
              onClick={() => setSortDirection((d) => (d === 'asc' ? 'desc' : 'asc'))}
              className="p-1.5 text-gray-600 hover:bg-gray-100 rounded-md"
              title={sortDirection === 'asc' ? 'Descending' : 'Ascending'}
            >
              {sortDirection === 'asc' ? <ArrowUp className="h-4 w-4" /> : <ArrowDown className="h-4 w-4" />}
            </button>
          </div>
          <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
            <input
              type="checkbox"
              checked={groupByCluster}
              onChange={(e) => setGroupByCluster(e.target.checked)}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            Group by cluster
          </label>
          <div className="h-5 border-l border-gray-300" />
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">View:</span>
            <button
              type="button"
              onClick={() => setViewMode('compact')}
              className={`px-2 py-1 text-sm rounded-md ${viewMode === 'compact' ? 'bg-gray-200 font-medium text-gray-900' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              Compact
            </button>
            <button
              type="button"
              onClick={() => setViewMode('detailed')}
              className={`px-2 py-1 text-sm rounded-md ${viewMode === 'detailed' ? 'bg-gray-200 font-medium text-gray-900' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              Detailed
            </button>
          </div>
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
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Backlog ({filteredAndSorted.length} of {issues.length} issues)
        </h2>
        {filteredAndSorted.length === 0 ? (
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
          jiraTicketHref={jiraStatus.base_url ? `${jiraStatus.base_url}/browse/${miniDetailIssue.key}` : null}
        />
      )}
    </div>
  );
};

function BacklogCard({ issue, triaged, viewMode = 'detailed', onClick, jiraTicketHref }) {
  const rec = issue.aiRecommendation || {};
  const primaryText = rec.shortSummary ?? issue.title;
  const showTitleSecondary = rec.shortSummary != null && rec.shortSummary !== issue.title;
  const isCompact = viewMode === 'compact';

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
        {issue.priority && (
          <span className="px-2 py-0.5 bg-slate-100 text-slate-700 text-xs rounded font-medium" title="Jira priority">
            {issue.priority}
          </span>
        )}
        {issue.status && (
          <span className="px-2 py-0.5 bg-sky-50 text-sky-700 text-xs rounded" title="Workflow state">
            {issue.status}
          </span>
        )}
      </div>
      <div className="font-medium text-gray-900 line-clamp-2 mb-0.5">{primaryText}</div>
      {showTitleSecondary && (
        <div className="text-xs text-gray-500 line-clamp-1 mb-2" title={issue.title}>
          {issue.title}
        </div>
      )}
      {!showTitleSecondary && !isCompact && <div className="mb-2" />}
      {isCompact ? (
        <div className="mt-auto pt-1 flex items-center gap-2 flex-wrap">
          {issue.priority && <span className="text-xs text-slate-600">{issue.priority}</span>}
          {issue.status && <span className="text-xs text-sky-600">{issue.status}</span>}
          {(rec.component != null || rec.category != null) && (
            <span className="text-xs text-blue-700">
              {[rec.category, rec.component].filter(Boolean).join(' · ')}
            </span>
          )}
        </div>
      ) : (
        <>
          <div className="text-sm text-gray-500 flex flex-wrap gap-x-3 gap-y-1 mb-2">
            {issue.priority && <span title="Priority">{issue.priority}</span>}
            {issue.status && <span title="Status">{issue.status}</span>}
            <span>{issue.component}</span>
            <span>{issue.platform}</span>
            {issue.clusterLabel && <span>{issue.clusterLabel}</span>}
          </div>
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
          <div className="text-xs text-gray-400 mt-2">
            {issue.updated ? new Date(issue.updated).toLocaleDateString() : new Date(issue.created).toLocaleDateString()}
          </div>
        </>
      )}
    </div>
  );
}

function MiniDetailDrawer({ issue, decisions, setDecisions, COMPONENTS, onClose, onFullEdit, jiraTicketHref }) {
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
                <span className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded text-xs font-medium" title="Priority">{issue.priority}</span>
              )}
              {issue.status && (
                <span className="px-2 py-0.5 bg-sky-50 text-sky-700 rounded text-xs" title="Workflow state">{issue.status}</span>
              )}
              <span className="px-2 py-0.5 bg-gray-100 rounded text-xs">{issue.platform}</span>
              <span className="px-2 py-0.5 bg-gray-100 rounded text-xs">{issue.component}</span>
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

function BugTriageDetail({ issue, allIssues, decisions, setDecisions, onBack, NEXT_ACTIONS, COMPONENTS, jiraTicketHref }) {
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
    <div className="p-6 max-w-4xl mx-auto">
      <button
        type="button"
        onClick={onBack}
        className="mb-4 flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
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
          {(issue.priority || issue.status) && (
            <div className="flex flex-wrap gap-2 mb-2">
              {issue.priority && (
                <span className="px-2 py-1 bg-slate-100 text-slate-700 rounded text-sm font-medium" title="Priority">{issue.priority}</span>
              )}
              {issue.status && (
                <span className="px-2 py-1 bg-sky-50 text-sky-700 rounded text-sm" title="Workflow state">{issue.status}</span>
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
            <span className="px-2 py-1 bg-gray-100 rounded">{issue.component}</span>
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
