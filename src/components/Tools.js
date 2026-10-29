import React from 'react';
import { prefetchMode } from './modePrefetch';
import {
  Download,
  Database,
  Bot,
  TrendingUp,
  Video,
  Activity,
  ExternalLink,
  Tags,
  Search,
  MessageSquare,
  BarChart3,
  FileText,
  Users,
  ClipboardList,
  Cpu,
  Bug,
  Home,
  FolderOpen,
} from 'lucide-react';

const Tools = ({ currentMode, setCurrentMode, adminMode, setAdminMode }) => {
  const openTool = (mode, nextAdminMode = null) => {
    setAdminMode(nextAdminMode);
    setCurrentMode(mode);
  };

  const sections = [
    {
      id: 'hardware',
      title: 'Hardware',
      description: 'Device fit modeling and collar logs',
      tools: [
        {
          id: 'neck-fit-modeler',
          name: 'Neck Fit Modeler',
          description: 'Hardware fit modeling tools',
          icon: Cpu,
          color: 'text-slate-700',
          bgColor: 'bg-slate-50',
          borderColor: 'border-slate-200',
          action: () => openTool('neck-fit-modeler'),
        },
        {
          id: 'collar-logs',
          name: 'Collar Logs',
          description: 'Inventory of collar logs copied into S3, by dataset and serial',
          icon: FolderOpen,
          color: 'text-sky-700',
          bgColor: 'bg-sky-50',
          borderColor: 'border-sky-200',
          action: () => openTool('collar-logs'),
        },
      ],
    },
    {
      id: 'research',
      title: 'Product Research',
      description: 'Churn, surveys, and interviews',
      tools: [
        {
          id: 'churn-trends',
          name: 'Churn Trends',
          description: 'Visualize cancellation trends',
          icon: BarChart3,
          color: 'text-red-600',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          action: () => openTool('churn-trends'),
        },
        {
          id: 'survicate',
          name: 'Ask About Churn',
          description: 'AI analysis of cancellation surveys',
          icon: FileText,
          color: 'text-teal-600',
          bgColor: 'bg-teal-50',
          borderColor: 'border-teal-200',
          action: () => openTool('survicate'),
        },
        {
          id: 'survey-manager',
          name: 'Survicate Surveys',
          description: 'Browse and manage Survicate survey data',
          icon: ClipboardList,
          color: 'text-orange-600',
          bgColor: 'bg-orange-50',
          borderColor: 'border-orange-200',
          action: () => openTool('survey-manager'),
        },
        {
          id: 'halo-surveys',
          name: 'Halo Surveys',
          description: 'Design and publish branded survey campaigns',
          icon: ClipboardList,
          color: 'text-amber-600',
          bgColor: 'bg-amber-50',
          borderColor: 'border-amber-200',
          action: () => openTool('halo-surveys'),
        },
        {
          id: 'text-interview',
          name: 'Text Interviews',
          description: 'Run structured text-based research interviews',
          icon: Users,
          color: 'text-violet-600',
          bgColor: 'bg-violet-50',
          borderColor: 'border-violet-200',
          action: () => openTool('text-interview'),
        },
      ],
    },
    {
      id: 'data',
      title: 'Data & integrations',
      description: 'Downloads, analytics, and connected services',
      tools: [
        {
          id: 'api-data-manager',
          name: 'Survicate Download Manager',
          description: 'Download survey data from Survicate API',
          icon: Database,
          color: 'text-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          action: () => openTool('api-data-manager'),
        },
        {
          id: 'download',
          name: 'Gladly Download Manager',
          description: 'Download conversation data from Gladly API',
          icon: Download,
          color: 'text-orange-600',
          bgColor: 'bg-orange-50',
          borderColor: 'border-orange-200',
          action: () => openTool('tools', 'download'),
        },
        {
          id: 'zoom',
          name: 'Zoom Download Manager',
          description: 'Download chat messages from Zoom API',
          icon: Video,
          color: 'text-indigo-600',
          bgColor: 'bg-indigo-50',
          borderColor: 'border-indigo-200',
          action: () => openTool('zoom'),
        },
        {
          id: 'analytics',
          name: 'Analytics Dashboard',
          description: 'View visitor and pageview analytics',
          icon: Activity,
          color: 'text-cyan-600',
          bgColor: 'bg-cyan-50',
          borderColor: 'border-cyan-200',
          action: () => openTool('analytics'),
        },
        {
          id: 'jira-status',
          name: 'Jira connection',
          description: 'Check if Jira (HALO) issues can be fetched for Bug Triage',
          icon: ExternalLink,
          color: 'text-amber-600',
          bgColor: 'bg-amber-50',
          borderColor: 'border-amber-200',
          action: () => openTool('jira-status'),
        },
      ],
    },
    {
      id: 'engineering',
      title: 'Engineering',
      description: 'Triage and internal utilities',
      tools: [
        {
          id: 'bug-triage',
          name: 'Bug Triage',
          description: 'Triage HALO issues with Jira context',
          icon: Bug,
          color: 'text-rose-600',
          bgColor: 'bg-rose-50',
          borderColor: 'border-rose-200',
          action: () => openTool('bug-triage'),
        },
        {
          id: 'claude',
          name: 'Claude Chat',
          description: 'Direct Claude API interaction (no RAG)',
          icon: Bot,
          color: 'text-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          action: () => openTool('tools', 'claude'),
        },
      ],
    },
    {
      id: 'gladly',
      title: 'Gladly conversations',
      description: 'Support conversation search, kept here for when you need it',
      quiet: true,
      tools: [
        {
          id: 'conversation-trends',
          name: 'Conversation Trends',
          description: 'Visualize conversation topic trends',
          icon: TrendingUp,
          color: 'text-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          action: () => openTool('conversation-trends'),
        },
        {
          id: 'conversations',
          name: 'Search Conversations',
          description: 'Search Gladly conversation data',
          icon: Search,
          color: 'text-green-600',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          action: () => openTool('conversations'),
        },
        {
          id: 'ask',
          name: 'Ask About Conversations',
          description: 'AI analysis of conversation data',
          icon: MessageSquare,
          color: 'text-purple-600',
          bgColor: 'bg-purple-50',
          borderColor: 'border-purple-200',
          action: () => openTool('ask'),
        },
      ],
    },
  ];

  const isToolActive = (tool) => {
    if (tool.id === 'download') return adminMode === 'download';
    if (tool.id === 'claude') return adminMode === 'claude';
    if (tool.id === 'tools') return false;
    return currentMode === tool.id && !adminMode;
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-gray-100">
            <Home className="h-5 w-5 text-gray-700" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Halo Insight</h1>
        </div>
        <p className="text-gray-600">
          Labeling Data is the main workspace. Research, hardware, triage, and the rest of the toolkit stay available below.
        </p>
      </div>

      <button
        type="button"
        onClick={() => openTool('labeling-data')}
        onPointerEnter={() => prefetchMode('labeling-data')}
        onFocus={() => prefetchMode('labeling-data')}
        className={`mb-10 w-full rounded-xl border-2 p-6 text-left transition-all hover:shadow-md ${
          currentMode === 'labeling-data' && !adminMode
            ? 'border-emerald-400 bg-emerald-50'
            : 'border-emerald-200 bg-emerald-50/70 hover:border-emerald-300'
        }`}
      >
        <div className="flex items-start gap-4">
          <div className="rounded-lg bg-emerald-100 p-3">
            <Tags className="h-6 w-6 text-emerald-700" />
          </div>
          <div className="min-w-0 flex-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-emerald-700">Featured</p>
            <h2 className="mt-1 text-xl font-semibold text-gray-900">Labeling Data</h2>
            <p className="mt-1 text-sm text-gray-600">
              Activity labeling inventory, collar dump coverage, and duration totals.
            </p>
            <span className="mt-3 inline-flex text-sm font-medium text-emerald-800">Open labeling</span>
          </div>
        </div>
      </button>

      <div className="space-y-10">
        {sections.map((section) => (
          <section key={section.id} className={section.quiet ? 'border-t border-gray-200 pt-8' : undefined}>
            <div className="mb-4">
              <h2 className={section.quiet ? 'text-base font-medium text-gray-600' : 'text-lg font-semibold text-gray-900'}>
                {section.title}
              </h2>
              <p className="text-sm text-gray-500">{section.description}</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {section.tools.map((tool) => {
                const Icon = tool.icon;
                const isActive = isToolActive(tool);

                return (
                  <button
                    key={tool.id}
                    type="button"
                    onClick={tool.action}
                    onPointerEnter={() => prefetchMode(tool.id)}
                    onFocus={() => prefetchMode(tool.id)}
                    className={`${section.quiet ? 'p-4' : 'p-5'} border-2 rounded-lg text-left transition-all hover:shadow-md ${
                      isActive
                        ? `${tool.bgColor} ${tool.borderColor}`
                        : section.quiet
                          ? 'bg-white border-gray-100 hover:border-gray-200'
                          : 'bg-white border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-start space-x-4">
                      <div className={`p-3 rounded-lg ${isActive ? tool.bgColor : 'bg-gray-50'}`}>
                        <Icon className={`h-5 w-5 ${isActive ? tool.color : 'text-gray-600'}`} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2 mb-1">
                          <h3
                            className={`text-base font-semibold ${
                              isActive ? tool.color : 'text-gray-900'
                            }`}
                          >
                            {tool.name}
                          </h3>
                          {isActive ? (
                            <span
                              className={`text-xs px-2 py-1 rounded shrink-0 ${tool.bgColor} ${tool.color} font-medium`}
                            >
                              Active
                            </span>
                          ) : null}
                        </div>
                        <p className="text-sm text-gray-600">{tool.description}</p>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
};

export default Tools;
