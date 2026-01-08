import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search, MessageSquare, BarChart3, FileText, TrendingUp, Wrench, List } from 'lucide-react';

const TabNavigation = ({ currentMode, setCurrentMode, adminMode }) => {
  const [, setSearchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState(() => {
    // Determine active tab based on current mode
    if (['conversations', 'ask', 'conversation-trends'].includes(currentMode)) {
      return 'gladly';
    } else if (['churn-trends', 'survicate'].includes(currentMode)) {
      return 'churn';
    } else if (currentMode === 'survey-manager') {
      return 'surveys';
    } else if (['api-data-manager', 'tools', 'analytics'].includes(currentMode) || adminMode === 'download' || adminMode === 'claude') {
      return 'tools';
    }
    // Default to gladly if mode doesn't match
    return 'gladly';
  });

  // Update active tab when currentMode or adminMode changes externally
  useEffect(() => {
    if (['conversations', 'ask', 'conversation-trends'].includes(currentMode)) {
      setActiveTab('gladly');
    } else if (['churn-trends', 'survicate'].includes(currentMode)) {
      setActiveTab('churn');
    } else if (currentMode === 'survey-manager') {
      setActiveTab('surveys');
    } else if (['api-data-manager', 'tools', 'analytics'].includes(currentMode) || adminMode === 'download' || adminMode === 'claude') {
      setActiveTab('tools');
    }
  }, [currentMode, adminMode]);

  const gladlyModes = [
    {
      id: 'conversation-trends',
      name: 'Conversation Trends',
      description: 'Visualize conversation topic trends',
      icon: TrendingUp,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200'
    },
    {
      id: 'conversations',
      name: 'Search Conversations',
      description: 'Search Gladly conversation data',
      icon: Search,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200'
    },
    {
      id: 'ask',
      name: 'Ask About Conversations',
      description: 'AI analysis of conversation data',
      icon: MessageSquare,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200'
    }
  ];

  const churnModes = [
    {
      id: 'churn-trends',
      name: 'Churn Trends',
      description: 'Visualize cancellation trends',
      icon: BarChart3,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200'
    },
    {
      id: 'survicate',
      name: 'Ask About Churn',
      description: 'AI analysis of cancellation surveys',
      icon: FileText,
      color: 'text-teal-600',
      bgColor: 'bg-teal-50',
      borderColor: 'border-teal-200'
    }
  ];

  const handleModeChange = (modeId) => {
    setCurrentMode(modeId);
    setSearchParams({ mode: modeId });
  };

  return (
    <div className="flex flex-col space-y-3">
      {/* Main Tabs */}
      <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
        <button
          onClick={() => {
            setActiveTab('gladly');
            // Switch to first mode of the tab if current mode is from other tab
            if (!['conversations', 'ask', 'conversation-trends'].includes(currentMode)) {
              const defaultMode = 'conversation-trends';
              setCurrentMode(defaultMode);
              setSearchParams({ mode: defaultMode });
            }
          }}
          className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-colors ${
            activeTab === 'gladly'
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Gladly Conversations
        </button>
        <button
          onClick={() => {
            setActiveTab('churn');
            // Switch to first mode of the tab if current mode is from other tab
            if (!['churn-trends', 'survicate'].includes(currentMode)) {
              const defaultMode = 'churn-trends';
              setCurrentMode(defaultMode);
              setSearchParams({ mode: defaultMode });
            }
          }}
          className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-colors ${
            activeTab === 'churn'
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Churn Analysis
        </button>
        <button
          onClick={() => {
            setActiveTab('surveys');
            // Switch to survey manager if current mode is from other tab
            if (currentMode !== 'survey-manager') {
              const defaultMode = 'survey-manager';
              setCurrentMode(defaultMode);
              setSearchParams({ mode: defaultMode });
            }
          }}
          className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-colors ${
            activeTab === 'surveys'
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Survicate Surveys
        </button>
        <button
          onClick={() => {
            setActiveTab('tools');
            // Switch to tools mode if current mode is from other tab
            if (!['api-data-manager', 'tools', 'analytics'].includes(currentMode) && adminMode !== 'download' && adminMode !== 'claude') {
              const defaultMode = 'tools';
              setCurrentMode(defaultMode);
              setSearchParams({ mode: defaultMode });
            }
          }}
          className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-colors ${
            activeTab === 'tools'
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Tools
        </button>
      </div>

      {/* Sub-options for active tab */}
      {activeTab !== 'tools' && activeTab !== 'surveys' && (
        <div className="flex space-x-2">
          {(activeTab === 'gladly' ? gladlyModes : churnModes).map((mode) => {
            const Icon = mode.icon;
            const isActive = currentMode === mode.id;
            
            return (
              <button
                key={mode.id}
                onClick={() => handleModeChange(mode.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg border-2 transition-all ${
                  isActive
                    ? `${mode.bgColor} ${mode.borderColor} border-2 ${mode.color}`
                    : 'bg-white border-gray-200 text-gray-700 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? mode.color : 'text-gray-500'}`} />
                <div className="text-left">
                  <div className={`text-sm font-medium ${isActive ? mode.color : 'text-gray-900'}`}>
                    {mode.name}
                  </div>
                  <div className="text-xs text-gray-500">
                    {mode.description}
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default TabNavigation;

