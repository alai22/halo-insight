Subject: Halo Insight access for @softeq.com — Google OAuth vs magic link

Hi [IT / Security team name],

We’d like `@softeq.com` users to sign in to **Halo Insight** (`https://insight.halocollar.com`) without opening the app to arbitrary domains.

## Why they’re blocked today

Our Google OAuth client uses an **Internal** consent screen. Google then returns **403 org_internal** for anyone outside our Cloud org—**before** our app runs. The app separately **allowlists email domains** (e.g. `halocollar.com` and `softeq.com`); that only applies *after* Google completes sign-in. We need your call on how to unblock Softeq at Google’s layer.

---

## Option A — **External** OAuth + app domain allowlist

Move the consent screen to **External** so `@softeq.com` Google accounts can finish OAuth. We keep **server-side domain allowlisting** only (`halocollar.com`, `softeq.com`); everyone else gets no session.

**Pros:** One “Sign in with Google” path; Google-backed identity (MFA/Workspace where Softeq uses it); no new auth system.

**Cons:** Possible **Google verification** for External apps; more accounts can *start* OAuth (mitigated by strict allowlist + treating misconfig as a security issue); confirm this fits our policy.

---

## Option B — **Magic link** for Softeq

Keep OAuth **Internal** for Halocollar. Softeq uses **email magic link** (already in our app): allowed domains + SMTP to `@softeq.com`.

**Pros:** No GCP consent change.

**Cons:** Second login UX to document/support; email deliverability and link/phishing considerations vs Workspace SSO.

---

## Ask

We’d default to **Option A** if you’re comfortable with **External** + allowlist. If OAuth must stay **Internal**, we’ll lean on **Option B** for Softeq.

Please confirm: (1) OK to set Halo Insight OAuth to **External** (and any verification steps you want), and (2) whether **magic link** should stay as a backup or stay off for simplicity.

Thanks,  
[Your name]
