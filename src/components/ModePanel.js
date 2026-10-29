import React, { lazy, memo, Suspense } from 'react';
import ConversationDisplay from './ConversationDisplay';
import Tools from './Tools';
import { getSurveyBuilderId } from '../utils/routes';
import { modeLoaders } from './modePrefetch';

const NeckFitModelingTool = lazy(modeLoaders['neck-fit-modeler']);
const LabelingDataDashboard = lazy(modeLoaders['labeling-data']);
const CollarLogsDashboard = lazy(modeLoaders['collar-logs']);
const BugTriageCopilot = lazy(modeLoaders['bug-triage']);
const ChurnTrendsChart = lazy(modeLoaders['churn-trends']);
const ConversationTrendsChart = lazy(modeLoaders['conversation-trends']);
const AnalyticsDashboard = lazy(modeLoaders.analytics);
const SurveyManager = lazy(modeLoaders['survey-manager']);
const SurveyHub = lazy(modeLoaders['halo-surveys']);
const SurveyBuilder = lazy(() => import('./surveys/SurveyBuilder'));
const TextInterviewHub = lazy(modeLoaders['text-interview']);
const ZoomDownloadManager = lazy(modeLoaders.zoom);
const ApiDataManager = lazy(modeLoaders['api-data-manager']);
const DownloadManager = lazy(modeLoaders.download);
const JiraStatusView = lazy(modeLoaders['jira-status']);

function PanelFallback() {
  return (
    <div className="flex items-center justify-center h-64 text-sm text-gray-500">
      Loading…
    </div>
  );
}

function ModePanel({
  mode,
  adminMode,
  conversations,
  isLoading,
  error,
  pathname,
  setCurrentMode,
  setAdminMode,
}) {
  const chatMode = adminMode || mode;
  const chat = conversations[chatMode] || [];

  let content;
  if (mode === 'bug-triage') {
    content = <BugTriageCopilot />;
  } else if (mode === 'jira-status') {
    content = <JiraStatusView setCurrentMode={setCurrentMode} />;
  } else if (mode === 'api-data-manager') {
    content = <ApiDataManager />;
  } else if (mode === 'survey-manager') {
    content = <SurveyManager />;
  } else if (mode === 'zoom') {
    content = <ZoomDownloadManager />;
  } else if (mode === 'analytics') {
    content = <AnalyticsDashboard />;
  } else if (mode === 'labeling-data') {
    content = <LabelingDataDashboard />;
  } else if (mode === 'collar-logs') {
    content = <CollarLogsDashboard />;
  } else if (adminMode === 'download') {
    content = <DownloadManager />;
  } else if (adminMode === 'claude') {
    content = (
      <ConversationDisplay conversations={chat} isLoading={isLoading} error={error} />
    );
  } else if (mode === 'tools') {
    content = (
      <Tools
        currentMode={mode}
        setCurrentMode={setCurrentMode}
        adminMode={adminMode}
        setAdminMode={setAdminMode}
      />
    );
  } else if (mode === 'text-interview') {
    content = <TextInterviewHub />;
  } else if (mode === 'halo-surveys') {
    const surveyId = getSurveyBuilderId(pathname);
    content = surveyId ? <SurveyBuilder surveyId={surveyId} /> : <SurveyHub />;
  } else if (mode === 'neck-fit-modeler') {
    content = <NeckFitModelingTool />;
  } else if (mode === 'churn-trends') {
    content = <ChurnTrendsChart />;
  } else if (mode === 'conversation-trends') {
    content = <ConversationTrendsChart />;
  } else {
    content = (
      <ConversationDisplay conversations={chat} isLoading={isLoading} error={error} />
    );
  }

  return <Suspense fallback={<PanelFallback />}>{content}</Suspense>;
}

export default memo(ModePanel);
