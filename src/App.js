import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Settings, Database, MessageSquare, Search, Download, BarChart3 } from 'lucide-react';
import PromptInput from './components/PromptInput';
import ConversationDisplay from './components/ConversationDisplay';
import Sidebar from './components/Sidebar';
import SettingsPanel from './components/SettingsPanel';
import Login from './components/Login';
import TabNavigation from './components/TabNavigation';
import DownloadManager from './components/DownloadManager';
import ChurnTrendsChart from './components/ChurnTrendsChart';
import ConversationTrendsChart from './components/ConversationTrendsChart';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';

// Configure axios to send credentials (cookies) with all requests
axios.defaults.withCredentials = true;

// Add interceptor to include auth token in headers (temporary workaround for session issues)
axios.interceptors.request.use(
  (config) => {
    const authToken = localStorage.getItem('auth_token');
    if (authToken) {
      config.headers['X-Auth-Token'] = authToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

function App() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [conversations, setConversations] = useState({
    claude: [],
    conversations: [],
    ask: [],
    download: [],
    survicate: [],
    'churn-trends': [],
    'conversation-trends': []
  });
  
  // Initialize currentMode from URL or default
  const [currentMode, setCurrentMode] = useState(() => {
    // Check URL first, then localStorage, then default
    const urlMode = searchParams.get('mode');
    if (urlMode) {
      return urlMode;
    }
    const savedMode = localStorage.getItem('gladly_current_mode');
    return savedMode || 'churn-trends';
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showSettings, setShowSettings] = useState(false);
  const [settings, setSettings] = useState({
    model: 'claude-sonnet-4',  // Default to Sonnet 4 (non-dated alias)
    maxTokens: 1000,
    systemPrompt: '',
    stream: false
  });
  const [healthStatus, setHealthStatus] = useState(null);
  const [adminMode, setAdminMode] = useState(null); // 'claude' or 'download' for admin tools
  
  // Ref to prevent infinite loops when syncing URL and currentMode
  const isSyncingRef = useRef(false);
  
  // Sync URL when currentMode changes (but not when URL changes)
  useEffect(() => {
    if (isSyncingRef.current) return;
    const currentUrlMode = searchParams.get('mode');
    if (currentMode && currentMode !== currentUrlMode) {
      isSyncingRef.current = true;
      setSearchParams({ mode: currentMode }, { replace: true });
      setTimeout(() => { isSyncingRef.current = false; }, 0);
    }
  }, [currentMode, searchParams, setSearchParams]);
  
  // Sync currentMode when URL changes (e.g., browser back/forward or direct link)
  useEffect(() => {
    if (isSyncingRef.current) return;
    const urlMode = searchParams.get('mode');
    if (urlMode && urlMode !== currentMode) {
      isSyncingRef.current = true;
      setCurrentMode(urlMode);
      setTimeout(() => { isSyncingRef.current = false; }, 0);
    } else if (!urlMode && currentMode) {
      // If URL has no mode but we have a currentMode, update URL
      isSyncingRef.current = true;
      setSearchParams({ mode: currentMode }, { replace: true });
      setTimeout(() => { isSyncingRef.current = false; }, 0);
    }
  }, [searchParams, currentMode, setSearchParams]);

  // Load conversations and settings from localStorage on mount
  useEffect(() => {
    try {
      const savedConversations = localStorage.getItem('gladly_conversations');
      if (savedConversations) {
        const parsed = JSON.parse(savedConversations);
        setConversations(prev => ({
          ...prev,
          ...parsed
        }));
      }
    } catch (error) {
      console.error('Error loading conversations from localStorage:', error);
    }

    try {
      const savedSettings = localStorage.getItem('gladly_settings');
      if (savedSettings) {
        const parsed = JSON.parse(savedSettings);
        setSettings(prev => ({
          ...prev,
          ...parsed
        }));
      }
    } catch (error) {
      console.error('Error loading settings from localStorage:', error);
    }

    // URL mode takes precedence, so we don't override it here
    // The initial state already handles localStorage fallback
  }, []);

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem('gladly_conversations', JSON.stringify(conversations));
    } catch (error) {
      console.error('Error saving conversations to localStorage:', error);
    }
  }, [conversations]);

  // Save settings to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem('gladly_settings', JSON.stringify(settings));
    } catch (error) {
      console.error('Error saving settings to localStorage:', error);
    }
  }, [settings]);

  // Save current mode to localStorage whenever it changes
  useEffect(() => {
    try {
      localStorage.setItem('gladly_current_mode', currentMode);
    } catch (error) {
      console.error('Error saving current mode to localStorage:', error);
    }
  }, [currentMode]);

  // Check if user is already authenticated (check localStorage token first, then backend session)
  useEffect(() => {
    const checkAuthStatus = async () => {
      // First check localStorage for auth token (temporary workaround)
      const authToken = localStorage.getItem('auth_token');
      
      // If token exists, trust it immediately (temporary workaround)
      if (authToken) {
        console.log('Initial auth check - token found, setting authenticated to true');
        setIsAuthenticated(true);
        return;
      }
      
      // If no token, check backend session
      try {
        const response = await axios.get('/api/auth/status');
        
        if (response.data.authenticated) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        setIsAuthenticated(false);
      }
    };
    checkAuthStatus();
  }, []);

  // Check backend health on component mount (only when authenticated)
  useEffect(() => {
    if (isAuthenticated) {
      checkHealth();
    }
  }, [isAuthenticated]);

  const handleLogin = async () => {
    // Check localStorage first - if token exists, we're authenticated
    const authToken = localStorage.getItem('auth_token');
    console.log('handleLogin - authToken from localStorage:', authToken ? 'found' : 'not found');
    
    // If we have a token, immediately set authenticated to true
    // This is a temporary workaround - in production with FLASK_SECRET_KEY, sessions will work
    if (authToken) {
      console.log('handleLogin - token found, setting authenticated to true immediately');
      setIsAuthenticated(true);
      return;
    }
    
    // If no token, verify authentication with backend session
    try {
      const response = await axios.get('/api/auth/status');
      
      console.log('handleLogin - auth status response:', response.data);
      
      if (response.data.authenticated) {
        console.log('handleLogin - setting authenticated to true');
        setIsAuthenticated(true);
      } else {
        // If not authenticated, stay on login screen
        console.log('handleLogin - not authenticated');
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
      setIsAuthenticated(false);
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post('/api/auth/logout');
    } catch (error) {
      console.error('Error during logout:', error);
    } finally {
      // Clear localStorage auth token
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_method');
      setIsAuthenticated(false);
    }
  };

  const checkHealth = async () => {
    try {
      const response = await axios.get('/api/health');
      setHealthStatus(response.data);
    } catch (error) {
      setHealthStatus({ status: 'unhealthy', error: error.message });
    }
  };

  // If not authenticated, show login screen
  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  const addConversation = (type, userMessage, response, metadata = {}) => {
    const newConversation = {
      id: Date.now(),
      type,
      timestamp: new Date().toISOString(),
      userMessage,
      response,
      metadata
    };
    const mode = adminMode || currentMode;
    setConversations(prev => ({
      ...prev,
      [mode]: [...(prev[mode] || []), newConversation]
    }));
  };

  // Get current mode's conversations
  const getCurrentConversations = () => {
    const mode = adminMode || currentMode;
    return conversations[mode] || [];
  };

  const handleClaudeMessage = async (message) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/claude/chat', {
        message,
        model: settings.model,
        max_tokens: settings.maxTokens,
        system_prompt: settings.systemPrompt || undefined,
        stream: settings.stream
      });

      if (response.data.success) {
        let responseText = '';
        if (response.data.streamed) {
          // Process streamed response
          for (const chunk of response.data.response) {
            if (chunk.content && chunk.content.length > 0) {
              for (const contentBlock of chunk.content) {
                if (contentBlock.type === 'text') {
                  responseText += contentBlock.text;
                }
              }
            }
          }
        } else {
          // Process regular response
          if (response.data.response.content && response.data.response.content.length > 0) {
            for (const contentBlock of response.data.response.content) {
              if (contentBlock.type === 'text') {
                responseText += contentBlock.text;
              }
            }
          }
        }

        addConversation('claude', message, responseText, {
          model: settings.model,
          tokens: response.data.response.usage?.output_tokens || 0
        });
      } else {
        throw new Error(response.data.error || 'Unknown error');
      }
    } catch (error) {
      setError(error.response?.data?.error || error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleConversationSearch = async (query) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/conversations/search', {
        query,
        limit: 10
      });

      if (response.data.success) {
        const results = response.data.results;
        const formattedResults = results.map((item, index) => {
          const content = item.content || {};
          return `**Result ${index + 1}**\n` +
                 `Type: ${content.type || 'Unknown'}\n` +
                 `Timestamp: ${item.timestamp || 'Unknown'}\n` +
                 `Customer: ${item.customerId || 'Unknown'}\n` +
                 `Content: ${content.content || content.subject || content.body || 'No content'}\n`;
        }).join('\n---\n');

        addConversation('search', query, formattedResults, {
          resultCount: results.length
        });
      } else {
        throw new Error(response.data.error || 'Unknown error');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || error.message;
      const errorDetails = error.response?.data?.details;
      setError(errorDetails ? `${errorMessage}\n\n${errorDetails}` : errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleConversationAsk = async (question) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/conversations/ask', {
        question,
        model: settings.model,
        max_tokens: settings.maxTokens
      }, {
        timeout: 120000 // 2 minutes timeout for RAG requests
      });

      if (response.data.success) {
        let responseText = '';
        if (response.data.response.content && response.data.response.content.length > 0) {
          for (const contentBlock of response.data.response.content) {
            if (contentBlock.type === 'text') {
              responseText += contentBlock.text;
            }
          }
        }

        addConversation('ask', question, responseText, {
          dataRetrieved: response.data.data_retrieved,
          plan: response.data.plan,
          ragProcess: response.data.rag_process,
          tokensUsed: response.data.response.usage?.output_tokens || 0,
          model: settings.model
        });
      } else {
        throw new Error(response.data.error || 'Unknown error');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || error.message;
      const errorDetails = error.response?.data?.details;
      setError(errorDetails ? `${errorMessage}\n\n${errorDetails}` : errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSurvicateAsk = async (question) => {
    setIsLoading(true);
    setError(null);

    try {
      // Get data source from localStorage (set by Sidebar)
      const dataSource = localStorage.getItem('survicate_data_source') || 'file';
      
      const response = await axios.post('/api/survicate/ask', {
        question,
        model: settings.model,
        max_tokens: settings.maxTokens,
        data_source: dataSource
      }, {
        timeout: 120000 // 2 minutes timeout for RAG requests
      });

      if (response.data.success) {
        let responseText = '';
        if (response.data.response.content && response.data.response.content.length > 0) {
          for (const contentBlock of response.data.response.content) {
            if (contentBlock.type === 'text') {
              responseText += contentBlock.text;
            }
          }
        }

        addConversation('survicate', question, responseText, {
          dataRetrieved: response.data.data_retrieved,
          plan: response.data.plan,
          ragProcess: response.data.rag_process,
          tokensUsed: response.data.response.usage?.output_tokens || 0,
          model: settings.model
        });
      } else {
        throw new Error(response.data.error || 'Unknown error');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || error.message;
      const errorDetails = error.response?.data?.details;
      setError(errorDetails ? `${errorMessage}\n\n${errorDetails}` : errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = (message) => {
    if (!message.trim()) return;

    // Check admin mode first
    if (adminMode === 'claude') {
      handleClaudeMessage(message);
      return;
    }

    switch (currentMode) {
      case 'conversations':
        handleConversationSearch(message);
        break;
      case 'ask':
        handleConversationAsk(message);
        break;
      case 'survicate':
        handleSurvicateAsk(message);
        break;
      default:
        handleConversationAsk(message);
    }
  };

  // Clear conversations for the current mode only
  const clearCurrentConversations = () => {
    const mode = adminMode || currentMode;
    setConversations(prev => ({
      ...prev,
      [mode]: []
    }));
    setError(null);
  };

  // Clear all conversations across all modes
  const clearAllConversations = () => {
    setConversations({
      claude: [],
      conversations: [],
      ask: [],
      download: [],
      survicate: [],
      'churn-trends': []
    });
    setError(null);
  };

  const getCurrentConversationCount = () => {
    return getCurrentConversations().length;
  };

  const getModeTitle = () => {
    const modeTitles = {
      'conversation-trends': 'Conversation Trends',
      'claude': 'Claude Chat',
      'conversations': 'Search Conversations', 
      'ask': 'Ask About Conversations',
      'download': 'Download Manager',
      'survicate': 'Ask About Churn',
      'churn-trends': 'Churn Trends'
    };
    if (adminMode) {
      return modeTitles[adminMode] || 'Admin Mode';
    }
    return modeTitles[currentMode] || 'Unknown Mode';
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <Sidebar 
        healthStatus={healthStatus}
        onRefreshHealth={checkHealth}
        currentMode={currentMode}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {adminMode ? (
                <div className="flex items-center space-x-3 px-4 py-2 bg-orange-50 border-2 border-orange-200 rounded-lg">
                  <span className="text-sm font-medium text-orange-900">
                    Admin Mode: {getModeTitle()}
                  </span>
                  <button
                    onClick={() => {
                      setAdminMode(null);
                      setCurrentMode('ask');
                    }}
                    className="text-xs text-orange-600 hover:text-orange-800 underline"
                  >
                    Exit
                  </button>
                </div>
              ) : (
                <TabNavigation 
                  currentMode={currentMode} 
                  setCurrentMode={setCurrentMode} 
                />
              )}
              {getCurrentConversationCount() > 0 && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {getCurrentConversationCount()} messages
                </span>
              )}
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={handleLogout}
                className="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
                title="Logout"
              >
                Logout
              </button>
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                title="Settings"
              >
                <Settings className="h-5 w-5" />
              </button>
              {!adminMode && (
                <div className="flex items-center space-x-2">
                  <button
                    onClick={clearCurrentConversations}
                    disabled={getCurrentConversationCount() === 0}
                    className="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Clear {getModeTitle()}
                  </button>
                  <button
                    onClick={clearAllConversations}
                    className="px-3 py-2 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    Clear All
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Settings Panel */}
        {showSettings && (
          <SettingsPanel
            settings={settings}
            setSettings={setSettings}
            adminMode={adminMode}
            setAdminMode={setAdminMode}
            setCurrentMode={setCurrentMode}
            onClose={() => setShowSettings(false)}
          />
        )}

        {/* Main Content Area */}
        <div className={`flex-1 ${currentMode === 'churn-trends' || currentMode === 'conversation-trends' || adminMode === 'download' ? 'overflow-y-auto' : 'overflow-hidden'}`}>
          {adminMode === 'download' ? (
            <DownloadManager />
          ) : currentMode === 'churn-trends' ? (
            <ChurnTrendsChart />
          ) : currentMode === 'conversation-trends' ? (
            <ConversationTrendsChart />
          ) : (
            <ConversationDisplay
              conversations={getCurrentConversations()}
              isLoading={isLoading}
              error={error}
            />
          )}
        </div>

        {/* Prompt Input */}
        {adminMode !== 'download' && currentMode !== 'churn-trends' && currentMode !== 'conversation-trends' && (
          <div className="bg-white border-t border-gray-200 p-6">
            <PromptInput
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              placeholder={
                adminMode === 'claude' ? 'Ask Claude anything...' :
                currentMode === 'conversations' ? 'Search Gladly conversation data...' :
                currentMode === 'survicate' ? 'Ask about cancellation survey data (e.g., "What are the main cancellation reasons?")' :
                'Ask Claude to analyze your conversation data (e.g., "What are the main customer complaints?")'
              }
              exampleQuestions={
                currentMode === 'ask' ? [
                  'What are the main customer complaints or issues mentioned in the conversations?',
                  'What are the most common topics or themes in the conversation data?',
                  'Analyze customer sentiment and satisfaction trends in the conversations'
                ] : currentMode === 'survicate' ? [
                  'What are the main reasons customers canceled their Halo Pack Membership?',
                  'How have GPS and location accuracy complaints changed over time?',
                  'What are the most common themes in customer feedback about battery life and charging issues?'
                ] : []
              }
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
