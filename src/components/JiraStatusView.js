import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { CheckCircle, XCircle, AlertCircle, RefreshCw, ExternalLink, Link2 } from 'lucide-react';

const JiraStatusView = ({ setCurrentMode }) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [status, setStatus] = useState({ configured: false, oauth_can_connect: false, oauth_connected: false });
  const [loading, setLoading] = useState(false);
  const [fetchResult, setFetchResult] = useState(null); // { count, issues, error }
  const [fetching, setFetching] = useState(false);
  const [oauthMessage, setOauthMessage] = useState(null); // { type: 'success' | 'error', text }

  const fetchStatus = () => {
    setLoading(true);
    fetch('/api/jira/status')
      .then((r) => r.json())
      .then((data) => {
        setStatus({
          configured: data.configured ?? false,
          base_url: data.base_url,
          auth_type: data.auth_type,
          oauth_can_connect: data.oauth_can_connect ?? false,
          oauth_connected: data.oauth_connected ?? false,
        });
      })
      .catch(() => setStatus({ configured: false, oauth_can_connect: false, oauth_connected: false }))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  // Read OAuth callback result from URL
  useEffect(() => {
    const connected = searchParams.get('connected');
    const oauthError = searchParams.get('oauth_error');
    if (connected === '1') {
      setOauthMessage({ type: 'success', text: 'Jira connected successfully. You can fetch issues below.' });
      setSearchParams({ mode: 'jira-status' }, { replace: true });
      fetchStatus();
    } else if (oauthError) {
      const messages = {
        missing_code: 'Authorization was cancelled or no code returned.',
        invalid_state: 'Invalid state; please try connecting again.',
        no_callback: 'APP_BASE_URL not set. Set it in .env for OAuth callback.',
        exchange_failed: 'Could not exchange code for tokens. Check client ID/secret and callback URL.',
      };
      setOauthMessage({ type: 'error', text: messages[oauthError] || oauthError });
      setSearchParams({ mode: 'jira-status' }, { replace: true });
    }
  }, [searchParams, setSearchParams]);

  const handleFetch = () => {
    setFetching(true);
    setFetchResult(null);
    fetch('/api/jira/issues?project=HALO&max_results=100')
      .then((res) => res.json().then((data) => ({ status: res.status, data })))
      .then(({ status: code, data }) => {
        if (code !== 200 || data.status !== 'success') {
          setFetchResult({ error: data.message || 'Failed to fetch issues' });
          return;
        }
        const list = Array.isArray(data.data) ? data.data : [];
        setFetchResult({
          count: list.length,
          issues: list.slice(0, 20).map((i) => ({ key: i.key, title: i.title })),
        });
      })
      .catch((err) => setFetchResult({ error: err.message || 'Request failed' }))
      .finally(() => setFetching(false));
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Jira connection</h1>
          <p className="text-gray-600 mt-1">Check if Jira issues can be fetched for Bug Triage (HALO)</p>
        </div>
        <button
          type="button"
          onClick={() => setCurrentMode('tools')}
          className="text-sm text-gray-600 hover:text-gray-900"
        >
          Back to Tools
        </button>
      </div>

      {oauthMessage && (
        <div className={`mb-4 p-3 rounded-lg ${oauthMessage.type === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
          {oauthMessage.type === 'success' ? <CheckCircle className="h-4 w-4 inline mr-2" /> : <XCircle className="h-4 w-4 inline mr-2" />}
          <span className="text-sm">{oauthMessage.text}</span>
        </div>
      )}

      {/* Config status */}
      <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-2">Configuration</h2>
        {loading ? (
          <p className="text-sm text-gray-500">Checking…</p>
        ) : status.configured ? (
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-green-700">
              <CheckCircle className="h-5 w-5 shrink-0" />
              <div>
                <p className="text-sm font-medium">Jira is connected {status.auth_type === 'oauth' ? '(OAuth)' : '(Basic auth)'}</p>
                {status.base_url && (
                  <p className="text-xs text-gray-500 mt-0.5">Base URL: {status.base_url}</p>
                )}
              </div>
            </div>
            {status.oauth_connected && (
              <button
                type="button"
                onClick={() => {
                  fetch('/api/jira/oauth/disconnect', { method: 'POST' })
                    .then(() => fetchStatus());
                }}
                className="text-xs text-gray-500 hover:text-red-600"
              >
                Disconnect OAuth
              </button>
            )}
          </div>
        ) : status.oauth_can_connect ? (
          <div className="space-y-3">
            <p className="text-sm text-gray-600">Connect with OAuth (use the client ID and secret from IT).</p>
            <a
              href="/api/jira/oauth/authorize"
              className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
            >
              <Link2 className="h-4 w-4" />
              Connect to Jira
            </a>
          </div>
        ) : (
          <div className="flex items-start gap-2 text-amber-700">
            <AlertCircle className="h-5 w-5 shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium">Jira is not configured</p>
              <p className="text-xs text-gray-600 mt-1">
                Either set JIRA_CLIENT_ID, JIRA_CLIENT_SECRET, and APP_BASE_URL for OAuth, or set JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN for Basic auth. API token at{' '}
                <a
                  href="https://id.atlassian.com/manage-profile/security/api-tokens"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline inline-flex items-center gap-0.5"
                >
                  id.atlassian.com <ExternalLink className="h-3 w-3" />
                </a>
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Fetch test */}
      <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-2">Test fetch</h2>
        <p className="text-sm text-gray-600 mb-3">
          Fetch up to 100 issues from project HALO to verify the connection.
        </p>
        <button
          type="button"
          onClick={handleFetch}
          disabled={!status.configured || fetching}
          className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RefreshCw className={`h-4 w-4 ${fetching ? 'animate-spin' : ''}`} />
          {fetching ? 'Fetching…' : 'Fetch issues'}
        </button>

        {fetchResult && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            {fetchResult.error ? (
              <div className="flex items-start gap-2 text-red-700">
                <XCircle className="h-5 w-5 shrink-0 mt-0.5" />
                <p className="text-sm">{fetchResult.error}</p>
              </div>
            ) : (
              <>
                <div className="flex items-center gap-2 text-green-700 mb-2">
                  <CheckCircle className="h-5 w-5 shrink-0" />
                  <p className="text-sm font-medium">{fetchResult.count} issues fetched</p>
                </div>
                {fetchResult.issues && fetchResult.issues.length > 0 && (
                  <div className="text-xs text-gray-600">
                    <p className="font-medium text-gray-700 mb-1">Sample (first {fetchResult.issues.length}):</p>
                    <ul className="list-disc list-inside space-y-0.5">
                      {fetchResult.issues.map((i) => (
                        <li key={i.key}>
                          <span className="font-mono">{i.key}</span>
                          {i.title && ` — ${i.title.length > 50 ? i.title.slice(0, 50) + '…' : i.title}`}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>

      {/* Auth options */}
      <div className="bg-gray-50 rounded-lg border border-gray-200 p-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-2">Auth options</h2>
        <p className="text-sm text-gray-600">
          <strong>OAuth 2.0:</strong> Use “Connect to Jira” above (requires JIRA_CLIENT_ID, JIRA_CLIENT_SECRET, APP_BASE_URL, and the callback URL added in Atlassian). One-time browser authorization, then the app uses stored tokens.
          {' '}<strong>Basic auth:</strong> Set JIRA_EMAIL and JIRA_API_TOKEN in .env (create token at id.atlassian.com). No browser step.
        </p>
      </div>
    </div>
  );
};

export default JiraStatusView;
