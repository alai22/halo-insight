import React, { useState, useEffect, useMemo } from 'react';
import {
  ArrowLeft,
  Bug,
  CheckCircle,
  ChevronDown,
  ClipboardList,
  Filter,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  FileText,
  AlertCircle,
  Copy,
  X,
} from 'lucide-react';
import {
  mockBugIssues,
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
  const [issues] = useState(() => mockBugIssues);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [decisions, setDecisionsState] = useState(loadDecisions);

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
  const [sortBy, setSortBy] = useState('rank');
  const [sortDirection, setSortDirection] = useState('desc');
  const [groupByCluster, setGroupByCluster] = useState(false);
  const [showSummary, setShowSummary] = useState(false);

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
    if (sortBy === 'rank') {
      list.sort((a, b) => mult * ((a.rank ?? 0) - (b.rank ?? 0)));
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
          <div className="space-y-2">
            {items.map((issue) => (
              <BacklogRow
                key={issue.id}
                issue={issue}
                triaged={isTriaged(issue.id)}
                onClick={() => setSelectedIssue(issue)}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  ) : (
    <div className="space-y-2">
      {filteredAndSorted.map((issue) => (
        <BacklogRow
          key={issue.id}
          issue={issue}
          triaged={isTriaged(issue.id)}
          onClick={() => setSelectedIssue(issue)}
        />
      ))}
    </div>
  );

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

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Bug className="h-7 w-7 text-amber-600" />
          Bug Triage Copilot
        </h1>
        <p className="text-gray-600 mt-1">Review and triage bugs with AI suggestions (mock data)</p>
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
              <option value="rank">Rank</option>
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
          <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer ml-auto">
            <input
              type="checkbox"
              checked={groupByCluster}
              onChange={(e) => setGroupByCluster(e.target.checked)}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
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
    </div>
  );
};

function BacklogRow({ issue, triaged, onClick }) {
  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
      className="p-4 rounded-lg border-2 border-gray-200 bg-gray-50 hover:border-gray-300 hover:shadow-md transition-all cursor-pointer flex items-center justify-between gap-4"
    >
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="font-mono text-sm text-gray-500">{issue.key}</span>
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
        </div>
        <div className="font-medium text-gray-900 mt-1 truncate">{issue.title}</div>
        <div className="text-sm text-gray-500 mt-1 flex flex-wrap gap-x-4 gap-y-0">
          <span>{issue.component}</span>
          <span>{issue.platform}</span>
          {issue.clusterLabel && <span>{issue.clusterLabel}</span>}
          <span>Rank {issue.rank ?? '—'}</span>
        </div>
      </div>
      <div className="text-right text-sm text-gray-500 shrink-0">
        {issue.updated ? new Date(issue.updated).toLocaleDateString() : new Date(issue.created).toLocaleDateString()}
      </div>
    </div>
  );
}

function BugTriageDetail({ issue, allIssues, decisions, setDecisions, onBack, NEXT_ACTIONS, COMPONENTS }) {
  const decision = decisions[issue.id] || {};
  const rec = issue.aiRecommendation || {};
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
          <p className="text-sm text-gray-500 font-mono mb-2">{issue.key}</p>
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
