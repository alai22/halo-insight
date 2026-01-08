import React, { useState, useEffect } from 'react';
import { Download, RefreshCw, FileDown, CheckCircle, XCircle, Clock, Database, List, Eye } from 'lucide-react';
import axios from 'axios';

const SurveyManager = () => {
  const [surveys, setSurveys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloadingSurveys, setDownloadingSurveys] = useState(new Set());
  const [selectedSurvey, setSelectedSurvey] = useState(null);
  const [surveyQuestions, setSurveyQuestions] = useState([]);
  const [surveyResponses, setSurveyResponses] = useState([]);
  const [loadingQuestions, setLoadingQuestions] = useState(false);
  const [loadingResponses, setLoadingResponses] = useState(false);
  const [surveyFiles, setSurveyFiles] = useState([]);
  const [loadingFiles, setLoadingFiles] = useState(false);

  const [error, setError] = useState(null);

  // Fetch all surveys
  const fetchSurveys = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/api/survicate/surveys');
      console.log('Surveys API response:', response.data);
      
      if (response.data.success) {
        const surveysList = response.data.surveys || [];
        console.log(`Received ${surveysList.length} surveys:`, surveysList);
        setSurveys(surveysList);
        
        if (surveysList.length === 0) {
          console.warn('API returned success but no surveys in response');
        }
      } else {
        const errorMsg = response.data.error || 'Failed to fetch surveys';
        const details = response.data.details || '';
        setError(`${errorMsg}${details ? ` - ${details}` : ''}`);
        console.error('Failed to fetch surveys:', response.data);
      }
    } catch (error) {
      const errorMsg = error.response?.data?.error || error.response?.data?.message || error.message || 'Failed to fetch surveys';
      const details = error.response?.data?.details || '';
      setError(`${errorMsg}${details ? ` - ${details}` : ''}`);
      console.error('Error fetching surveys:', error);
      console.error('Error response:', error.response?.data);
    } finally {
      setLoading(false);
    }
  };

  // Fetch questions for a survey
  const fetchSurveyQuestions = async (surveyId) => {
    setLoadingQuestions(true);
    try {
      const response = await axios.get(`/api/survicate/surveys/${surveyId}/questions`);
      if (response.data.success) {
        setSurveyQuestions(response.data.questions || []);
      } else {
        console.error('Failed to fetch questions:', response.data.error);
        setSurveyQuestions([]);
      }
    } catch (error) {
      console.error('Error fetching questions:', error);
      setSurveyQuestions([]);
    } finally {
      setLoadingQuestions(false);
    }
  };

  // Fetch responses for a survey (first page)
  const fetchSurveyResponses = async (surveyId) => {
    setLoadingResponses(true);
    try {
      const response = await axios.get(`/api/survicate/surveys/${surveyId}/responses`, {
        params: {
          items_per_page: 10
        }
      });
      if (response.data.success) {
        setSurveyResponses(response.data.responses || []);
      } else {
        console.error('Failed to fetch responses:', response.data.error);
        setSurveyResponses([]);
      }
    } catch (error) {
      console.error('Error fetching responses:', error);
      setSurveyResponses([]);
    } finally {
      setLoadingResponses(false);
    }
  };

  // Fetch files for a survey
  const fetchSurveyFiles = async (surveyId) => {
    setLoadingFiles(true);
    try {
      const response = await axios.get(`/api/survicate/surveys/${surveyId}/files`);
      if (response.data.success) {
        setSurveyFiles(response.data.files || []);
      } else {
        console.error('Failed to fetch files:', response.data.error);
        setSurveyFiles([]);
      }
    } catch (error) {
      console.error('Error fetching files:', error);
      setSurveyFiles([]);
    } finally {
      setLoadingFiles(false);
    }
  };

  // Handle survey selection
  const handleSurveySelect = (survey) => {
    setSelectedSurvey(survey);
    setSurveyQuestions([]);
    setSurveyResponses([]);
    setSurveyFiles([]);
    fetchSurveyQuestions(survey.id);
    fetchSurveyResponses(survey.id);
    fetchSurveyFiles(survey.id);
  };

  // Handle download
  const handleDownload = async (surveyId, surveyName) => {
    if (downloadingSurveys.has(surveyId)) {
      return;
    }

    setDownloadingSurveys(prev => new Set(prev).add(surveyId));
    
    try {
      const response = await axios.post(
        `/api/survicate/surveys/${surveyId}/download`,
        {}, // Empty body
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      if (response.data.success) {
        alert(`Download started for "${surveyName}". This may take a few minutes. The file will be saved to S3 or local storage.`);
        
        // Poll for completion (simplified - in production you might want more sophisticated polling)
        const pollInterval = setInterval(async () => {
          try {
            const statusResponse = await axios.get('/api/survicate/cache-status');
            if (statusResponse.data.success) {
              const state = statusResponse.data.cache_status.refresh_state;
              if (!state || !state.is_running) {
                clearInterval(pollInterval);
                setDownloadingSurveys(prev => {
                  const next = new Set(prev);
                  next.delete(surveyId);
                  return next;
                });
                if (state && state.error) {
                  alert(`Download completed with error: ${state.error}`);
                } else {
                  alert(`Download completed for "${surveyName}"`);
                  // Refresh files list for this survey
                  fetchSurveyFiles(surveyId);
                }
              }
            }
          } catch (error) {
            console.error('Error polling status:', error);
          }
        }, 5000);
        
        // Timeout after 10 minutes
        setTimeout(() => {
          clearInterval(pollInterval);
          setDownloadingSurveys(prev => {
            const next = new Set(prev);
            next.delete(surveyId);
            return next;
          });
        }, 600000);
      } else {
        alert(`Failed to start download: ${response.data.error || 'Unknown error'}`);
        setDownloadingSurveys(prev => {
          const next = new Set(prev);
          next.delete(surveyId);
          return next;
        });
      }
    } catch (error) {
      alert(`Error starting download: ${error.message}`);
      setDownloadingSurveys(prev => {
        const next = new Set(prev);
        next.delete(surveyId);
        return next;
      });
    }
  };

  useEffect(() => {
    fetchSurveys();
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchSurveys, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Survey Manager</h1>
        <p className="text-gray-600">View and download responses from all your Survicate surveys</p>
      </div>

      {/* Surveys List */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <List className="h-5 w-5" />
            <span>All Surveys</span>
          </h2>
          <button
            onClick={fetchSurveys}
            disabled={loading}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50"
            title="Refresh surveys"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
        
        {loading ? (
          <div className="text-sm text-gray-500 py-4">Loading surveys...</div>
        ) : error ? (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="text-sm text-red-800">
              <strong>Error:</strong> {error}
            </div>
            {error.includes('authentication') || error.includes('auth') || error.includes('401') || error.includes('403') ? (
              <div className="text-sm text-red-700 mt-2">
                This feature requires admin authentication. Please log in as an admin.
              </div>
            ) : null}
          </div>
        ) : surveys.length === 0 ? (
          <div className="text-sm text-gray-500 py-4">
            No surveys found. This could mean:
            <ul className="list-disc list-inside mt-2 space-y-1">
              <li>No surveys exist in your Survicate account</li>
              <li>The SURVICATE_API_KEY doesn't have access to list surveys</li>
              <li>There was an authentication error (check browser console)</li>
            </ul>
          </div>
        ) : (
          <div className="space-y-3">
            {surveys.map((survey) => {
              const isDownloading = downloadingSurveys.has(survey.id);
              const isSelected = selectedSurvey && selectedSurvey.id === survey.id;
              
              return (
                <div
                  key={survey.id}
                  className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-blue-50 border-blue-300'
                      : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleSurveySelect(survey)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="font-medium text-gray-900 mb-1">{survey.name}</div>
                      <div className="text-sm text-gray-600 space-y-1">
                        {survey.description && (
                          <div>{survey.description}</div>
                        )}
                        <div className="flex items-center space-x-4">
                          <span>ID: {survey.id}</span>
                          {survey.responses_count !== undefined && (
                            <span>{survey.responses_count.toLocaleString()} responses</span>
                          )}
                          {survey.questions_count !== undefined && (
                            <span>{survey.questions_count} questions</span>
                          )}
                          <span className={`px-2 py-1 rounded text-xs ${
                            survey.status === 'active' ? 'bg-green-100 text-green-700' :
                            survey.status === 'draft' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {survey.status || 'unknown'}
                          </span>
                        </div>
                        {survey.created_at && (
                          <div className="text-xs text-gray-500">
                            Created: {new Date(survey.created_at).toLocaleDateString()}
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDownload(survey.id, survey.name);
                        }}
                        disabled={isDownloading}
                        className="px-3 py-2 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center space-x-2 transition-colors"
                        title="Download all responses"
                      >
                        {isDownloading ? (
                          <>
                            <RefreshCw className="h-4 w-4 animate-spin" />
                            <span>Downloading...</span>
                          </>
                        ) : (
                          <>
                            <Download className="h-4 w-4" />
                            <span>Download</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Survey Details */}
      {selectedSurvey && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
              <Eye className="h-5 w-5" />
              <span>Survey Details: {selectedSurvey.name}</span>
            </h2>
          </div>

          {/* Questions Section */}
          <div className="mb-6">
            <h3 className="text-md font-medium text-gray-900 mb-3">Questions</h3>
            {loadingQuestions ? (
              <div className="text-sm text-gray-500 py-4">Loading questions...</div>
            ) : surveyQuestions.length === 0 ? (
              <div className="text-sm text-gray-500 py-4">No questions found</div>
            ) : (
              <div className="space-y-2">
                {surveyQuestions.map((q, index) => (
                  <div key={q.id} className="p-3 bg-gray-50 rounded border border-gray-200">
                    <div className="text-sm font-medium text-gray-700 mb-1">
                      Question {q.id}
                    </div>
                    <div className="text-sm text-gray-600">{q.text}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Downloaded Files Section */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-md font-medium text-gray-900">Downloaded Files</h3>
              <button
                onClick={() => fetchSurveyFiles(selectedSurvey.id)}
                className="p-1 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors"
                title="Refresh files"
              >
                <RefreshCw className={`h-4 w-4 ${loadingFiles ? 'animate-spin' : ''}`} />
              </button>
            </div>
            {loadingFiles ? (
              <div className="text-sm text-gray-500 py-4">Loading files...</div>
            ) : surveyFiles.length === 0 ? (
              <div className="text-sm text-gray-500 py-4">No files downloaded yet. Click "Download" above to download responses.</div>
            ) : (
              <div className="space-y-2">
                {surveyFiles.map((file) => (
                  <div key={file.key} className="p-3 bg-gray-50 rounded border border-gray-200 flex items-center justify-between">
                    <div className="flex-1">
                      <div className="font-medium text-gray-900 mb-1">{file.display_name}</div>
                      <div className="text-sm text-gray-600 space-y-1">
                        {file.response_count !== undefined && (
                          <div>{file.response_count.toLocaleString()} responses</div>
                        )}
                        {file.last_modified && (
                          <div>Downloaded: {new Date(file.last_modified).toLocaleString()}</div>
                        )}
                        {file.file_size && (
                          <div>Size: {(file.file_size / 1024).toFixed(2)} KB</div>
                        )}
                      </div>
                    </div>
                    <div className="ml-4">
                      <a
                        href={`/api/survicate/surveys/${selectedSurvey.id}/files/download?file_key=${encodeURIComponent(file.key)}`}
                        download={file.display_name}
                        className="px-3 py-2 text-sm bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center space-x-2 transition-colors"
                        title="Download CSV file"
                      >
                        <FileDown className="h-4 w-4" />
                        <span>Download</span>
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Sample Responses Section */}
          <div>
            <h3 className="text-md font-medium text-gray-900 mb-3">Sample Responses (First 10)</h3>
            {loadingResponses ? (
              <div className="text-sm text-gray-500 py-4">Loading responses...</div>
            ) : surveyResponses.length === 0 ? (
              <div className="text-sm text-gray-500 py-4">No responses found</div>
            ) : (
              <div className="space-y-3">
                {surveyResponses.map((response, index) => (
                  <div key={response.id || index} className="p-3 bg-gray-50 rounded border border-gray-200">
                    <div className="text-xs text-gray-500 mb-2">
                      Response ID: {response.id || 'N/A'}
                      {response.created_at && (
                        <span className="ml-2">
                          • {new Date(response.created_at).toLocaleString()}
                        </span>
                      )}
                    </div>
                    {response.answers && response.answers.length > 0 && (
                      <div className="space-y-1">
                        {response.answers.map((answer, aIndex) => (
                          <div key={aIndex} className="text-sm">
                            <span className="font-medium text-gray-700">Q{answer.question_id}:</span>{' '}
                            <span className="text-gray-600">{answer.answer || 'N/A'}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SurveyManager;

