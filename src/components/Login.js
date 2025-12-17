import React, { useState, useEffect } from 'react';
import { Mail, CheckCircle, Loader } from 'lucide-react';
import axios from 'axios';

function Login({ onLogin, onAdminLogin, requireAdmin = false }) {
  const [authMethod, setAuthMethod] = useState('password'); // 'password', 'magic-link', or 'google'
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [emailEnabled, setEmailEnabled] = useState(false);
  const [googleEnabled, setGoogleEnabled] = useState(false);

  // Check if email service is enabled
  useEffect(() => {
    const checkEmailEnabled = async () => {
      try {
        const response = await axios.get('/api/auth/email-enabled');
        setEmailEnabled(response.data.enabled);
      } catch (error) {
        console.error('Error checking email service:', error);
        setEmailEnabled(false);
      }
    };
    checkEmailEnabled();
  }, []);

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
    if (!requireAdmin) {
      checkGoogleEnabled();
    }
  }, [requireAdmin]);

  // Check if we're returning from a magic link or Google OAuth
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const authParam = urlParams.get('auth');
    const emailParam = urlParams.get('email');
    const messageParam = urlParams.get('message');
    
    if (authParam === 'success' && emailParam) {
      // Successfully authenticated via magic link or Google OAuth
      setUserEmail(emailParam);
      setEmailSent(false);
      // Clear URL params
      window.history.replaceState({}, document.title, window.location.pathname);
      // Trigger login
      setTimeout(() => {
        onLogin();
      }, 1000);
    } else if (authParam === 'error') {
      // Authentication error (from Google OAuth or magic link)
      setError(messageParam || 'Authentication failed. Please try again.');
      // Clear URL params
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [onLogin]);

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // If requireAdmin is true, use admin login endpoint
      const endpoint = requireAdmin ? '/api/auth/admin-login' : '/api/auth/password-login';
      const response = await axios.post(endpoint, {
        password: password
      }, {
        withCredentials: true  // Important for session cookies
      });

      if (response.data.success) {
        // Password validated on backend
        // If session is available, it's already created
        // If not, store auth token in localStorage (temporary workaround)
        if (requireAdmin) {
          // Admin login
          if (!response.data.session_available && response.data.admin_token) {
            localStorage.setItem('admin_token', response.data.admin_token);
            localStorage.setItem('auth_method', 'admin_password');
            console.log('Stored admin token in localStorage (session unavailable)');
            await new Promise(resolve => setTimeout(resolve, 100));
          }
          if (onAdminLogin) {
            onAdminLogin();
          }
        } else {
          // Regular login
          if (!response.data.session_available && response.data.auth_token) {
            localStorage.setItem('auth_token', response.data.auth_token);
            localStorage.setItem('auth_method', 'password');
            console.log('Stored auth token in localStorage (session unavailable)');
            await new Promise(resolve => setTimeout(resolve, 100));
          }
          onLogin();
        }
        setError('');
      } else {
        setError(response.data.error || 'Incorrect password');
        setPassword('');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.error || 'Failed to login. Please try again.');
      setPassword('');
    } finally {
      setLoading(false);
    }
  };

  const handleMagicLinkSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Basic email validation
    if (!email || !email.includes('@')) {
      setError('Please enter a valid email address');
      setLoading(false);
      return;
    }

    // Check domain (client-side validation - backend also validates)
    if (!email.toLowerCase().endsWith('@halocollar.com')) {
      setError('Only @halocollar.com email addresses are allowed');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post('/api/auth/request-login', {
        email: email.trim().toLowerCase()
      }, {
        withCredentials: true  // Important for session cookies
      });

      if (response.data.success) {
        setEmailSent(true);
        setUserEmail(email.trim().toLowerCase());
        setEmail('');
      } else {
        setError(response.data.error || 'Failed to send login email');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.error || 'Failed to send login email. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResend = () => {
    setEmailSent(false);
    setError('');
    setEmail(userEmail);
  };

  const handleGoogleLogin = () => {
    // Redirect to Google OAuth login endpoint
    window.location.href = '/api/auth/google/login';
  };

  if (emailSent) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-300 via-yellow-400 to-yellow-500 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-2xl p-8 w-full max-w-md">
          <div className="flex items-center justify-center mb-6">
            <CheckCircle className="h-12 w-12 text-green-600" />
          </div>
          <h1 className="text-2xl font-bold text-center text-gray-900 mb-2">
            Check Your Email
          </h1>
          <p className="text-center text-gray-600 mb-6">
            We've sent a login link to
          </p>
          <p className="text-center text-gray-900 font-semibold mb-6">
            {userEmail}
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-800 text-center">
              Click the link in the email to log in. The link will expire in 30 minutes.
            </p>
          </div>
          <button
            onClick={handleResend}
            className="w-full text-blue-600 py-2 text-sm hover:text-blue-700 transition-colors"
          >
            Resend email
          </button>
          <button
            onClick={() => {
              setEmailSent(false);
              setAuthMethod('password');
            }}
            className="w-full text-gray-600 py-2 text-sm hover:text-gray-800 transition-colors mt-2"
          >
            Back to login
          </button>
          <p className="text-xs text-gray-500 text-center mt-6">
            Didn't receive the email? Check your spam folder.
          </p>
        </div>
      </div>
    );
  }

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
            <p>Enter admin password to access admin tools.</p>
          </div>
        )}
        
        {/* Google SSO Button - show first if enabled and not admin login */}
        {googleEnabled && !requireAdmin && (
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
            {(emailEnabled || authMethod !== 'google') && (
              <div className="relative my-6">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">Or continue with</span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Auth Method Toggle - only show if email is enabled and not admin login */}
        {emailEnabled && !requireAdmin && (
          <div className="flex mb-6 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => {
                setAuthMethod('password');
                setError('');
                setPassword('');
                setEmail('');
              }}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                authMethod === 'password'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Password
            </button>
            <button
              onClick={() => {
                setAuthMethod('magic-link');
                setError('');
                setPassword('');
                setEmail('');
              }}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors relative ${
                authMethod === 'magic-link'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Magic Link
              <span className="ml-1.5 inline-flex items-center px-1.5 py-0.5 rounded text-xs font-semibold bg-yellow-100 text-yellow-800 border border-yellow-300">
                BETA
              </span>
            </button>
          </div>
        )}

        {(!emailEnabled || authMethod === 'password') ? (
          <form onSubmit={handlePasswordSubmit}>
            <p className="text-center text-gray-600 mb-6">
              {requireAdmin ? 'Enter admin password' : 'Enter password to access'}
            </p>
            <div className="mb-4">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={requireAdmin ? "Enter admin password" : "Enter password"}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                autoFocus
                disabled={loading}
              />
            </div>
            
            {error && (
              <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
                {error}
              </div>
            )}
            
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {loading ? (
                <>
                  <Loader className="animate-spin h-5 w-5 mr-2" />
                  Logging in...
                </>
              ) : (
                'Login'
              )}
            </button>
          </form>
        ) : (
          <form onSubmit={handleMagicLinkSubmit}>
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-yellow-600" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3 flex-1">
                  <p className="text-sm font-medium text-yellow-800">
                    Beta Feature
                  </p>
                  <p className="mt-1 text-xs text-yellow-700">
                    Magic link authentication is still in beta and needs to be fully implemented. Use password login for production access.
                  </p>
                </div>
              </div>
            </div>
            <p className="text-center text-gray-600 mb-6">
              Enter your @halocollar.com email to receive a login link
            </p>
            <div className="mb-4">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your.name@halocollar.com"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                autoFocus
                disabled={loading}
              />
            </div>
            
            {error && (
              <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
                {error}
              </div>
            )}
            
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {loading ? (
                <>
                  <Loader className="animate-spin h-5 w-5 mr-2" />
                  Sending...
                </>
              ) : (
                'Send Login Link'
              )}
            </button>
          </form>
        )}
        
        {!requireAdmin && (
          <p className="text-xs text-gray-500 text-center mt-6">
            {authMethod === 'password' 
              ? 'Secured with password authentication'
              : authMethod === 'magic-link'
              ? 'Secured with magic link authentication (Beta)'
              : googleEnabled
              ? 'Secured with Google SSO'
              : 'Secured authentication'}
          </p>
        )}
      </div>
    </div>
  );
}

export default Login;

