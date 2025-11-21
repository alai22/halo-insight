import React, { useState, useEffect } from 'react';
import { Mail, CheckCircle, Loader } from 'lucide-react';
import axios from 'axios';

function Login({ onLogin }) {
  const [authMethod, setAuthMethod] = useState('password'); // 'password' or 'magic-link'
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [emailEnabled, setEmailEnabled] = useState(false);

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

  // Check if we're returning from a magic link
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const authParam = urlParams.get('auth');
    const emailParam = urlParams.get('email');
    
    if (authParam === 'success' && emailParam) {
      // Successfully authenticated via magic link
      setUserEmail(emailParam);
      setEmailSent(false);
      // Clear URL params
      window.history.replaceState({}, document.title, window.location.pathname);
      // Trigger login
      setTimeout(() => {
        onLogin();
      }, 1000);
    }
  }, [onLogin]);

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post('/api/auth/password-login', {
        password: password
      }, {
        withCredentials: true  // Important for session cookies
      });

      if (response.data.success) {
        // Password validated on backend
        // If session is available, it's already created
        // If not, store auth token in localStorage (temporary workaround)
        if (!response.data.session_available && response.data.auth_token) {
          localStorage.setItem('auth_token', response.data.auth_token);
          localStorage.setItem('auth_method', 'password');
          console.log('Stored auth token in localStorage (session unavailable)');
          // Small delay to ensure localStorage is written before checking status
          await new Promise(resolve => setTimeout(resolve, 100));
        }
        // Password validated on backend, session created or token stored
        onLogin();
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
          Halo Insight
        </h1>
        
        <div className="text-sm text-gray-600 text-center mb-6 space-y-2">
          <p>Customer support conversation analysis and churn insights.</p>
          <p>Analyze Gladly conversations, survey responses, and identify trends.</p>
        </div>
        
        {/* Auth Method Toggle - only show if email is enabled */}
        {emailEnabled && (
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
              Enter password to access
            </p>
            <div className="mb-4">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
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
        
        <p className="text-xs text-gray-500 text-center mt-6">
          {authMethod === 'password' 
            ? 'Secured with password authentication'
            : 'Secured with magic link authentication (Beta)'}
        </p>
      </div>
    </div>
  );
}

export default Login;

