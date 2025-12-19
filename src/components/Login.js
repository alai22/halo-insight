import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Login({ onLogin, onAdminLogin, requireAdmin = false }) {
  const [error, setError] = useState('');
  const [googleEnabled, setGoogleEnabled] = useState(false);

  // Check if Google OAuth is enabled
  useEffect(() => {
    const checkGoogleEnabled = async () => {
      try {
        const response = await axios.get('/api/auth/google/enabled');
        setGoogleEnabled(response.data.enabled);
      } catch (error) {
        console.error('Error checking Google OAuth service:', error);
        setGoogleEnabled(false);
      }
    };
    checkGoogleEnabled();
  }, []);

  // Check if we're returning from Google OAuth
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const authParam = urlParams.get('auth');
    const emailParam = urlParams.get('email');
    const messageParam = urlParams.get('message');
    
    if (authParam === 'success' && emailParam) {
      // Successfully authenticated via Google OAuth
      // Clear URL params
      window.history.replaceState({}, document.title, window.location.pathname);
      // Trigger login - check if admin login is needed
      setTimeout(() => {
        if (requireAdmin && onAdminLogin) {
          onAdminLogin();
        } else {
          onLogin();
        }
      }, 1000);
    } else if (authParam === 'error') {
      // Authentication error from Google OAuth
      setError(messageParam || 'Authentication failed. Please try again.');
      // Clear URL params
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [onLogin, onAdminLogin, requireAdmin]);

  const handleGoogleLogin = () => {
    // Redirect to Google OAuth login endpoint
    window.location.href = '/api/auth/google/login';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-300 via-yellow-400 to-yellow-500 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl p-8 w-full max-w-md">
        <div className="flex items-center justify-center mb-4">
          <img 
            src="/dog-spark.jpg" 
            alt="Halo Insight Logo" 
            className="h-32 w-32 rounded-full object-cover shadow-md"
          />
        </div>
        <h1 className="text-2xl font-bold text-center text-gray-900 mb-4">
          {requireAdmin ? 'Admin Login' : 'Halo Insight'}
        </h1>
        
        {!requireAdmin && (
          <div className="text-sm text-gray-600 text-center mb-6 space-y-2">
            <p>Customer support conversation analysis and churn insights.</p>
            <p>Analyze Gladly conversations, survey responses, and identify trends.</p>
          </div>
        )}
        
        {requireAdmin && (
          <div className="text-sm text-gray-600 text-center mb-6 space-y-2">
            <p className="text-orange-600 font-semibold">Admin Access Required</p>
            <p>Sign in with your admin Google account to access admin tools.</p>
          </div>
        )}
        
        {/* Google SSO Button - only authentication method */}
        {googleEnabled ? (
          <div className="mb-6">
            <button
              onClick={handleGoogleLogin}
              className="w-full bg-white border-2 border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors flex items-center justify-center gap-3 shadow-sm"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Sign in with Google
            </button>
          </div>
        ) : (
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-yellow-800 text-sm text-center">
              Google SSO is not configured. Please contact your administrator.
            </p>
          </div>
        )}
        
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}
        
        <p className="text-xs text-gray-500 text-center mt-6">
          Secured with Google SSO
        </p>
      </div>
    </div>
  );
}

export default Login;

