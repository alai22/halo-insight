import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { RefreshCw, AlertCircle, Download, Presentation } from 'lucide-react';
import axios from 'axios';
import QuestionTrendsChart from './QuestionTrendsChart';

const ChurnTrendsChart = () => {
  const [data, setData] = useState([]);
  const [reasons, setReasons] = useState([]);
  const [months, setMonths] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [totalResponses, setTotalResponses] = useState(0);
  const [reasonTotals, setReasonTotals] = useState({});
  
  // Weekly chart state
  const [weeklyData, setWeeklyData] = useState([]);
  const [weeklyReasons, setWeeklyReasons] = useState([]);
  const [weeks, setWeeks] = useState([]);
  const [weeklyLoading, setWeeklyLoading] = useState(true);
  const [weeklyError, setWeeklyError] = useState(null);
  const [weeklyTotalResponses, setWeeklyTotalResponses] = useState(0);
  const [weeklyReasonTotals, setWeeklyReasonTotals] = useState({});

  // Google Sheets style: Fixed hue sequence repeated at progressively lower saturation levels
  // Sequence: Blue, Red, Yellow, Green, Orange, Purple, Teal (repeated 3 times with decreasing saturation)
  const colors = [
    // Cycle 1: Vibrant colors
    '#4285F4',  // Blue - vibrant
    '#EA4335',  // Red - vibrant
    '#FBBC04',  // Yellow - vibrant
    '#34A853',  // Green - vibrant
    '#FF6D01',  // Orange - vibrant
    '#9334E6',  // Purple - vibrant
    '#00ACC1',  // Teal - vibrant
    // Cycle 2: Softer pastels (same hue sequence, lower saturation)
    '#64B5F6',  // Blue - softer pastel
    '#F28B82',  // Red - softer pastel
    '#FFF176',  // Yellow - softer pastel
    '#81C784',  // Green - softer pastel
    '#FFB74D',  // Orange - softer pastel
    '#BA68C8',  // Purple - softer pastel
    '#4DB6AC',  // Teal - softer pastel
    // Cycle 3: Very soft pastels (same hue sequence, even lower saturation)
    '#BBDEFB',  // Blue - very soft pastel
    '#FAD2CF',  // Red - very soft pastel
    '#FFF9C4',  // Yellow - very soft pastel
    '#C8E6C9',  // Green - very soft pastel
    '#FFE0B2',  // Orange - very soft pastel
    '#E1BEE7',  // Purple - very soft pastel
    '#B2DFDB',  // Teal - very soft pastel
    // Additional very pale for overflow
    '#E8F0FE',  // Very pale Blue
    '#FCE8E6',  // Very pale Red
  ];

  const fetchChurnTrends = async () => {
    setLoading(true);
    setError(null);
    try {
      // Get data source and file key from localStorage (set by Sidebar)
      const dataSource = localStorage.getItem('survicate_data_source') || 'file';
      const fileKey = localStorage.getItem('survicate_selected_file_key');
      const url = `/api/survicate/churn-trends?data_source=${dataSource}${fileKey && fileKey !== 'latest' ? `&file_key=${encodeURIComponent(fileKey)}` : ''}`;
      const response = await axios.get(url);
      if (response.data.success) {
        setData(response.data.data);
        setReasons(response.data.reasons);
        setMonths(response.data.months);
        setTotalResponses(response.data.total_responses || 0);
        setReasonTotals(response.data.reason_totals || {});
      } else {
        // Handle non-success response
        const errorMsg = response.data.error || 'Failed to load churn trends';
        const details = response.data.details ? ` - ${response.data.details}` : '';
        setError(`${errorMsg}${details}`);
      }
    } catch (err) {
      // Handle axios errors (including 404, 500, etc.)
      const errorMsg = err.response?.data?.error || err.response?.data?.message || err.message || 'Failed to load churn trends';
      const details = err.response?.data?.details ? ` - ${err.response.data.details}` : '';
      setError(`${errorMsg}${details}`);
      console.error('Error fetching churn trends:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchChurnTrendsWeekly = async () => {
    setWeeklyLoading(true);
    setWeeklyError(null);
    try {
      // Get data source and file key from localStorage (set by Sidebar)
      const dataSource = localStorage.getItem('survicate_data_source') || 'file';
      const fileKey = localStorage.getItem('survicate_selected_file_key');
      const url = `/api/survicate/churn-trends-weekly?data_source=${dataSource}${fileKey && fileKey !== 'latest' ? `&file_key=${encodeURIComponent(fileKey)}` : ''}`;
      const response = await axios.get(url);
      if (response.data.success) {
        setWeeklyData(response.data.data);
        setWeeklyReasons(response.data.reasons);
        setWeeks(response.data.weeks);
        setWeeklyTotalResponses(response.data.total_responses || 0);
        setWeeklyReasonTotals(response.data.reason_totals || {});
      } else {
        // Handle non-success response
        const errorMsg = response.data.error || 'Failed to load weekly churn trends';
        const details = response.data.details ? ` - ${response.data.details}` : '';
        setWeeklyError(`${errorMsg}${details}`);
      }
    } catch (err) {
      // Handle axios errors (including 404, 500, etc.)
      const errorMsg = err.response?.data?.error || err.response?.data?.message || err.message || 'Failed to load weekly churn trends';
      const details = err.response?.data?.details ? ` - ${err.response.data.details}` : '';
      setWeeklyError(`${errorMsg}${details}`);
      console.error('Error fetching weekly churn trends:', err);
    } finally {
      setWeeklyLoading(false);
    }
  };

  useEffect(() => {
    fetchChurnTrends();
    fetchChurnTrendsWeekly();
    // Also refresh when data source changes
    const handleStorageChange = () => {
      fetchChurnTrends();
      fetchChurnTrendsWeekly();
    };
    const handleFileChange = () => {
      fetchChurnTrends();
      fetchChurnTrendsWeekly();
    };
    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('survicate-file-changed', handleFileChange);
    // Poll for data source changes (since localStorage events don't fire in same window)
    const interval = setInterval(() => {
      const currentSource = localStorage.getItem('survicate_data_source') || 'file';
      const currentFileKey = localStorage.getItem('survicate_selected_file_key') || 'latest';
      const lastSource = localStorage.getItem('_last_data_source') || 'file';
      const lastFileKey = localStorage.getItem('_last_file_key') || 'latest';
      if (currentSource !== lastSource || currentFileKey !== lastFileKey) {
        localStorage.setItem('_last_data_source', currentSource);
        localStorage.setItem('_last_file_key', currentFileKey);
        fetchChurnTrends();
        fetchChurnTrendsWeekly();
      }
    }, 1000);
    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('survicate-file-changed', handleFileChange);
      clearInterval(interval);
    };
  }, []);

  const handleDownloadPDF = async () => {
    try {
      // Trigger PDF generation on backend
      const response = await axios.post('/api/survicate/generate-pdf-report', {}, {
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'churn_reasons_report.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading PDF:', err);
      alert('Failed to generate PDF. You can run the generate_churn_report.py script manually.');
    }
  };

  const handleDownloadSlides = async () => {
    try {
      // Trigger PowerPoint generation on backend
      const response = await axios.post('/api/survicate/generate-slides-report', {}, {
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'churn_trends_slides.pptx');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading PowerPoint:', err);
      alert('Failed to generate PowerPoint. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full p-8">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 text-blue-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading churn trends data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full p-8">
        <div className="text-center max-w-md">
          <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-2 font-semibold">Error loading data</p>
          <p className="text-gray-600 text-sm mb-4">{error}</p>
          <button
            onClick={fetchChurnTrends}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full p-8">
        <div className="text-center">
          <p className="text-gray-600">No data available</p>
        </div>
      </div>
    );
  }

  // Prepare data for Recharts (stacked bar chart)
  // Also store counts for tooltip display
  const chartData = data.map(item => {
    const chartItem = { month: item.month, _total: item._total || 0 };
    reasons.forEach(reason => {
      chartItem[reason] = item[reason] || 0;
      chartItem[`${reason}_count`] = item[`${reason}_count`] || 0;
    });
    return chartItem;
  });

  // Calculate aggregate "Total" column
  const aggregateData = {
    month: 'Total',
    _total: totalResponses,
    _isAggregate: true // Flag to style differently
  };
  
  reasons.forEach(reason => {
    const totalCount = reasonTotals[reason] || 0;
    const aggregatePercentage = totalResponses > 0 ? (totalCount / totalResponses) * 100 : 0;
    aggregateData[reason] = Math.round(aggregatePercentage * 100) / 100; // Round to 2 decimal places
    aggregateData[`${reason}_count`] = totalCount;
  });

  // Append aggregate column to chart data
  const chartDataWithTotal = [...chartData, aggregateData];

  return (
    <div className="flex flex-col p-4 bg-white" style={{ minHeight: '100vh' }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4 flex-shrink-0">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Churn Reasons Over Time</h2>
          <p className="text-sm text-gray-600 mt-1">
            {totalResponses.toLocaleString()} total responses across {months.length} months
          </p>
          <div className="mt-2 px-3 py-1.5 bg-amber-50 border border-amber-200 rounded-md inline-block">
            <p className="text-xs text-amber-800">
              <span className="font-semibold">Note:</span> November 2024 data excluded due to low response volume
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={fetchChurnTrends}
            className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors flex items-center space-x-2"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Refresh</span>
          </button>
          <button
            onClick={handleDownloadPDF}
            className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
          >
            <Download className="h-4 w-4" />
            <span>Download PDF</span>
          </button>
          <button
            onClick={handleDownloadSlides}
            className="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
          >
            <Presentation className="h-4 w-4" />
            <span>Download Slides</span>
          </button>
        </div>
      </div>

      {/* Chart - Fixed height that won't shrink */}
      <div style={{ height: '900px', flexShrink: 0 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartDataWithTotal}
            margin={{ top: 10, right: 30, left: 20, bottom: 50 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="month" 
              angle={-45}
              textAnchor="end"
              height={80}
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => value}
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
                      fontSize={isTotal ? 13 : 12}
                      fontWeight={isTotal ? '600' : '400'}
                    >
                      {payload.value}
                    </text>
                  </g>
                );
              }}
            />
            <YAxis 
              label={{ value: 'Percentage of Churn (%)', angle: -90, position: 'insideLeft' }}
              domain={[0, 100]}
              ticks={[0, 20, 40, 60, 80, 100]}
              tickFormatter={(value) => `${value}%`}
              tick={{ fontSize: 12 }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#ffffff',
                border: '1px solid #e5e7eb',
                borderRadius: '12px',
                padding: '0',
                boxShadow: '0 8px 16px rgba(0, 0, 0, 0.12)',
                maxWidth: '500px',
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
                
                // Filter to only show segments with non-zero values
                const nonZeroSegments = payload.filter(item => item.value > 0);
                
                if (nonZeroSegments.length === 0) {
                  return null;
                }
                
                // Sort segments by value (highest to lowest) for better readability
                const sortedSegments = [...nonZeroSegments].sort((a, b) => b.value - a.value);
                
                // Get total for this month
                const total = nonZeroSegments[0]?.payload?._total || 0;
                
                return (
                  <div style={{ padding: '12px', backgroundColor: '#ffffff' }}>
                    {/* Header */}
                    <div style={{ 
                      fontWeight: '600', 
                      fontSize: '14px', 
                      color: '#111827', 
                      marginBottom: '8px', 
                      borderBottom: '1px solid #e5e7eb', 
                      paddingBottom: '6px' 
                    }}>
                      {label}
                    </div>
                    
                    {/* Segments list */}
                    <div style={{ 
                      display: 'flex', 
                      flexDirection: 'column', 
                      gap: '4px'
                    }}>
                      {sortedSegments.map((segment, index) => {
                        const reasonName = segment.dataKey;
                        const percentage = segment.value;
                        const count = segment.payload[`${reasonName}_count`] || 0;
                        const color = segment.color;
                        
                        return (
                          <div
                            key={index}
                            style={{
                              display: 'flex',
                              alignItems: 'center',
                              gap: '8px',
                              padding: '4px 6px',
                              borderRadius: '4px',
                              backgroundColor: index % 2 === 0 ? '#ffffff' : '#f9fafb'
                            }}
                          >
                            {/* Color indicator */}
                            <div 
                              style={{ 
                                width: '12px', 
                                height: '12px', 
                                backgroundColor: color,
                                borderRadius: '2px',
                                flexShrink: 0,
                                border: '1px solid rgba(0, 0, 0, 0.1)'
                              }} 
                            />
                            
                            {/* Content */}
                            <div style={{ flex: 1, minWidth: 0 }}>
                              <div style={{ 
                                fontWeight: '500', 
                                color: '#1f2937', 
                                fontSize: '12px', 
                                marginBottom: '2px',
                                lineHeight: '1.3'
                              }}>
                                {reasonName}
                              </div>
                              <div style={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                gap: '6px',
                                fontSize: '11px'
                              }}>
                                <span style={{ 
                                  fontWeight: '600', 
                                  color: '#111827',
                                  fontSize: '12px'
                                }}>
                                  {percentage.toFixed(2)}%
                                </span>
                                {count > 0 && (
                                  <span style={{ 
                                    color: '#6b7280',
                                    fontSize: '10px'
                                  }}>
                                    ({count.toLocaleString()} of {total.toLocaleString()})
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              }}
            />
            <Legend 
              wrapperStyle={{ 
                paddingTop: '10px',
                paddingBottom: '5px'
              }}
              iconType="rect"
              iconSize={14}
              formatter={(value) => {
                // Truncate long labels but keep them readable
                return value.length > 35 ? value.substring(0, 32) + '...' : value;
              }}
              content={({ payload }) => {
                if (!payload || payload.length === 0) return null;
                
                // Sort payload by total count (highest to lowest) to match bar chart order
                const sortedPayload = [...payload].sort((a, b) => {
                  const totalA = reasonTotals[a.dataKey] || 0;
                  const totalB = reasonTotals[b.dataKey] || 0;
                  return totalB - totalA; // Descending order
                });
                
                // Organize legend into columns - use 4-5 columns when there's space
                // Determine number of columns based on screen width and item count
                const screenWidth = window.innerWidth;
                let numColumns = 3; // Default
                if (screenWidth >= 1920) {
                  numColumns = 5; // Large screens
                } else if (screenWidth >= 1440) {
                  numColumns = 4; // Medium-large screens
                } else if (screenWidth >= 1024) {
                  numColumns = 3; // Standard desktop
                } else {
                  numColumns = 2; // Smaller screens
                }
                
                const itemsPerColumn = Math.ceil(sortedPayload.length / numColumns);
                const columns = [];
                for (let i = 0; i < sortedPayload.length; i += itemsPerColumn) {
                  columns.push(sortedPayload.slice(i, i + itemsPerColumn));
                }
                
                return (
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'center', 
                    gap: '40px',
                    padding: '12px 20px 8px 20px',
                    flexWrap: 'wrap',
                    backgroundColor: '#f9fafb',
                    borderRadius: '8px',
                    marginTop: '10px'
                  }}>
                    {columns.map((column, colIndex) => (
                      <div key={colIndex} style={{ 
                        display: 'flex', 
                        flexDirection: 'column', 
                        gap: '10px', 
                        minWidth: '220px',
                        maxWidth: '280px'
                      }}>
                        {column.map((entry, index) => (
                          <div 
                            key={`legend-item-${index}`}
                            style={{ 
                              display: 'flex', 
                              alignItems: 'flex-start', 
                              gap: '10px',
                              fontSize: '13px',
                              lineHeight: '1.6',
                              padding: '4px 0'
                            }}
                          >
                            <div 
                              style={{ 
                                width: '16px', 
                                height: '16px', 
                                backgroundColor: entry.color,
                                borderRadius: '3px',
                                flexShrink: 0,
                                marginTop: '2px',
                                border: '1px solid rgba(0, 0, 0, 0.1)'
                              }} 
                            />
                            <span style={{ 
                              color: '#1f2937',
                              fontWeight: '500',
                              wordBreak: 'break-word'
                            }}>
                              {entry.value}
                            </span>
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>
                );
              }}
            />
            {reasons.map((reason, index) => (
              <Bar
                key={reason}
                dataKey={reason}
                stackId="a"
                fill={colors[index % colors.length]}
                name={reason}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Weekly Chart */}
      <div className="mt-12 pt-8 border-t border-gray-200 flex-shrink-0">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Churn Reasons Over Time (Weekly)</h2>
            <p className="text-sm text-gray-600 mt-1">
              {weeklyTotalResponses.toLocaleString()} total responses across {weeks.length} weeks
            </p>
          </div>
          <button
            onClick={fetchChurnTrendsWeekly}
            className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors flex items-center space-x-2"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Refresh</span>
          </button>
        </div>

        {weeklyLoading ? (
          <div className="flex items-center justify-center h-64 p-8">
            <div className="text-center">
              <RefreshCw className="h-8 w-8 text-blue-500 animate-spin mx-auto mb-4" />
              <p className="text-gray-600">Loading weekly churn trends data...</p>
            </div>
          </div>
        ) : weeklyError ? (
          <div className="flex items-center justify-center h-64 p-8">
            <div className="text-center max-w-md">
              <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-4" />
              <p className="text-red-600 mb-2 font-semibold">Error loading data</p>
              <p className="text-gray-600 text-sm mb-4">{weeklyError}</p>
              <button
                onClick={fetchChurnTrendsWeekly}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Retry
              </button>
            </div>
          </div>
        ) : weeklyData.length === 0 ? (
          <div className="flex items-center justify-center h-64 p-8">
            <div className="text-center">
              <p className="text-gray-600">No weekly data available</p>
            </div>
          </div>
        ) : (
          <>
            {/* Prepare weekly data for Recharts */}
            {(() => {
              const weeklyChartData = weeklyData.map(item => {
                const chartItem = { week: item.week, _total: item._total || 0 };
                weeklyReasons.forEach(reason => {
                  chartItem[reason] = item[reason] || 0;
                  chartItem[`${reason}_count`] = item[`${reason}_count`] || 0;
                });
                return chartItem;
              });

              // Calculate aggregate "Total" column
              const weeklyAggregateData = {
                week: 'Total',
                _total: weeklyTotalResponses,
                _isAggregate: true
              };
              
              weeklyReasons.forEach(reason => {
                const totalCount = weeklyReasonTotals[reason] || 0;
                const aggregatePercentage = weeklyTotalResponses > 0 ? (totalCount / weeklyTotalResponses) * 100 : 0;
                weeklyAggregateData[reason] = Math.round(aggregatePercentage * 100) / 100;
                weeklyAggregateData[`${reason}_count`] = totalCount;
              });

              const weeklyChartDataWithTotal = [...weeklyChartData, weeklyAggregateData];

              // Format week labels to be more compact
              const formatWeekLabel = (weekLabel) => {
                if (weekLabel === 'Total') return 'Total';
                
                // Parse "YYYY-MM-DD to YYYY-MM-DD" format
                const match = weekLabel.match(/(\d{4})-(\d{2})-(\d{2}) to (\d{4})-(\d{2})-(\d{2})/);
                if (match) {
                  const [, startYear, startMonth, startDay, endYear, endMonth, endDay] = match;
                  
                  // Remove leading zeros from month and day
                  const startMonthNum = parseInt(startMonth, 10);
                  const startDayNum = parseInt(startDay, 10);
                  const endMonthNum = parseInt(endMonth, 10);
                  const endDayNum = parseInt(endDay, 10);
                  
                  // If same year, show: "M/D-M/D" (compact format)
                  if (startYear === endYear) {
                    return `${startMonthNum}/${startDayNum}-${endMonthNum}/${endDayNum}`;
                  } else {
                    // Year change - show abbreviated: "M/D/YY-M/D/YY"
                    return `${startMonthNum}/${startDayNum}/${startYear.slice(-2)}-${endMonthNum}/${endDayNum}/${endYear.slice(-2)}`;
                  }
                }
                
                // Fallback to original if format doesn't match
                return weekLabel;
              };

              // Determine how many labels to show (every Nth week)
              // Show more labels if there are fewer weeks, fewer if there are many
              const targetLabelCount = 25; // Target ~25 labels for readability
              const showEveryNth = Math.max(1, Math.floor(weeks.length / targetLabelCount));
              
              return (
                <div style={{ height: '900px', flexShrink: 0 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={weeklyChartDataWithTotal}
                      margin={{ top: 10, right: 30, left: 20, bottom: 100 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis 
                        dataKey="week" 
                        angle={-60}
                        textAnchor="end"
                        height={120}
                        interval={showEveryNth > 1 ? showEveryNth - 1 : 0}
                        tick={{ fontSize: 10 }}
                        tickFormatter={formatWeekLabel}
                        tick={(props) => {
                          const { x, y, payload } = props;
                          const isTotal = payload.value === 'Total';
                          const formattedValue = formatWeekLabel(payload.value);
                          
                          return (
                            <g transform={`translate(${x},${y})`}>
                              <text
                                x={0}
                                y={0}
                                dy={20}
                                textAnchor="end"
                                fill={isTotal ? '#1f2937' : '#6b7280'}
                                fontSize={isTotal ? 12 : 10}
                                fontWeight={isTotal ? '600' : '400'}
                              >
                                {formattedValue}
                              </text>
                            </g>
                          );
                        }}
                      />
                      <YAxis 
                        label={{ value: 'Percentage of Churn (%)', angle: -90, position: 'insideLeft' }}
                        domain={[0, 100]}
                        ticks={[0, 20, 40, 60, 80, 100]}
                        tickFormatter={(value) => `${value}%`}
                        tick={{ fontSize: 12 }}
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
                          
                          // Sort by value (descending) for better readability
                          const sortedPayload = [...payload].sort((a, b) => (b.value || 0) - (a.value || 0));
                          
                          const total = payload[0]?.payload?._total || 0;
                          
                          return (
                            <div style={{ padding: '12px', backgroundColor: '#ffffff' }}>
                              <div style={{ 
                                fontWeight: '600', 
                                fontSize: '13px', 
                                color: '#1f2937', 
                                marginBottom: '8px', 
                                borderBottom: '1px solid #e5e7eb', 
                                paddingBottom: '8px' 
                              }}>
                                Week: {label}
                              </div>
                              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                                {sortedPayload.filter(item => item.value > 0).map((item, index) => {
                                  const reason = item.dataKey;
                                  const percentage = item.value || 0;
                                  const count = item.payload[`${reason}_count`] || 0;
                                  const color = item.color;
                                  
                                  return (
                                    <div key={index} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
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
                                          {reason}
                                        </div>
                                        <div style={{ fontSize: '14px', fontWeight: '700', color: '#1f2937', marginBottom: '2px' }}>
                                          {percentage.toFixed(2)}%
                                        </div>
                                        <div style={{ fontSize: '11px', color: '#6b7280' }}>
                                          {count.toLocaleString()} of {total.toLocaleString()} responses
                                        </div>
                                      </div>
                                    </div>
                                  );
                                })}
                              </div>
                            </div>
                          );
                        }}
                      />
                      <Legend 
                        wrapperStyle={{ 
                          paddingTop: '10px',
                          paddingBottom: '5px'
                        }}
                        iconType="rect"
                        iconSize={14}
                        formatter={(value) => {
                          return value.length > 35 ? value.substring(0, 32) + '...' : value;
                        }}
                        content={({ payload }) => {
                          if (!payload || payload.length === 0) return null;
                          
                          const sortedPayload = [...payload].sort((a, b) => {
                            const totalA = weeklyReasonTotals[a.dataKey] || 0;
                            const totalB = weeklyReasonTotals[b.dataKey] || 0;
                            return totalB - totalA;
                          });
                          
                          const screenWidth = window.innerWidth;
                          let numColumns = 3;
                          if (screenWidth >= 1920) {
                            numColumns = 5;
                          } else if (screenWidth >= 1440) {
                            numColumns = 4;
                          } else if (screenWidth >= 1024) {
                            numColumns = 3;
                          } else {
                            numColumns = 2;
                          }
                          
                          const itemsPerColumn = Math.ceil(sortedPayload.length / numColumns);
                          const columns = [];
                          for (let i = 0; i < sortedPayload.length; i += itemsPerColumn) {
                            columns.push(sortedPayload.slice(i, i + itemsPerColumn));
                          }
                          
                          return (
                            <div style={{ 
                              display: 'flex', 
                              justifyContent: 'center', 
                              gap: '40px',
                              padding: '12px 20px 8px 20px',
                              flexWrap: 'wrap',
                              backgroundColor: '#f9fafb',
                              borderRadius: '8px',
                              marginTop: '10px'
                            }}>
                              {columns.map((column, colIndex) => (
                                <div key={colIndex} style={{ 
                                  display: 'flex', 
                                  flexDirection: 'column', 
                                  gap: '10px', 
                                  minWidth: '220px',
                                  maxWidth: '280px'
                                }}>
                                  {column.map((entry, index) => (
                                    <div 
                                      key={`legend-item-${index}`}
                                      style={{ 
                                        display: 'flex', 
                                        alignItems: 'flex-start', 
                                        gap: '10px',
                                        fontSize: '13px',
                                        lineHeight: '1.6',
                                        padding: '4px 0'
                                      }}
                                    >
                                      <div 
                                        style={{ 
                                          width: '16px', 
                                          height: '16px', 
                                          backgroundColor: entry.color,
                                          borderRadius: '3px',
                                          flexShrink: 0,
                                          marginTop: '2px',
                                          border: '1px solid rgba(0, 0, 0, 0.1)'
                                        }} 
                                      />
                                      <span style={{ 
                                        color: '#1f2937',
                                        fontWeight: '500',
                                        wordBreak: 'break-word'
                                      }}>
                                        {entry.value}
                                      </span>
                                    </div>
                                  ))}
                                </div>
                              ))}
                            </div>
                          );
                        }}
                      />
                      {weeklyReasons.map((reason, index) => (
                        <Bar
                          key={reason}
                          dataKey={reason}
                          stackId="b"
                          fill={colors[index % colors.length]}
                          name={reason}
                        />
                      ))}
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              );
            })()}
          </>
        )}
      </div>

      {/* Additional Question Trends */}
      <div className="mt-8 pt-8 border-t border-gray-200 flex-shrink-0">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Follow-up Survey Question Trends</h3>
        
        {/* Helper function to get color for a parent reason */}
        {(() => {
          const getColorForReason = (reasonName) => {
            const reasonIndex = reasons.findIndex(r => r === reasonName);
            return reasonIndex >= 0 ? colors[reasonIndex % colors.length] : '#6b7280';
          };

          // Helper to convert hex to rgba with opacity
          const hexToRgba = (hex, opacity) => {
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            return `rgba(${r}, ${g}, ${b}, ${opacity})`;
          };

          // Map questions to their parent churn reasons
          const questionGroups = [
            {
              parentReason: 'GPS and Location Accuracy Issues',
              questions: [
                { id: 'Q2', text: 'Q#2: Where does the location pin not match your dog\'s location?' },
                { id: 'Q3', text: 'Q#3: Was the pet location pin grayed out when the location was inaccurate?' }
              ]
            },
            {
              parentReason: 'GPS doesn\'t respond to collar',
              questions: [
                { id: 'Q4', text: 'Q#4: Is the collar not sending feedback or is your dog not responding to the feedback sent?' },
                { id: 'Q5', text: 'Q#5: Did you screw in the contact tips required for static feedback to work properly?' }
              ]
            },
            {
              parentReason: 'Battery life, charging or power issues',
              questions: [
                { id: 'Q6', text: 'Q#6: What battery life, charging or power issues did you encounter?' }
              ]
            },
            {
              parentReason: 'Found Alternative Solution',
              questions: [
                { id: 'Q7', text: 'Q#7: Which containment solution did you purchase?' }
              ]
            }
          ];

          // Other questions without parent reasons
          // Updated to reflect new question order after Q8 was added
          const otherQuestions = [
            { id: 'Q8', text: 'Q#8: Which other GPS or wireless fence did you purchase?' },
            { id: 'Q9', text: 'Q#9: Did you engage with the Learn training curriculum?' },
            { id: 'Q10', text: 'Q#10: What was the main reason you didn\'t complete the Learn curriculum?' },
            { id: 'Q11', text: 'Q#11: Did you contact our Customer Service team via Dog Park?' },
            { id: 'Q12', text: 'Q#12: Would a free session with a trainer to help your dog use the collar effectively have helped you continue to use it?' }
          ];

          return (
            <>
              {/* Grouped questions by parent reason */}
              {questionGroups.map((group, groupIndex) => {
                const parentColor = getColorForReason(group.parentReason);
                return (
                  <div key={groupIndex} className="mb-8">
                    {/* Color-coded section header */}
                    <div 
                      className="mb-4 p-4 rounded-lg border-l-4"
                      style={{ 
                        borderLeftColor: parentColor,
                        backgroundColor: hexToRgba(parentColor, 0.08), // Very light tint of the color
                        borderTop: `1px solid ${hexToRgba(parentColor, 0.2)}`,
                        borderRight: `1px solid ${hexToRgba(parentColor, 0.2)}`,
                        borderBottom: `1px solid ${hexToRgba(parentColor, 0.2)}`
                      }}
                    >
                      <div className="flex items-center gap-3">
                        {/* Color swatch */}
                        <div 
                          className="w-5 h-5 rounded flex-shrink-0"
                          style={{ 
                            backgroundColor: parentColor,
                            border: '1px solid rgba(0, 0, 0, 0.1)',
                            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)'
                          }}
                        />
                        <div className="flex-1">
                          <h4 
                            className="text-base font-semibold mb-1"
                            style={{ color: '#1f2937' }}
                          >
                            {group.parentReason}
                          </h4>
                          <p className="text-sm text-gray-600">
                            Follow-up questions for users who selected this churn reason
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    {/* Questions in this group */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 ml-8">
                      {group.questions.map((q) => (
                        <QuestionTrendsChart 
                          key={q.id}
                          question={q.id}
                          questionText={q.text}
                        />
                      ))}
                    </div>
                  </div>
                );
              })}

              {/* Other questions without parent reasons */}
              {otherQuestions.length > 0 && (
                <div className="mt-8 pt-6 border-t border-gray-200">
                  <h4 className="text-base font-semibold text-gray-900 mb-4">Other Survey Questions</h4>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {otherQuestions.map((q) => (
                      <QuestionTrendsChart 
                        key={q.id}
                        question={q.id}
                        questionText={q.text}
                      />
                    ))}
                  </div>
                </div>
              )}
            </>
          );
        })()}
      </div>
    </div>
  );
};

export default ChurnTrendsChart;

