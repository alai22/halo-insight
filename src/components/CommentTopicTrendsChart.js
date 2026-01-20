import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { RefreshCw, AlertCircle, Play, MessageSquare } from 'lucide-react';
import axios from 'axios';

const CommentTopicTrendsChart = ({ surveyId, questionKey = 'Q1', questionText }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [needsAnalysis, setNeedsAnalysis] = useState(false);

  const fetchTopicTrends = async () => {
    setLoading(true);
    setError(null);
    setNeedsAnalysis(false);
    try {
      const response = await axios.get(`/api/survicate/surveys/${surveyId}/comment-topic-trends?question=${questionKey}`);
      if (response.data.success) {
        setData(response.data);
      } else {
        if (response.data.error?.includes('No topic analysis found') || response.data.error?.includes('run topic analysis')) {
          setNeedsAnalysis(true);
        } else {
          setError(response.data.error || 'Failed to load topic trends');
        }
      }
    } catch (err) {
      if (err.response?.status === 404) {
        setNeedsAnalysis(true);
      } else {
        setError(err.response?.data?.error || err.message || 'Failed to load topic trends');
      }
    } finally {
      setLoading(false);
    }
  };

  const runTopicAnalysis = async () => {
    setAnalyzing(true);
    setError(null);
    try {
      const response = await axios.post(`/api/survicate/surveys/${surveyId}/analyze-comment-topics`, {
        question: questionKey,
        batch_size: 20
      });
      if (response.data.success) {
        // Analysis complete, fetch the trends
        await fetchTopicTrends();
      } else {
        setError(response.data.error || 'Failed to analyze topics');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to analyze topics');
    } finally {
      setAnalyzing(false);
    }
  };

  useEffect(() => {
    if (surveyId && questionKey) {
      fetchTopicTrends();
    }
  }, [surveyId, questionKey]);

  if (loading) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <RefreshCw className="h-8 w-8 text-blue-500 animate-spin mx-auto mb-2" />
            <p className="text-gray-600">Loading topic trends...</p>
          </div>
        </div>
      </div>
    );
  }

  if (needsAnalysis) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <MessageSquare className="h-5 w-5 text-amber-600" />
          <h3 className="text-lg font-semibold text-gray-900">Comment Topic Analysis</h3>
        </div>
        <div className="text-center py-8 bg-amber-50 rounded-lg border border-amber-200">
          <MessageSquare className="h-12 w-12 text-amber-400 mx-auto mb-4" />
          <p className="text-gray-700 mb-2 font-medium">Topic analysis not yet run</p>
          <p className="text-sm text-gray-600 mb-4">
            Analyze comments to categorize them by topic and see trends over time.
          </p>
          <button
            onClick={runTopicAnalysis}
            disabled={analyzing}
            className="px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center space-x-2 mx-auto transition-colors"
          >
            {analyzing ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                <span>Analyzing comments...</span>
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                <span>Run Topic Analysis</span>
              </>
            )}
          </button>
          {analyzing && (
            <p className="text-xs text-gray-500 mt-3">
              This may take a few minutes depending on the number of comments.
            </p>
          )}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
            <p className="text-red-600 font-medium">Error loading topic trends</p>
            <p className="text-sm text-gray-600 mt-1">{error}</p>
            <button
              onClick={fetchTopicTrends}
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!data || !data.monthly_data || data.monthly_data.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="text-center py-8">
          <p className="text-gray-600">No topic data available</p>
        </div>
      </div>
    );
  }

  // Prepare chart data - transform monthly_data into chart-friendly format
  const chartData = data.monthly_data.map(month => {
    const entry = { month: month.month, _total: month.total_comments };
    Object.entries(month.topics).forEach(([topicId, topicData]) => {
      entry[topicId] = topicData.percentage;
      entry[`${topicId}_count`] = topicData.count;
    });
    return entry;
  });

  // Get topics that have data, sorted by overall frequency
  const activeTopics = Object.entries(data.overall_distribution)
    .filter(([_, d]) => d.count > 0)
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 10); // Top 10 topics

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <MessageSquare className="h-5 w-5 text-amber-600" />
          <h3 className="text-lg font-semibold text-gray-900">Comment Topic Trends</h3>
          <span className="px-2 py-0.5 bg-amber-100 text-amber-700 text-xs rounded-full">
            {data.total_comments?.toLocaleString()} comments
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={runTopicAnalysis}
            disabled={analyzing}
            className="px-3 py-1 text-sm bg-amber-100 text-amber-700 rounded hover:bg-amber-200 disabled:opacity-50 flex items-center space-x-1"
            title="Re-run topic analysis"
          >
            {analyzing ? (
              <RefreshCw className="h-3 w-3 animate-spin" />
            ) : (
              <RefreshCw className="h-3 w-3" />
            )}
            <span>Re-analyze</span>
          </button>
        </div>
      </div>

      {questionText && (
        <p className="text-sm text-gray-600 mb-4">{questionText}</p>
      )}

      {/* Topic Distribution Summary */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3">Overall Topic Distribution</h4>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
          {activeTopics.map(([topicId, topicData]) => (
            <div 
              key={topicId} 
              className="p-2 rounded-lg border"
              style={{ borderColor: topicData.color + '40', backgroundColor: topicData.color + '10' }}
            >
              <div className="text-xs font-medium text-gray-800 truncate" title={topicData.name}>
                {topicData.name}
              </div>
              <div className="flex items-baseline space-x-1">
                <span className="text-lg font-bold" style={{ color: topicData.color }}>
                  {topicData.percentage.toFixed(1)}%
                </span>
                <span className="text-xs text-gray-500">
                  ({topicData.count})
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Monthly Trends Chart */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-3">Monthly Trends (% of comments mentioning each topic)</h4>
      </div>
      
      <div style={{ height: '400px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 10, right: 20, left: 10, bottom: 60 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="month" 
              angle={-45}
              textAnchor="end"
              height={80}
              tick={{ fontSize: 11 }}
            />
            <YAxis 
              label={{ value: '% of Comments', angle: -90, position: 'insideLeft', fontSize: 11 }}
              tickFormatter={(value) => `${value}%`}
              tick={{ fontSize: 11 }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#ffffff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
              }}
              content={({ active, payload, label }) => {
                if (!active || !payload || payload.length === 0) return null;
                
                const monthData = chartData.find(d => d.month === label);
                if (!monthData) return null;
                
                return (
                  <div className="p-3 bg-white rounded-lg shadow-lg border max-w-xs">
                    <div className="font-semibold text-gray-900 mb-2 border-b pb-2">
                      {label} ({monthData._total} comments)
                    </div>
                    <div className="space-y-1">
                      {payload
                        .filter(p => p.value > 0)
                        .sort((a, b) => b.value - a.value)
                        .slice(0, 8)
                        .map((entry, idx) => (
                          <div key={idx} className="flex items-center justify-between text-sm">
                            <div className="flex items-center space-x-2">
                              <div 
                                className="w-3 h-3 rounded"
                                style={{ backgroundColor: entry.color }}
                              />
                              <span className="text-gray-700 truncate max-w-32">
                                {data.topic_names[entry.dataKey] || entry.dataKey}
                              </span>
                            </div>
                            <span className="font-medium ml-2">
                              {entry.value.toFixed(1)}%
                            </span>
                          </div>
                        ))}
                    </div>
                  </div>
                );
              }}
            />
            <Legend 
              wrapperStyle={{ paddingTop: '20px', fontSize: '10px' }}
              iconType="rect"
              iconSize={10}
            />
            {activeTopics.map(([topicId, topicData]) => (
              <Bar
                key={topicId}
                dataKey={topicId}
                name={topicData.name}
                fill={topicData.color}
                stackId="topics"
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default CommentTopicTrendsChart;
