Subject: Request: Google OAuth Application Setup for Halo Insight SSO

Hi IT Team,

I'd like to implement Google SSO for our internally developed Halo Insight application (hosted at https://insight.halocollar.com). Could you help create an OAuth 2.0 application in Google Cloud Console?

**What I need:**
- OAuth Client ID and Client Secret

**Configuration:**
- **Application Name:** Halo Insight
- **Authorized redirect URIs:**
  - `https://insight.halocollar.com/api/auth/google/callback`
  - `http://localhost:5000/api/auth/google/callback`
- **OAuth Consent Screen:** Set user type to "Internal" with scopes: `openid`, `email`, `profile`

Thanks!

