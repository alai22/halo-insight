import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { RefreshCw, AlertCircle } from 'lucide-react';
import axios from 'axios';

const SurveyQuestionTrendsChart = ({ surveyId, questionKey, questionText }) => {
  const [data, setData] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [totalResponses, setTotalResponses] = useState(0);
  
  // Color palette for answer segments
  const answerColors = [
    '#4285F4',  // Google Blue
    '#EA4335',  // Google Red
    '#FBBC04',  // Google Yellow
    '#34A853',  // Google Green
    '#FF6D01',  // Bright Orange
    '#9334E6',  // Bright Purple
    '#00ACC1',  // Teal
    '#F06292',  // Pink
    '#8D6E63',  // Brown
    '#78909C',  // Blue Grey
  ];

  const fetchQuestionTrends = async () => {
    setLoading(true);
    setError(null);
    try {
      const url = `/api/survicate/surveys/${surveyId}/question-trends?question=${questionKey}`;
      const response = await axios.get(url);
      if (response.data.success) {
        setData(response.data.data);
        setAnswers(response.data.answers || []);
        setTotalResponses(response.data.total_responses || 0);
      } else {
        const errorMsg = response.data.error || 'Failed to load question trends';
        const details = response.data.details ? ` - ${response.data.details}` : '';
        setError(`${errorMsg}${details}`);
      }
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.response?.data?.message || err.message || 'Failed to load question trends';
      const details = err.response?.data?.details ? ` - ${err.response.data.details}` : '';
      setError(`${errorMsg}${details}`);
      console.error('Error fetching question trends:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (surveyId && questionKey) {
      fetchQuestionTrends();
    }
  }, [surveyId, questionKey]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 p-8">
        <div className="text-center">
          <RefreshCw className="h-6 w-6 text-blue-500 animate-spin mx-auto mb-2" />
          <p className="text-gray-600 text-sm">Loading trends...</p>
        </div>
      </div>
    );
  }

  if (error) {
    // For "not found" errors, don't render anything
    if (error.includes('not found') || error.includes('No responses found')) {
      return null;
    }
    
    return (
      <div className="flex items-center justify-center h-64 p-8">
        <div className="text-center max-w-md">
          <AlertCircle className="h-6 w-6 text-red-500 mx-auto mb-2" />
          <p className="text-red-600 text-sm font-semibold">Error loading data</p>
          <p className="text-gray-600 text-xs mb-3">{error}</p>
          <button
            onClick={fetchQuestionTrends}
            className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 p-8">
        <div className="text-center">
          <p className="text-gray-600 text-sm">No trend data available</p>
        </div>
      </div>
    );
  }

  // Prepare chart data - use percentages instead of counts
  const chartData = data.map(item => {
    const chartItem = { month: item.month, _total: item._total || 0 };
    answers.forEach(answer => {
      // Use percentage for the bar value instead of count
      chartItem[answer] = item[`${answer}_percentage`] || 0;
      chartItem[`${answer}_count`] = item[answer] || 0; // Keep count for tooltip
      chartItem[`${answer}_percentage`] = item[`${answer}_percentage`] || 0;
    });
    return chartItem;
  });

  // Calculate aggregate "Total" column
  const aggregateData = {
    month: 'Total',
    _isAggregate: true
  };

  // Sum counts across all months for each answer
  const answerTotals = {};
  let aggregateTotal = 0;
  
  data.forEach(item => {
    aggregateTotal += item._total || 0;
    answers.forEach(answer => {
      const count = item[answer] || 0;
      answerTotals[answer] = (answerTotals[answer] || 0) + count;
    });
  });

  // Calculate aggregate percentages
  answers.forEach(answer => {
    const totalCount = answerTotals[answer] || 0;
    const aggregatePercentage = aggregateTotal > 0 ? (totalCount / aggregateTotal) * 100 : 0;
    aggregateData[answer] = Math.round(aggregatePercentage * 100) / 100;
    aggregateData[`${answer}_count`] = totalCount;
    aggregateData[`${answer}_percentage`] = aggregatePercentage;
  });

  aggregateData._total = aggregateTotal;

  // Append aggregate column to chart data
  const chartDataWithTotal = [...chartData, aggregateData];

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-gray-900 mb-1">{questionText}</h3>
        <p className="text-xs text-gray-500">{totalResponses.toLocaleString()} responses over {data.length} months</p>
      </div>
      
      <div style={{ height: '300px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartDataWithTotal}
            margin={{ top: 10, right: 20, left: 10, bottom: 40 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="month" 
              angle={-45}
              textAnchor="end"
              height={60}
              tick={{ fontSize: 10 }}
              tick={(props) => {
                const { x, y, payload } = props;
                const isTotal = payload.value === 'Total';
                return (
                  <g transform={`translate(${x},${y})`}>
                    <text
                      x={0}
                      y={0}
                      dy={16}
                      textAnchor="end"
                      fill={isTotal ? '#1f2937' : '#6b7280'}
                      fontSize={isTotal ? 11 : 10}
                      fontWeight={isTotal ? '600' : '400'}
                    >
                      {payload.value}
                    </text>
                  </g>
                );
              }}
            />
            <YAxis 
              label={{ value: '%', angle: -90, position: 'insideLeft', fontSize: 10 }}
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
              tickFormatter={(value) => `${value}%`}
              tick={{ fontSize: 10 }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#ffffff',
                border: '1px solid #e5e7eb',
                borderRadius: '12px',
                padding: '0',
                boxShadow: '0 8px 16px rgba(0, 0, 0, 0.12)',
                maxWidth: '350px',
                opacity: 1
              }}
              wrapperStyle={{ 
                opacity: 1,
                backgroundColor: '#ffffff'
              }}
              cursor={{ fill: 'rgba(0, 0, 0, 0.05)' }}
              content={({ active, payload, label }) => {
                if (!active || !payload || payload.length === 0) {
                  return null;
                }
                
                // Find the non-zero segment being hovered
                const activeSegment = payload.find(item => item.value > 0);
                if (!activeSegment) return null;
                
                const answerName = activeSegment.dataKey;
                const percentage = activeSegment.value;
                const count = activeSegment.payload[`${answerName}_count`] || 0;
                const total = activeSegment.payload._total || 0;
                const color = activeSegment.color;
                
                return (
                  <div style={{ padding: '10px', backgroundColor: '#ffffff' }}>
                    <div style={{ 
                      fontWeight: '600', 
                      fontSize: '12px', 
                      color: '#1f2937', 
                      marginBottom: '6px', 
                      borderBottom: '1px solid #e5e7eb', 
                      paddingBottom: '6px' 
                    }}>
                      {label === 'Total' ? 'All Time' : `Month: ${label}`}
                    </div>
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                      <div 
                        style={{ 
                          width: '12px', 
                          height: '12px', 
                          backgroundColor: color,
                          borderRadius: '2px',
                          flexShrink: 0,
                          marginTop: '2px'
                        }} 
                      />
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: '600', color: '#1f2937', fontSize: '12px', marginBottom: '3px' }}>
                          {answerName}
                        </div>
                        <div style={{ fontSize: '14px', fontWeight: '700', color: '#1f2937', marginBottom: '2px' }}>
                          {percentage.toFixed(1)}%
                        </div>
                        <div style={{ fontSize: '11px', color: '#6b7280' }}>
                          {count.toLocaleString()} of {total.toLocaleString()} responses
                        </div>
                      </div>
                    </div>
                  </div>
                );
              }}
            />
            <Legend 
              wrapperStyle={{ paddingTop: '10px', fontSize: '10px' }}
              iconType="rect"
              iconSize={10}
            />
            {answers.map((answer, index) => (
              <Bar
                key={answer}
                dataKey={answer}
                stackId="a"
                fill={answerColors[index % answerColors.length]}
                name={answer}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default SurveyQuestionTrendsChart;
