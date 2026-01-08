import React, { useState, useEffect } from 'react';
import { Download, RefreshCw, FileDown, CheckCircle, XCircle, Clock, Database, List, Eye, ArrowLeft, FileText, BarChart3 } from 'lucide-react';
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
  const [activeTab, setActiveTab] = useState('overview'); // 'overview', 'files', 'questions', 'responses'
  const [surveysWithFiles, setSurveysWithFiles] = useState(new Set()); // Track which surveys have files
  const [surveySummary, setSurveySummary] = useState(null);
  const [loadingSummary, setLoadingSummary] = useState(false);

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

  // Fetch summary statistics for a survey
  const fetchSurveySummary = async (surveyId, fileKey = null) => {
    setLoadingSummary(true);
    try {
      const url = `/api/survicate/surveys/${surveyId}/summary${fileKey ? `?file_key=${encodeURIComponent(fileKey)}` : ''}`;
      const response = await axios.get(url);
      if (response.data.success) {
        setSurveySummary(response.data.summary);
      } else {
        console.error('Failed to fetch summary:', response.data.error);
        setSurveySummary(null);
      }
    } catch (error) {
      console.error('Error fetching summary:', error);
      setSurveySummary(null);
    } finally {
      setLoadingSummary(false);
    }
  };

  // Fetch files for a survey
  const fetchSurveyFiles = async (surveyId) => {
    setLoadingFiles(true);
    try {
      const response = await axios.get(`/api/survicate/surveys/${surveyId}/files`);
      if (response.data.success) {
        const files = response.data.files || [];
        setSurveyFiles(files);
        // Update tracking of surveys with files
        if (files.length > 0) {
          setSurveysWithFiles(prev => new Set(prev).add(surveyId));
        } else {
          setSurveysWithFiles(prev => {
            const next = new Set(prev);
            next.delete(surveyId);
            return next;
          });
        }
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
    setSurveySummary(null);
    setActiveTab('overview');
    fetchSurveyQuestions(survey.id);
    fetchSurveyResponses(survey.id);
    fetchSurveyFiles(survey.id);
    // Fetch summary after files are loaded (so we know which file to use)
    setTimeout(() => {
      fetchSurveyFiles(survey.id).then(() => {
        // Use most recent file for summary
        fetchSurveySummary(survey.id);
      });
    }, 500);
  };

  // Handle back to list
  const handleBackToList = () => {
    setSelectedSurvey(null);
    setActiveTab('overview');
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
                  if (selectedSurvey && selectedSurvey.id === surveyId) {
                    fetchSurveyFiles(surveyId).then(() => {
                      // Refresh summary after files are updated
                      setTimeout(() => fetchSurveySummary(surveyId), 1000);
                    });
                  }
                  // Update tracking
                  setSurveysWithFiles(prev => new Set(prev).add(surveyId));
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

  // If a survey is selected, show detail view
  if (selectedSurvey) {
    return (
      <div className="p-6 max-w-7xl mx-auto">
        {/* Header with Back Button */}
        <div className="mb-6">
          <button
            onClick={handleBackToList}
            className="mb-4 flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Back to Surveys</span>
          </button>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">{selectedSurvey.name}</h1>
          <p className="text-gray-600">Survey ID: {selectedSurvey.id} • {selectedSurvey.responses_count?.toLocaleString() || 0} responses</p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="flex space-x-1 border-b border-gray-200 p-1">
            {[
              { id: 'overview', name: 'Overview', icon: Eye },
              { id: 'files', name: 'Downloaded Files', icon: FileDown },
              { id: 'questions', name: 'Questions', icon: FileText },
              { id: 'responses', name: 'Sample Responses', icon: BarChart3 }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Survey Information</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <div className="text-sm text-gray-600">Survey ID</div>
                      <div className="text-lg font-medium text-gray-900">{selectedSurvey.id}</div>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <div className="text-sm text-gray-600">Status</div>
                      <div className="text-lg font-medium text-gray-900">
                        <span className={`px-2 py-1 rounded text-sm ${
                          selectedSurvey.status === 'active' ? 'bg-green-100 text-green-700' :
                          selectedSurvey.status === 'draft' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {selectedSurvey.status || 'unknown'}
                        </span>
                      </div>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <div className="text-sm text-gray-600">Total Responses</div>
                      <div className="text-lg font-medium text-gray-900">{selectedSurvey.responses_count?.toLocaleString() || 0}</div>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <div className="text-sm text-gray-600">Created</div>
                      <div className="text-lg font-medium text-gray-900">
                        {selectedSurvey.created_at ? new Date(selectedSurvey.created_at).toLocaleDateString() : 'N/A'}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Summary Statistics */}
                {surveyFiles.length > 0 && (
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Analyze File:
                    </label>
                    <select
                      onChange={(e) => {
                        const fileKey = e.target.value;
                        if (fileKey) {
                          fetchSurveySummary(selectedSurvey.id, fileKey);
                        } else {
                          fetchSurveySummary(selectedSurvey.id);
                        }
                      }}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      defaultValue=""
                    >
                      <option value="">Most Recent</option>
                      {surveyFiles.map((file) => (
                        <option key={file.key} value={file.key}>
                          {file.filename} ({file.response_count?.toLocaleString() || 0} responses, {new Date(file.last_modified).toLocaleDateString()})
                        </option>
                      ))}
                    </select>
                  </div>
                )}
                {loadingSummary ? (
                  <div className="text-center py-8">
                    <RefreshCw className="h-8 w-8 text-gray-400 animate-spin mx-auto mb-2" />
                    <div className="text-sm text-gray-500">Loading summary statistics...</div>
                  </div>
                ) : surveySummary ? (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Response Summary</h3>
                    <div className="grid grid-cols-3 gap-4 mb-6">
                      <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                        <div className="text-sm text-blue-600 mb-1">Total Responses</div>
                        <div className="text-2xl font-bold text-blue-900">{surveySummary.total_responses?.toLocaleString() || 0}</div>
                      </div>
                      <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                        <div className="text-sm text-green-600 mb-1">Questions</div>
                        <div className="text-2xl font-bold text-green-900">{surveySummary.total_questions || 0}</div>
                      </div>
                      {surveySummary.date_range && (
                        <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                          <div className="text-sm text-purple-600 mb-1">Date Range</div>
                          <div className="text-sm font-medium text-purple-900">
                            {new Date(surveySummary.date_range.start).toLocaleDateString()} - {new Date(surveySummary.date_range.end).toLocaleDateString()}
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Question Answer Distributions */}
                    {surveySummary.questions && Object.keys(surveySummary.questions).length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Answer Distributions</h3>
                        <div className="space-y-4">
                          {Object.entries(surveySummary.questions).slice(0, 5).map(([qKey, qData]) => (
                            <div key={qKey} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                              <div className="mb-3">
                                <div className="font-medium text-gray-900 mb-1 flex items-center space-x-2">
                                  <span>{qKey}: {qData.question_text}</span>
                                  {qData.is_text_question && (
                                    <span className="px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded-full">
                                      Text Question
                                    </span>
                                  )}
                                </div>
                                <div className="text-sm text-gray-600">
                                  {qData.total_responses} responses ({qData.response_rate}% response rate) • {qData.unique_answers_count} unique answers
                                  {qData.average_answer_length > 0 && ` • Avg length: ${qData.average_answer_length.toFixed(0)} chars`}
                                </div>
                              </div>
                              
                              {/* LLM Insights for Text Questions */}
                              {qData.is_text_question && qData.llm_insights && (
                                <div className="mt-4 p-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border border-purple-200">
                                  <div className="flex items-center space-x-2 mb-3">
                                    <BarChart3 className="h-4 w-4 text-purple-600" />
                                    <div className="text-sm font-semibold text-purple-900">AI-Powered Insights</div>
                                  </div>
                                  
                                  {/* Summary */}
                                  {qData.llm_insights.summary && !qData.llm_insights.raw_analysis && (
                                    <div className="mb-3 p-2 bg-white rounded border border-purple-100">
                                      <div className="text-xs font-medium text-gray-700 mb-1">Summary</div>
                                      <div className="text-sm text-gray-800">{qData.llm_insights.summary}</div>
                                    </div>
                                  )}
                                  
                                  {/* Sentiment Distribution */}
                                  {qData.llm_insights.sentiment && (
                                    <div className="mb-3">
                                      <div className="text-xs font-medium text-gray-700 mb-2">Sentiment Distribution</div>
                                      <div className="flex space-x-2">
                                        {qData.llm_insights.sentiment.positive !== undefined && (
                                          <div className="flex-1">
                                            <div className="flex justify-between text-xs mb-1">
                                              <span className="text-green-700">Positive</span>
                                              <span className="text-gray-600">{qData.llm_insights.sentiment.positive}%</span>
                                            </div>
                                            <div className="w-full bg-gray-200 rounded-full h-2">
                                              <div
                                                className="bg-green-500 h-2 rounded-full"
                                                style={{ width: `${qData.llm_insights.sentiment.positive}%` }}
                                              />
                                            </div>
                                          </div>
                                        )}
                                        {qData.llm_insights.sentiment.neutral !== undefined && (
                                          <div className="flex-1">
                                            <div className="flex justify-between text-xs mb-1">
                                              <span className="text-gray-700">Neutral</span>
                                              <span className="text-gray-600">{qData.llm_insights.sentiment.neutral}%</span>
                                            </div>
                                            <div className="w-full bg-gray-200 rounded-full h-2">
                                              <div
                                                className="bg-gray-500 h-2 rounded-full"
                                                style={{ width: `${qData.llm_insights.sentiment.neutral}%` }}
                                              />
                                            </div>
                                          </div>
                                        )}
                                        {qData.llm_insights.sentiment.negative !== undefined && (
                                          <div className="flex-1">
                                            <div className="flex justify-between text-xs mb-1">
                                              <span className="text-red-700">Negative</span>
                                              <span className="text-gray-600">{qData.llm_insights.sentiment.negative}%</span>
                                            </div>
                                            <div className="w-full bg-gray-200 rounded-full h-2">
                                              <div
                                                className="bg-red-500 h-2 rounded-full"
                                                style={{ width: `${qData.llm_insights.sentiment.negative}%` }}
                                              />
                                            </div>
                                          </div>
                                        )}
                                      </div>
                                    </div>
                                  )}
                                  
                                  {/* Themes */}
                                  {qData.llm_insights.themes && qData.llm_insights.themes.length > 0 && (
                                    <div className="mb-3">
                                      <div className="text-xs font-medium text-gray-700 mb-2">Common Themes</div>
                                      <div className="flex flex-wrap gap-2">
                                        {qData.llm_insights.themes.slice(0, 8).map((theme, idx) => (
                                          <div key={idx} className="px-2 py-1 bg-white rounded border border-purple-200 text-xs">
                                            <div className="font-medium text-gray-800">{theme.theme}</div>
                                            {theme.frequency && (
                                              <div className="text-gray-500 text-xs">{theme.frequency}</div>
                                            )}
                                          </div>
                                        ))}
                                      </div>
                                    </div>
                                  )}
                                  
                                  {/* Categories */}
                                  {qData.llm_insights.categories && qData.llm_insights.categories.length > 0 && (
                                    <div className="mb-3">
                                      <div className="text-xs font-medium text-gray-700 mb-2">Categorized Feedback</div>
                                      <div className="space-y-2">
                                        {qData.llm_insights.categories.slice(0, 5).map((category, idx) => (
                                          <div key={idx} className="flex items-center justify-between text-xs">
                                            <span className="text-gray-700 flex-1">{category.category}</span>
                                            <div className="flex items-center space-x-2">
                                              <div className="w-24 bg-gray-200 rounded-full h-1.5">
                                                <div
                                                  className="bg-purple-500 h-1.5 rounded-full"
                                                  style={{ width: `${category.percentage}%` }}
                                                />
                                              </div>
                                              <span className="text-gray-600 w-16 text-right">
                                                {category.count} ({category.percentage}%)
                                              </span>
                                            </div>
                                          </div>
                                        ))}
                                      </div>
                                    </div>
                                  )}
                                  
                                  {/* Key Phrases */}
                                  {qData.llm_insights.key_phrases && qData.llm_insights.key_phrases.length > 0 && (
                                    <div>
                                      <div className="text-xs font-medium text-gray-700 mb-2">Key Phrases</div>
                                      <div className="flex flex-wrap gap-1">
                                        {qData.llm_insights.key_phrases.slice(0, 10).map((phrase, idx) => (
                                          <span key={idx} className="px-2 py-0.5 bg-blue-100 text-blue-800 rounded text-xs">
                                            {phrase}
                                          </span>
                                        ))}
                                      </div>
                                    </div>
                                  )}
                                  
                                  {/* Raw Analysis Fallback */}
                                  {qData.llm_insights.raw_analysis && qData.llm_insights.summary && (
                                    <div className="p-2 bg-white rounded border border-purple-100 text-sm text-gray-800">
                                      {qData.llm_insights.summary}
                                    </div>
                                  )}
                                </div>
                              )}
                              
                              {/* Regular Answer Distribution (for non-text or when LLM not available) */}
                              {(!qData.is_text_question || !qData.llm_insights) && qData.top_answers && Object.keys(qData.top_answers).length > 0 && (
                                <div className="space-y-2">
                                  <div className="text-xs font-medium text-gray-700 mb-2">Top Answers:</div>
                                  {Object.entries(qData.top_answers).slice(0, 5).map(([answer, stats]) => (
                                    <div key={answer} className="flex items-center justify-between text-sm">
                                      <span className="text-gray-700 flex-1 truncate mr-4">{answer}</span>
                                      <div className="flex items-center space-x-3">
                                        <div className="w-32 bg-gray-200 rounded-full h-2">
                                          <div
                                            className="bg-blue-500 h-2 rounded-full"
                                            style={{ width: `${stats.percentage}%` }}
                                          />
                                        </div>
                                        <span className="text-gray-600 w-20 text-right">
                                          {stats.count} ({stats.percentage}%)
                                        </span>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          ))}
                          {Object.keys(surveySummary.questions).length > 5 && (
                            <div className="text-sm text-gray-500 text-center py-2">
                              Showing top 5 questions. View all in the Questions tab.
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ) : surveyFiles.length === 0 ? (
                  <div className="text-center py-8 bg-gray-50 rounded-lg border border-gray-200">
                    <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600 mb-2">No data available for analysis</p>
                    <p className="text-sm text-gray-500">Download responses to see summary statistics</p>
                  </div>
                ) : null}

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                  <div className="flex space-x-3">
                    <button
                      onClick={() => {
                        handleDownload(selectedSurvey.id, selectedSurvey.name);
                      }}
                      disabled={downloadingSurveys.has(selectedSurvey.id)}
                      className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center space-x-2 transition-colors"
                    >
                      {downloadingSurveys.has(selectedSurvey.id) ? (
                        <>
                          <RefreshCw className="h-4 w-4 animate-spin" />
                          <span>Downloading...</span>
                        </>
                      ) : (
                        <>
                          <Download className="h-4 w-4" />
                          <span>Download All Responses</span>
                        </>
                      )}
                    </button>
                    {surveyFiles.length > 0 && (
                      <button
                        onClick={() => {
                          setActiveTab('files');
                          fetchSurveySummary(selectedSurvey.id);
                        }}
                        className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center space-x-2 transition-colors"
                      >
                        <FileDown className="h-4 w-4" />
                        <span>View Downloads ({surveyFiles.length})</span>
                      </button>
                    )}
                    {surveySummary && (
                      <button
                        onClick={() => {
                          fetchSurveySummary(selectedSurvey.id);
                        }}
                        className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 flex items-center space-x-2 transition-colors"
                      >
                        <RefreshCw className="h-4 w-4" />
                        <span>Refresh Summary</span>
                      </button>
                    )}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'files' && (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Downloaded Files</h3>
                  <button
                    onClick={() => fetchSurveyFiles(selectedSurvey.id)}
                    className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors"
                    title="Refresh files"
                  >
                    <RefreshCw className={`h-4 w-4 ${loadingFiles ? 'animate-spin' : ''}`} />
                  </button>
                </div>
                {loadingFiles ? (
                  <div className="text-sm text-gray-500 py-8 text-center">Loading files...</div>
                ) : surveyFiles.length === 0 ? (
                  <div className="text-center py-8">
                    <FileDown className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600 mb-4">No files downloaded yet</p>
                    <button
                      onClick={() => handleDownload(selectedSurvey.id, selectedSurvey.name)}
                      disabled={downloadingSurveys.has(selectedSurvey.id)}
                      className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center space-x-2 transition-colors mx-auto"
                    >
                      <Download className="h-4 w-4" />
                      <span>Download Responses</span>
                    </button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {surveyFiles.map((file) => (
                      <div key={file.key} className="p-4 bg-gray-50 rounded-lg border border-gray-200 flex items-center justify-between">
                        <div className="flex-1">
                          <div className="font-medium text-gray-900 mb-2">{file.display_name}</div>
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
                            className="px-4 py-2 text-sm bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center space-x-2 transition-colors"
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
            )}

            {activeTab === 'questions' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Survey Questions</h3>
                {loadingQuestions ? (
                  <div className="text-sm text-gray-500 py-8 text-center">Loading questions...</div>
                ) : surveyQuestions.length === 0 ? (
                  <div className="text-sm text-gray-500 py-8 text-center">No questions found</div>
                ) : (
                  <div className="space-y-3">
                    {surveyQuestions.map((q, index) => (
                      <div key={q.id} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                        <div className="text-sm font-medium text-gray-700 mb-2">
                          Question {index + 1} (ID: {q.id})
                        </div>
                        <div className="text-sm text-gray-900">{q.text}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'responses' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Sample Responses (First 10)</h3>
                {loadingResponses ? (
                  <div className="text-sm text-gray-500 py-8 text-center">Loading responses...</div>
                ) : surveyResponses.length === 0 ? (
                  <div className="text-sm text-gray-500 py-8 text-center">No responses found</div>
                ) : (
                  <div className="space-y-4">
                    {surveyResponses.map((response, index) => (
                      <div key={response.id || index} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                        <div className="text-xs text-gray-500 mb-3 flex items-center justify-between">
                          <span>Response {index + 1} • ID: {response.id || 'N/A'}</span>
                          {response.created_at && (
                            <span>{new Date(response.created_at).toLocaleString()}</span>
                          )}
                        </div>
                        {response.answers && response.answers.length > 0 ? (
                          <div className="space-y-2">
                            {response.answers.map((answer, aIndex) => {
                              let answerText = 'N/A';
                              if (answer && answer.answer !== undefined && answer.answer !== null) {
                                if (typeof answer.answer === 'string') {
                                  answerText = answer.answer;
                                } else if (typeof answer.answer === 'object') {
                                  answerText = answer.answer.content || answer.answer.text || JSON.stringify(answer.answer);
                                } else {
                                  answerText = String(answer.answer);
                                }
                              }
                              
                              return (
                                <div key={aIndex} className="text-sm border-l-2 border-blue-200 pl-3">
                                  <span className="font-medium text-gray-700">Q{answer.question_id || '?'}:</span>{' '}
                                  <span className="text-gray-600">{answerText}</span>
                                </div>
                              );
                            })}
                          </div>
                        ) : (
                          <div className="text-sm text-gray-500">No answers available</div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Default: Show survey list
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Survey Manager</h1>
        <p className="text-gray-600">View and download responses from all your Survicate surveys</p>
      </div>

      {/* Surveys List */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
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
              const hasFiles = surveysWithFiles.has(survey.id);
              
              return (
                <div
                  key={survey.id}
                  className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${
                    'bg-gray-50 border-gray-200 hover:border-gray-300 hover:shadow-md'
                  }`}
                  onClick={() => handleSurveySelect(survey)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="font-medium text-gray-900">{survey.name}</span>
                        {hasFiles && (
                          <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full flex items-center space-x-1">
                            <CheckCircle className="h-3 w-3" />
                            <span>Has Downloads</span>
                          </span>
                        )}
                      </div>
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
    </div>
  );
};

export default SurveyManager;

