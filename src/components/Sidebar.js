import React, { useState, useEffect } from 'react';
import { Database, RefreshCw, CheckCircle, XCircle, Download } from 'lucide-react';

const Sidebar = ({ healthStatus, onRefreshHealth, currentMode, setAdminMode, setCurrentMode, onCloseSettings }) => {
  const [downloadStats, setDownloadStats] = useState(null);
  const [surveyStats, setSurveyStats] = useState(null);
  const [dataSource, setDataSource] = useState(
    localStorage.getItem('survicate_data_source') || 'file'
  );
  const [cacheStatus, setCacheStatus] = useState(null);

  // Fetch download stats
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/download/stats');
        const data = await response.json();
        if (data.status === 'success') {
          setDownloadStats(data.data);
        }
      } catch (error) {
        console.error('Error fetching download stats:', error);
      }
    };

    fetchStats();
    // Refresh every 30 seconds
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  // Fetch survey stats when in survicate or churn-trends mode
  useEffect(() => {
    const fetchSurveyStats = async () => {
      if (currentMode === 'survicate' || currentMode === 'churn-trends') {
        try {
          const response = await fetch(`/api/survicate/summary?data_source=${dataSource}`);
          const data = await response.json();
          if (data.success) {
            setSurveyStats(data.summary);
          }
        } catch (error) {
          console.error('Error fetching survey stats:', error);
          setSurveyStats(null);
        }
      } else {
        setSurveyStats(null);
      }
    };

    fetchSurveyStats();
  }, [currentMode, dataSource]);

  // Fetch cache status when in API mode
  useEffect(() => {
    const fetchCacheStatus = async () => {
      if ((currentMode === 'survicate' || currentMode === 'churn-trends') && dataSource === 'api') {
        try {
          const response = await fetch('/api/survicate/cache-status');
          const data = await response.json();
          if (data.success) {
            setCacheStatus(data.cache_status);
          }
        } catch (error) {
          console.error('Error fetching cache status:', error);
          setCacheStatus(null);
        }
      } else {
        setCacheStatus(null);
      }
    };

    fetchCacheStatus();
    // Poll cache status every 10 seconds when in API mode
    if ((currentMode === 'survicate' || currentMode === 'churn-trends') && dataSource === 'api') {
      const interval = setInterval(fetchCacheStatus, 10000);
      return () => clearInterval(interval);
    }
  }, [currentMode, dataSource]);

  const handleDataSourceChange = async (newSource) => {
    setDataSource(newSource);
    localStorage.setItem('survicate_data_source', newSource);
    
    // Refresh survey stats with new source
    if (currentMode === 'survicate' || currentMode === 'churn-trends') {
      try {
        const response = await fetch(`/api/survicate/summary?data_source=${newSource}`);
        const data = await response.json();
        if (data.success) {
          setSurveyStats(data.summary);
        }
      } catch (error) {
        console.error('Error refreshing survey stats:', error);
      }
    }
  };

  const getHealthStatusIcon = () => {
    if (!healthStatus) return <RefreshCw className="h-4 w-4 animate-spin" />;
    if (healthStatus.status === 'healthy') return <CheckCircle className="h-4 w-4 text-green-500" />;
    return <XCircle className="h-4 w-4 text-red-500" />;
  };

  const getHealthStatusText = () => {
    if (!healthStatus) return 'Checking...';
    if (healthStatus.status === 'healthy') return 'Connected';
    return 'Disconnected';
  };

  const getHealthStatusColor = () => {
    if (!healthStatus) return 'text-gray-500';
    if (healthStatus.status === 'healthy') return 'text-green-600';
    return 'text-red-600';
  };

  return (
    <div className="w-64 bg-white shadow-lg border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3 mb-4">
          <Database className="h-8 w-8 text-blue-600" />
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Halo AI Insights</h2>
            <p className="text-sm text-gray-500">Customer Intelligence</p>
          </div>
        </div>
        
        {/* Health Status */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {getHealthStatusIcon()}
            <span className={`text-sm font-medium ${getHealthStatusColor()}`}>
              {getHealthStatusText()}
            </span>
          </div>
          <button
            onClick={onRefreshHealth}
            className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
            title="Refresh connection"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Download Manager Button - Only show in Gladly Conversations tab */}
      {(currentMode === 'conversations' || currentMode === 'ask' || currentMode === 'conversation-trends') && (
        <div className="p-6 border-t border-gray-200">
          <button
            onClick={() => {
              setAdminMode('download');
              setCurrentMode('ask'); // Reset to a regular mode
              if (onCloseSettings) onCloseSettings(); // Close settings panel if open
            }}
            className="w-full flex items-center space-x-3 px-4 py-3 bg-orange-50 border-2 border-orange-200 rounded-lg hover:bg-orange-100 hover:border-orange-300 transition-all group"
          >
            <Download className="h-5 w-5 text-orange-600 group-hover:text-orange-700" />
            <div className="flex-1 text-left">
              <div className="text-sm font-medium text-orange-900">Download Manager</div>
              <div className="text-xs text-orange-600">Download conversation data from Gladly</div>
            </div>
          </button>
        </div>
      )}

      {/* Conversation Stats - Only show in Gladly Conversations mode */}
      {downloadStats && (currentMode === 'conversations' || currentMode === 'ask') && (
        <div className="p-6 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            <div className="mb-2">
              <strong>Conversations:</strong>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Available</span>
                <span className="font-semibold text-blue-600">{downloadStats.total_in_csv?.toLocaleString() || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Downloaded</span>
                <span className="font-semibold text-green-600">{downloadStats.total_downloaded?.toLocaleString() || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Remaining</span>
                <span className="font-semibold text-yellow-600">{downloadStats.remaining?.toLocaleString() || 0}</span>
              </div>
              {downloadStats.completion_percentage !== undefined && (
                <div className="mt-2">
                  <div className="w-full bg-gray-200 rounded-full h-1.5">
                    <div 
                      className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
                      style={{ width: `${Math.min(downloadStats.completion_percentage, 100)}%` }}
                    ></div>
                  </div>
                  <div className="text-center mt-1 text-xs">
                    {downloadStats.completion_percentage.toFixed(1)}% Complete
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Churn Trends Stats */}
      {surveyStats && currentMode === 'churn-trends' && (
        <div className="p-6 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            <div className="mb-2">
              <strong>Churn Trends Data:</strong>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Survey Responses</span>
                <span className="font-semibold text-blue-600">{surveyStats.total_responses?.toLocaleString() || 0}</span>
              </div>
              {surveyStats.date_range && (
                <div className="flex flex-col space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Start Date</span>
                    <span className="font-semibold text-gray-700 text-xs">
                      {surveyStats.date_range.start !== 'Unknown' ? (
                        new Date(surveyStats.date_range.start).toLocaleDateString()
                      ) : 'N/A'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">End Date</span>
                    <span className="font-semibold text-gray-700 text-xs">
                      {surveyStats.date_range.end !== 'Unknown' ? (
                        new Date(surveyStats.date_range.end).toLocaleDateString()
                      ) : 'N/A'}
                    </span>
                  </div>
                </div>
              )}
            </div>
            {surveyStats.total_responses === 0 && (
              <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
                No survey data loaded. Ensure the CSV file is in the data directory.
              </div>
            )}
          </div>
        </div>
      )}

      {/* Data Source Toggle - Show for survicate and churn-trends modes */}
      {(currentMode === 'survicate' || currentMode === 'churn-trends') && (
        <div className="p-6 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            <div className="mb-2">
              <strong>Data Source:</strong>
            </div>
            <select
              value={dataSource}
              onChange={(e) => handleDataSourceChange(e.target.value)}
              className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="file">File (CSV)</option>
              <option value="api">API (Live)</option>
            </select>
          </div>
        </div>
      )}

      {/* Cache Status - Show when in API mode */}
      {cacheStatus && dataSource === 'api' && (currentMode === 'survicate' || currentMode === 'churn-trends') && (
        <div className="p-6 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            <div className="mb-2">
              <strong>Cache Status:</strong>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Status</span>
                <span className={`font-semibold ${cacheStatus.is_fresh ? 'text-green-600' : 'text-yellow-600'}`}>
                  {cacheStatus.is_fresh ? 'Fresh' : 'Stale'}
                </span>
              </div>
              {cacheStatus.cache_age_hours !== null && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Age</span>
                  <span className="font-semibold text-gray-700">
                    {Math.round(cacheStatus.cache_age_hours)}h ago
                  </span>
                </div>
              )}
              {cacheStatus.refresh_in_progress && (
                <div className="flex items-center text-blue-600 mt-2">
                  <RefreshCw className="h-3 w-3 animate-spin mr-1" />
                  <span className="text-xs">Refreshing from API...</span>
                </div>
              )}
              {cacheStatus.refresh_error && (
                <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-800">
                  Error: {cacheStatus.refresh_error}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Survey Stats */}
      {surveyStats && currentMode === 'survicate' && (
        <div className="p-6 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            <div className="mb-2">
              <strong>Survey Responses:</strong>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Available in RAG</span>
                <span className="font-semibold text-blue-600">{surveyStats.total_responses?.toLocaleString() || 0}</span>
              </div>
              {surveyStats.date_range && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Date Range</span>
                  <span className="font-semibold text-gray-700 text-xs">
                    {surveyStats.date_range.start !== 'Unknown' && surveyStats.date_range.end !== 'Unknown' ? (
                      <>{new Date(surveyStats.date_range.start).toLocaleDateString()} - {new Date(surveyStats.date_range.end).toLocaleDateString()}</>
                    ) : 'N/A'}
                  </span>
                </div>
              )}
            </div>
            {surveyStats.total_responses === 0 && (
              <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
                {dataSource === 'api' 
                  ? 'No survey data loaded. Cache may be refreshing or API may be unavailable.'
                  : 'No survey data loaded. Ensure the CSV file is in the data directory.'}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="mt-auto p-6 border-t border-gray-200">
        <div className="text-xs text-gray-500">
          <div className="mb-2">
            <strong>Backend Status:</strong>
          </div>
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${
                healthStatus?.claude_initialized ? 'bg-green-400' : 'bg-red-400'
              }`} />
              <span>Claude API</span>
            </div>
            {healthStatus?.error && !healthStatus.claude_initialized && (
              <div className="ml-4 text-xs text-red-600 mt-1">
                {healthStatus.error}
              </div>
            )}
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${
                healthStatus?.conversation_analyzer_initialized ? 'bg-green-400' : 'bg-red-400'
              }`} />
              <span>Data Analyzer</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
