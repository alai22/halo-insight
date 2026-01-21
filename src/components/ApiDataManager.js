import React, { useState, useEffect } from 'react';
import { Download, RefreshCw, FileDown, Sparkles, CheckCircle, XCircle, Clock, Database } from 'lucide-react';
import axios from 'axios';

const ApiDataManager = () => {
  const [cacheStatus, setCacheStatus] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [augmentedFiles, setAugmentedFiles] = useState([]);
  const [rawFiles, setRawFiles] = useState([]);
  const [isAugmenting, setIsAugmenting] = useState(false);
  const [refreshProgress, setRefreshProgress] = useState(null);

  // Fetch cache status
  const fetchCacheStatus = async () => {
    try {
      const response = await axios.get('/api/survicate/cache-status');
      if (response.data.success) {
        setCacheStatus(response.data.cache_status);
      }
    } catch (error) {
      console.error('Error fetching cache status:', error);
    }
  };

  // Fetch raw files
  const fetchRawFiles = async () => {
    try {
      const response = await axios.get('/api/survicate/raw-files');
      if (response.data.success) {
        setRawFiles(response.data.files || []);
      }
    } catch (error) {
      console.error('Error fetching raw files:', error);
    }
  };

  // Fetch augmented files
  const fetchAugmentedFiles = async () => {
    try {
      const response = await axios.get('/api/survicate/augmented-files');
      if (response.data.success) {
        setAugmentedFiles(response.data.files || []);
      }
    } catch (error) {
      console.error('Error fetching augmented files:', error);
    }
  };

  useEffect(() => {
    fetchCacheStatus();
    fetchRawFiles();
    fetchAugmentedFiles();
    
    // Refresh every 5 seconds when refreshing
    let interval;
    if (isRefreshing || refreshProgress) {
      interval = setInterval(() => {
        fetchCacheStatus();
        fetchRawFiles();
        fetchAugmentedFiles();
      }, 5000);
    } else {
      // Otherwise refresh every 30 seconds
      interval = setInterval(() => {
        fetchCacheStatus();
        fetchRawFiles();
        fetchAugmentedFiles();
      }, 30000);
    }
    
    return () => clearInterval(interval);
  }, [isRefreshing, refreshProgress]);

  const handleRefreshApi = async () => {
    setIsRefreshing(true);
    setRefreshProgress({ status: 'starting', message: 'Starting API refresh...' });
    
    try {
      const response = await axios.post('/api/survicate/refresh-api');
      
      if (response.data.success) {
        setRefreshProgress({ status: 'running', message: 'Downloading responses from API...' });
        // Poll for completion
        const pollInterval = setInterval(async () => {
          const statusResponse = await axios.get('/api/survicate/cache-status');
          const statusData = statusResponse.data;
          if (statusData.success && statusData.cache_status) {
            const state = statusData.cache_status.refresh_state;
            if (state && state.is_running) {
              setRefreshProgress({ 
                status: 'running', 
                message: state.message || 'Processing...',
                error: state.error 
              });
            } else {
              clearInterval(pollInterval);
              setIsRefreshing(false);
              setRefreshProgress(null);
              fetchCacheStatus();
              fetchRawFiles();
              if (state && state.error) {
                alert(`API refresh completed with error: ${state.error}`);
              }
            }
          }
        }, 2000);
        
        // Timeout after 5 minutes
        setTimeout(() => {
          clearInterval(pollInterval);
          setIsRefreshing(false);
          setRefreshProgress(null);
        }, 300000);
      } else {
        setIsRefreshing(false);
        setRefreshProgress(null);
        alert(`Failed to start API refresh: ${response.data.error || 'Unknown error'}`);
      }
    } catch (error) {
      setIsRefreshing(false);
      setRefreshProgress(null);
      alert(`Error starting API refresh: ${error.message}`);
    }
  };

  const handleTriggerAugmentation = async (fileKey) => {
    setIsAugmenting(true);
    try {
      const response = await axios.post('/api/survicate/augment', {
        raw_file_key: fileKey
      });
      
      const data = response.data;
      if (data.success) {
        // Poll for completion
        const pollInterval = setInterval(async () => {
          await fetchAugmentedFiles();
          const file = rawFiles.find(f => f.key === fileKey);
          if (file && file.has_augmentation) {
            clearInterval(pollInterval);
            setIsAugmenting(false);
          }
        }, 2000);
        
        setTimeout(() => {
          clearInterval(pollInterval);
          setIsAugmenting(false);
        }, 600000); // 10 minute timeout
      } else {
        setIsAugmenting(false);
        alert(`Failed to start augmentation: ${data.error || 'Unknown error'}`);
      }
    } catch (error) {
      setIsAugmenting(false);
      alert(`Error starting augmentation: ${error.message}`);
    }
  };

  const getCacheStatusColor = () => {
    if (!cacheStatus) return 'text-gray-500';
    if (cacheStatus.is_fresh) return 'text-green-600';
    if (cacheStatus.cache_exists) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getCacheStatusIcon = () => {
    if (!cacheStatus) return <Clock className="h-4 w-4" />;
    if (cacheStatus.is_fresh) return <CheckCircle className="h-4 w-4" />;
    if (cacheStatus.cache_exists) return <Clock className="h-4 w-4" />;
    return <XCircle className="h-4 w-4" />;
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">API Data Management</h1>
        <p className="text-gray-600">Download and augment survey data from the Survicate API</p>
      </div>

      {/* Cache Status Card */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <Database className="h-5 w-5" />
            <span>Cache Status</span>
          </h2>
          <button
            onClick={fetchCacheStatus}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            title="Refresh status"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
        
        {cacheStatus ? (
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              {getCacheStatusIcon()}
              <span className={`font-medium ${getCacheStatusColor()}`}>
                {cacheStatus.is_fresh ? 'Fresh' : cacheStatus.cache_exists ? 'Stale' : 'No Cache'}
              </span>
              {cacheStatus.cache_age_hours != null && typeof cacheStatus.cache_age_hours === 'number' && (
                <span className="text-sm text-gray-500">
                  ({cacheStatus.cache_age_hours.toFixed(1)}h ago)
                </span>
              )}
            </div>
            {cacheStatus.last_modified && (
              <div className="text-sm text-gray-600">
                Last updated: {new Date(cacheStatus.last_modified).toLocaleString()}
              </div>
            )}
            {cacheStatus.refresh_state && cacheStatus.refresh_state.is_running && (
              <div className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded">
                <div className="flex items-center space-x-2">
                  <RefreshCw className="h-4 w-4 text-blue-600 animate-spin" />
                  <span className="text-sm text-blue-800">
                    {cacheStatus.refresh_state.message || 'Refreshing...'}
                  </span>
                </div>
              </div>
            )}
            {cacheStatus.refresh_state && cacheStatus.refresh_state.error && (
              <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded">
                <div className="text-sm text-red-800">
                  <strong>Error:</strong> {cacheStatus.refresh_state.error}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="text-sm text-gray-500">Loading status...</div>
        )}
      </div>

      {/* Download Section */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <Download className="h-5 w-5" />
            <span>Download from API</span>
          </h2>
        </div>
        
        <div className="space-y-4">
          <p className="text-sm text-gray-600">
            Download the latest survey responses from the Survicate API. This will fetch all responses and save them locally.
          </p>
          
          {refreshProgress && (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded">
              <div className="flex items-center space-x-2 mb-2">
                <RefreshCw className="h-4 w-4 text-blue-600 animate-spin" />
                <span className="text-sm font-medium text-blue-800">{refreshProgress.message}</span>
              </div>
              {refreshProgress.error && (
                <div className="mt-2 text-sm text-red-700">{refreshProgress.error}</div>
              )}
            </div>
          )}
          
          <button
            onClick={handleRefreshApi}
            disabled={isRefreshing}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center space-x-2 transition-colors"
          >
            {isRefreshing ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                <span>Downloading...</span>
              </>
            ) : (
              <>
                <Download className="h-4 w-4" />
                <span>Download from API</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Raw Files Section */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <FileDown className="h-5 w-5" />
            <span>Downloaded Files</span>
          </h2>
          <button
            onClick={fetchRawFiles}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            title="Refresh files"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
        
        {rawFiles.length === 0 ? (
          <div className="text-sm text-gray-500 py-4">
            No files downloaded yet. Click "Download from API" above to get started.
          </div>
        ) : (
          <div className="space-y-3">
            {rawFiles.map((file) => (
              <div key={file.key} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 mb-1">{file.display_name}</div>
                    <div className="text-sm text-gray-600 space-y-1">
                      <div>{file.response_count?.toLocaleString() || 'Unknown'} responses</div>
                      <div>Last modified: {new Date(file.last_modified).toLocaleString()}</div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <a
                      href={`/api/survicate/raw-files/download?file_key=${encodeURIComponent(file.key)}`}
                      download={file.display_name}
                      className="px-3 py-2 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center space-x-2 transition-colors"
                      title="Download CSV file"
                    >
                      <FileDown className="h-4 w-4" />
                      <span>Download</span>
                    </a>
                    {!file.has_augmentation && (
                      <button
                        onClick={() => handleTriggerAugmentation(file.key)}
                        disabled={isAugmenting}
                        className="px-3 py-2 text-sm bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center space-x-2 transition-colors"
                        title="Run augmentation with LLM"
                      >
                        {isAugmenting ? (
                          <>
                            <RefreshCw className="h-4 w-4 animate-spin" />
                            <span>Augmenting...</span>
                          </>
                        ) : (
                          <>
                            <Sparkles className="h-4 w-4" />
                            <span>Augment</span>
                          </>
                        )}
                      </button>
                    )}
                    {file.has_augmentation && (
                      <span className="px-3 py-2 text-sm bg-green-100 text-green-700 rounded-lg flex items-center space-x-2">
                        <CheckCircle className="h-4 w-4" />
                        <span>Augmented</span>
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Augmented Files Section */}
      {augmentedFiles.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
              <Sparkles className="h-5 w-5" />
              <span>Augmented Files</span>
            </h2>
            <button
              onClick={fetchAugmentedFiles}
              className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              title="Refresh files"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
          
          <div className="space-y-3">
            {augmentedFiles.map((file) => (
              <div key={file.key} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 mb-1">{file.display_name}</div>
                    <div className="text-sm text-gray-600 space-y-1">
                      <div>{file.response_count?.toLocaleString() || 'Unknown'} responses</div>
                      <div>Last modified: {new Date(file.last_modified).toLocaleString()}</div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <a
                      href={`/api/survicate/augmented-files/download?file_key=${encodeURIComponent(file.key)}`}
                      download={file.display_name}
                      className="px-3 py-2 text-sm bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center space-x-2 transition-colors"
                      title="Download augmented CSV file"
                    >
                      <FileDown className="h-4 w-4" />
                      <span>Download</span>
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ApiDataManager;

