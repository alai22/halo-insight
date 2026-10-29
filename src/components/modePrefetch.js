const loadNeckFit = () => import('./neckFit/NeckFitModelingTool');
const loadLabeling = () => import('./LabelingDataDashboard');
const loadCollarLogs = () => import('./CollarLogsDashboard');
const loadBugTriage = () => import('./BugTriageCopilot');
const loadChurnTrends = () => import('./ChurnTrendsChart');
const loadConversationTrends = () => import('./ConversationTrendsChart');
const loadAnalytics = () => import('./AnalyticsDashboard');
const loadSurveyManager = () => import('./SurveyManager');
const loadSurveyHub = () => import('./surveys/SurveyHub');
const loadTextInterview = () => import('./interview/TextInterviewHub');
const loadZoom = () => import('./ZoomDownloadManager');
const loadApiData = () => import('./ApiDataManager');
const loadDownload = () => import('./DownloadManager');
const loadJiraStatus = () => import('./JiraStatusView');

export const modeLoaders = {
  'neck-fit-modeler': loadNeckFit,
  'labeling-data': loadLabeling,
  'collar-logs': loadCollarLogs,
  'bug-triage': loadBugTriage,
  'churn-trends': loadChurnTrends,
  'conversation-trends': loadConversationTrends,
  analytics: loadAnalytics,
  'survey-manager': loadSurveyManager,
  'halo-surveys': loadSurveyHub,
  'text-interview': loadTextInterview,
  zoom: loadZoom,
  'api-data-manager': loadApiData,
  download: loadDownload,
  'jira-status': loadJiraStatus,
};

/** Start loading a tab's chunk before the click commits, so the swap feels immediate. */
export function prefetchMode(modeId) {
  const load = modeLoaders[modeId];
  if (load) load();
}
