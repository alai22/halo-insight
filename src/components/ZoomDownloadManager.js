import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react';

const ZoomDownloadManager = () => {
  const [downloadStatus, setDownloadStatus] = useState(null);
  const [downloadStats, setDownloadStats] = useState(null);
  const [downloadHistory, setDownloadHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [maxDuration, setMaxDuration] = useState(30);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [zoomStatus, setZoomStatus] = useState(null);

  // Fetch download status
  const fetchDownloadStatus = async () => {
    try {
      const response = await fetch('/api/zoom/download/status');
      const data = await response.json();
      if (data.status === 'success') {
        const prevStatus = downloadStatus;
        setDownloadStatus(data.data);
        
        // Log status changes to console with timestamp
        if (data.data.is_running) {
          if (!prevStatus || prevStatus.current_session !== data.data.current_session) {
            const timestamp = new Date().toLocaleTimeString('en-US', { 
              hour12: false, 
              hour: '2-digit', 
              minute: '2-digit', 
              second: '2-digit',
              fractionalSecondDigits: 3
            });
            console.log(`[${timestamp}] [ZOOM DOWNLOAD STATUS] Progress: ${data.data.current_session}/${data.data.total_sessions} (${data.data.progress_percentage.toFixed(1)}%)`);
            console.log(`[${timestamp}] [ZOOM DOWNLOAD STATUS] Downloaded: ${data.data.downloaded_count} | Failed: ${data.data.failed_count}`);
          }
        }
      }
    } catch (error) {
      console.error('[ZOOM DOWNLOAD ERROR] Error fetching download status:', error);
    }
  };

  // Fetch download statistics
  const fetchDownloadStats = async () => {
    try {
      const response = await fetch('/api/zoom/download/stats');
      const data = await response.json();
      if (data.status === 'success') {
        setDownloadStats(data.data);
      }
    } catch (error) {
      console.error('Error fetching Zoom download stats:', error);
    }
  };

  // Fetch download history
  const fetchDownloadHistory = async () => {
    try {
      const response = await fetch('/api/zoom/download/history');
      const data = await response.json();
      if (data.status === 'success') {
        setDownloadHistory(data.data.files || []);
      }
    } catch (error) {
      console.error('Error fetching Zoom download history:', error);
    }
  };

  // Start download
  const startDownload = async () => {
    if (!startDate || !endDate) {
      alert('Please select both start and end dates');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('/api/zoom/download/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          start_date: startDate,
          end_date: endDate,
          max_duration_minutes: maxDuration
        }),
      });
      
      const data = await response.json();
      if (data.status === 'success') {
        // Refresh data
        await Promise.all([
          fetchDownloadStatus(),
          fetchDownloadStats(),
          fetchDownloadHistory()
        ]);
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      console.error('Error starting Zoom download:', error);
      alert('Error starting download');
    } finally {
      setIsLoading(false);
    }
  };

  // Stop download
  const stopDownload = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/zoom/download/stop', {
        method: 'POST',
      });
      
      const data = await response.json();
      if (data.status === 'success') {
        // Refresh data
        await Promise.all([
          fetchDownloadStatus(),
          fetchDownloadStats(),
          fetchDownloadHistory()
        ]);
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      console.error('Error stopping Zoom download:', error);
      alert('Error stopping download');
    } finally {
      setIsLoading(false);
    }
  };

  // Auto-refresh when download is running
  useEffect(() => {
    if (!downloadStatus?.is_running) return;
    
    const interval = setInterval(async () => {
      try {
        const response = await fetch('/api/zoom/download/status');
        const data = await response.json();
        if (data.status === 'success' && data.data.is_running) {
          // Log progress to console for debugging with timestamp
          const timestamp = new Date().toLocaleTimeString('en-US', { 
            hour12: false, 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit'
          });
          console.log(`[${timestamp}] [ZOOM DOWNLOAD PROGRESS] ${data.data.current_session}/${data.data.total_sessions} (${data.data.progress_percentage.toFixed(1)}%) - Downloaded: ${data.data.downloaded_count}, Failed: ${data.data.failed_count}`);
          
          // Update state
          setDownloadStatus(data.data);
        }
      } catch (error) {
        console.error('[ZOOM DOWNLOAD ERROR] Error fetching download status:', error);
      }
    }, 2000); // Refresh every 2 seconds when running

    return () => clearInterval(interval);
  }, [downloadStatus?.is_running]);

  // Fetch Zoom credentials status
  const fetchZoomStatus = async () => {
    try {
      const response = await fetch('/api/zoom/status');
      const data = await response.json();
      if (data.status === 'success') {
        setZoomStatus(data.data);
      } else {
        setZoomStatus({
          configured: false,
          credentials_valid: false,
          error: data.message || 'Failed to check Zoom credentials'
        });
      }
    } catch (error) {
      console.error('Error fetching Zoom status:', error);
      setZoomStatus({
        configured: false,
        credentials_valid: false,
        error: `Network error: ${error.message}`
      });
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchDownloadStatus();
    fetchDownloadStats();
    fetchDownloadHistory();
    fetchZoomStatus();
  }, []);

  // Get status indicator
  const getStatusIndicator = () => {
    if (!zoomStatus) {
      return (
        <div className="flex items-center space-x-2 text-gray-500">
          <AlertCircle className="h-4 w-4" />
          <span className="text-sm">Checking credentials...</span>
        </div>
      );
    }

    if (zoomStatus.credentials_valid) {
      return (
        <div className="flex items-center space-x-2 text-green-600">
          <CheckCircle className="h-4 w-4" />
          <span className="text-sm font-medium">Zoom credentials configured and valid</span>
        </div>
      );
    }

    if (zoomStatus.configured) {
      return (
        <div className="flex items-center space-x-2 text-yellow-600">
          <AlertCircle className="h-4 w-4" />
          <span className="text-sm font-medium">Zoom credentials configured but invalid</span>
          {zoomStatus.error && (
            <span className="text-xs text-gray-500">({zoomStatus.error})</span>
          )}
        </div>
      );
    }

    // Not configured - show what's missing
    const missing = [];
    if (!zoomStatus.account_id_configured) missing.push('Account ID');
    if (!zoomStatus.client_id_configured) missing.push('Client ID');
    if (!zoomStatus.client_secret_configured) missing.push('Client Secret');

    return (
      <div className="flex items-center space-x-2 text-red-600">
        <XCircle className="h-4 w-4" />
        <span className="text-sm font-medium">
          Zoom credentials not configured
          {missing.length > 0 && (
            <span className="text-xs text-gray-500 ml-1">(Missing: {missing.join(', ')})</span>
          )}
        </span>
      </div>
    );
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Zoom Chat Download Manager</h1>
      
      {/* Credentials Status */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6 border-l-4 border-blue-500">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-sm font-semibold text-gray-700 mb-1">Zoom API Credentials</h2>
            {getStatusIndicator()}
          </div>
          <button
            onClick={fetchZoomStatus}
            className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors"
          >
            Refresh Status
          </button>
        </div>
      </div>
      
      {/* Download Controls */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Download Configuration</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Start Date (Required)
            </label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              disabled={downloadStatus?.is_running}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              End Date (Required)
            </label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              disabled={downloadStatus?.is_running}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Duration (minutes)
            </label>
            <input
              type="number"
              value={maxDuration}
              onChange={(e) => setMaxDuration(parseInt(e.target.value) || 30)}
              disabled={downloadStatus?.is_running}
              min="1"
              max="120"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
          </div>
        </div>
        
        <div className="flex gap-4">
          <button
            onClick={startDownload}
            disabled={isLoading || downloadStatus?.is_running || !startDate || !endDate || !zoomStatus?.credentials_valid}
            className={`px-6 py-2 rounded-lg font-medium transition-colors ${
              isLoading || downloadStatus?.is_running || !startDate || !endDate || !zoomStatus?.credentials_valid
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {downloadStatus?.is_running ? 'Download Running...' : 
             !zoomStatus?.credentials_valid ? 'Configure Zoom Credentials First' : 
             'Start Download'}
          </button>
          
          {downloadStatus?.is_running && (
            <button
              onClick={stopDownload}
              disabled={isLoading}
              className="px-6 py-2 rounded-lg font-medium bg-red-600 text-white hover:bg-red-700 transition-colors disabled:bg-gray-300 disabled:text-gray-500"
            >
              Stop Download
            </button>
          )}
        </div>
      </div>

      {/* Download Status */}
      {downloadStatus && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Download Status</h2>
          
          {downloadStatus.is_running ? (
            <div>
              {/* Phase Indicator */}
              {downloadStatus.current_phase && (
                <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></div>
                    <span className="text-sm font-medium text-blue-800">
                      {downloadStatus.current_phase === 'fetching_sessions' && 'Fetching chat sessions from Zoom...'}
                      {downloadStatus.current_phase === 'downloading_messages' && 'Downloading messages from sessions...'}
                      {downloadStatus.current_phase === 'uploading_s3' && 'Uploading to S3...'}
                      {downloadStatus.current_phase === 'completed' && 'Download completed!'}
                    </span>
                  </div>
                </div>
              )}
              
              {/* Current Session Info */}
              {downloadStatus.current_session_id && downloadStatus.current_phase === 'downloading_messages' && (
                <div className="mb-4 p-2 bg-gray-50 border border-gray-200 rounded text-sm">
                  <span className="text-gray-600">Processing session: </span>
                  <span className="font-mono text-gray-800">{downloadStatus.current_session_id.substring(0, 30)}...</span>
                  {downloadStatus.messages_in_current_session > 0 && (
                    <span className="text-gray-600 ml-2">
                      ({downloadStatus.messages_in_current_session} messages)
                    </span>
                  )}
                </div>
              )}
              
              <div className="mb-4">
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Progress</span>
                  <span className="text-sm font-medium text-gray-700">
                    {downloadStatus.current_session} / {downloadStatus.total_sessions} sessions
                    ({downloadStatus.progress_percentage.toFixed(1)}%)
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div
                    className="bg-blue-600 h-4 rounded-full transition-all duration-300"
                    style={{ width: `${downloadStatus.progress_percentage}%` }}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div>
                  <div className="text-sm text-gray-600">Downloaded</div>
                  <div className="text-2xl font-bold text-green-600">{downloadStatus.downloaded_count}</div>
                  <div className="text-xs text-gray-500">sessions</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Failed</div>
                  <div className="text-2xl font-bold text-red-600">{downloadStatus.failed_count}</div>
                  <div className="text-xs text-gray-500">sessions</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Total Messages</div>
                  <div className="text-2xl font-bold text-purple-600">{downloadStatus.total_messages || 0}</div>
                  <div className="text-xs text-gray-500">messages</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Rate</div>
                  <div className="text-lg font-semibold text-gray-800">
                    {downloadStatus.sessions_per_minute ? `${downloadStatus.sessions_per_minute.toFixed(1)}/min` : '0/min'}
                  </div>
                  <div className="text-xs text-gray-500">sessions</div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 pt-4 border-t border-gray-200">
                <div>
                  <div className="text-sm text-gray-600">Elapsed Time</div>
                  <div className="text-lg font-semibold text-gray-800">
                    {downloadStatus.elapsed_time ? `${Math.floor(downloadStatus.elapsed_time / 60)}m ${Math.floor(downloadStatus.elapsed_time % 60)}s` : '0s'}
                  </div>
                </div>
                {downloadStatus.estimated_time_remaining && downloadStatus.estimated_time_remaining > 0 && (
                  <div>
                    <div className="text-sm text-gray-600">Est. Time Remaining</div>
                    <div className="text-lg font-semibold text-orange-600">
                      {Math.floor(downloadStatus.estimated_time_remaining / 60)}m {Math.floor(downloadStatus.estimated_time_remaining % 60)}s
                    </div>
                  </div>
                )}
                <div>
                  <div className="text-sm text-gray-600">Status</div>
                  <div className="text-lg font-semibold text-blue-600">
                    {downloadStatus.current_phase === 'completed' ? 'Completed' : 'Running'}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-gray-600">
              {downloadStatus.error ? (
                <div className="text-red-600">Error: {downloadStatus.error}</div>
              ) : (
                <div>No download in progress</div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Download Statistics */}
      {downloadStats && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Download Statistics</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <div className="text-sm text-gray-600">Total Sessions Downloaded</div>
              <div className="text-3xl font-bold text-blue-600">{downloadStats.total_downloaded || 0}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Total Files</div>
              <div className="text-3xl font-bold text-green-600">{downloadStats.files?.length || 0}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Total Size</div>
              <div className="text-3xl font-bold text-purple-600">{downloadStats.total_size_mb || 0} MB</div>
            </div>
          </div>
        </div>
      )}

      {/* Download History */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Download History</h2>
        
        {downloadHistory.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Filename
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Sessions
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Size
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created At
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {downloadHistory.map((file, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {file.filename}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {file.session_count || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {file.size_mb || 0} MB
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {file.created_at ? new Date(file.created_at).toLocaleString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-gray-600">No download history available</div>
        )}
      </div>
    </div>
  );
};

export default ZoomDownloadManager;

