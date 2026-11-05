# Labeling Gmail ingester (replacing Make.com)

Labelers email collar log zips to the `ai_logs@halocollar.com` Google Group. The group
delivers each email to the `ai_logs_ingest@halocollar.com` inbox. Today Make.com reads that
inbox and uploads to S3 `halo-ai-labeling-prod/staging/`. When Make ran out of credits
(Nov 1–2, 2026) it dropped emails without any warning.

The dashboard server can now read that inbox itself through the Gmail API. It writes the
same layout Process staging already reads:

```
staging/<labeler email>/<gmail message id>/_meta.json
                                          raw/<attachment>.zip
                                          extracted/<activity|gps>_session_*.txt
staging/_forwards/<gmail message id>/...   # sender unclear, or forwarded by someone else
```

Folders are always named by the labeler's email address, never by display name. Mail that
came through the group shows From as "X via …" or as the group address. For that mail the
real sender is taken from `X-Original-Sender`, then `Reply-To`, then `X-Original-From`.
When none of those names a person, or someone forwarded another labeler's email, the
batch goes to `_forwards/`. The existing forward promotion then credits it to the labeler.

Code: `backend/services/labeling_gmail_ingest_service.py`. CLI: `ingest_labeling_gmail.py`.
One-time sign-in: `authorize_labeling_gmail.py`.

## Running beside Make

Make keeps running unchanged until you turn it off. The ingester has two modes:

| `LABELING_GMAIL_INGEST_MODE` | Writes to | Effect on the dashboard |
|---|---|---|
| `shadow` (default) | `staging-gmail/` | None. Process staging never reads it. Data health compares it with Make, email by email. |
| `live` | `staging/` | New emails reach the charts after Process staging. It skips every email Make already delivered, in any folder, so both can run at once. Make's `_meta.json`-only batches (emails it dropped) get filled in. |

Suggested cutover:

1. Finish the setup below with `LABELING_GMAIL_INGEST_MODE=shadow` and deploy.
2. Let it run for a few days. On **Data health → Gmail ingest**, the comparison should
   say *they agree*. "Only Make" should list only Make batches that had no logs. "Only
   Gmail" lists emails Make missed, such as the Nov 1 gap. "Other folder" lists emails Make
   filed under a display name or the group address.
3. Switch to `LABELING_GMAIL_INGEST_MODE=live` and redeploy. To recover the emails Make
   missed, use **Backfill from date**, e.g. `2026-11-01`, then Process staging.
4. Turn the Make scenario off once live has run cleanly for a while. Nothing in this repo
   changes when you do.

## Google setup

The ingester needs read-only Gmail access to the inbox. There are two ways to grant it.
Use **A** unless IT allows domain-wide delegation.

| | A. OAuth for the inbox (recommended) | B. Service account, domain-wide delegation |
|---|---|---|
| Who grants it | The inbox itself, once, in a browser | A Workspace super admin |
| What it can reach | Only `ai_logs_ingest@halocollar.com` | Any user Google lets it impersonate; the code limits it to the inbox |
| Secret on the server | Client ID, client secret, refresh token | Service account key |
| Breaks when | The inbox's password changes, or access is revoked | The key is deleted or delegation is removed |

Either way the scope is `https://www.googleapis.com/auth/gmail.readonly`: it can read
mail but cannot send, delete or change anything.

First, **check the inbox.** `ai_logs_ingest@halocollar.com` must be a Workspace user with
Gmail turned on, and a member of `ai_logs@halocollar.com` with delivery set to *Each
email*. It already is if Make reads it today. Leave Make's connection to it alone.

### A. OAuth for the inbox

About 10 minutes. Needs a Google Cloud project in the halocollar.com organization (create
it with your work account, not the inbox; add a second owner), and the inbox's password.

1. **Turn on the Gmail API.** At <https://console.cloud.google.com>, in the project, go to
   *APIs & Services → Library → Gmail API → Enable*.
2. **Consent screen.** *Google Auth Platform* (or *APIs & Services → OAuth consent
   screen*): app name `Halo labeling ingest`, support email yours, audience **Internal**.
   Internal keeps it to halocollar.com accounts, needs no Google review, and its tokens do
   not expire after 7 days. Under *Data access*, add the scope
   `https://www.googleapis.com/auth/gmail.readonly`.
3. **OAuth client.** *Clients → Create client*, type **Desktop app**, name
   `labeling-gmail-ingest`. Download the JSON (`client_secret_….json`). Treat it as a
   secret.
4. **Sign in as the inbox, once.** On your laptop, from this repo:

   ```bash
   pip install google-auth-oauthlib google-api-python-client
   python authorize_labeling_gmail.py ~/Downloads/client_secret_XXXX.json
   ```

   A browser opens. Sign in as `ai_logs_ingest@halocollar.com` (a private window avoids
   picking your own account) and approve. The script checks it got that inbox and prints
   three lines.
5. **Put them on the server.** SSH to the EC2 server and add to `~/halo-insight/.env`:

   ```
   LABELING_GMAIL_INGEST_ENABLED=true
   LABELING_GMAIL_INGEST_MODE=shadow
   LABELING_GMAIL_INGEST_MAILBOX=ai_logs_ingest@halocollar.com
   LABELING_GMAIL_OAUTH_CLIENT_ID=<from the script>
   LABELING_GMAIL_OAUTH_CLIENT_SECRET=<from the script>
   LABELING_GMAIL_OAUTH_REFRESH_TOKEN=<from the script>
   ```

   Then delete the downloaded client JSON.
6. **Restart** (see *Restart* below).

If IT restricts third-party apps, they mark this one OAuth client as *Trusted* under
admin.google.com *Security → API controls → App access control*. That trusts one app; it
is not domain-wide delegation.

To revoke: sign in as the inbox at <https://myaccount.google.com/permissions> and remove
*Halo labeling ingest*, or IT removes it in App access control. If the inbox's password
changes, Google revokes the token: run step 4 again and replace the refresh token.

### B. Service account with domain-wide delegation

Needs a Workspace super admin.

1. In the Cloud project, turn on the Gmail API (A1).
2. **Create a service account.** *IAM & Admin → Service Accounts → Create service
   account*. Name it `labeling-gmail-ingest`, grant no roles, and finish. Open it and note
   the **Unique ID** (a long number; this is the OAuth client ID). Under *Keys → Add key →
   Create new key → JSON*, download the key file. Treat this file as a password.
   - If key creation is blocked, the org policy `iam.disableServiceAccountKeyCreation` is
     on. A super admin can allow keys for this one project under *IAM & Admin →
     Organization Policies*.
3. **Grant domain-wide delegation.** At <https://admin.google.com> go to *Security → Access
   and data control → API controls → Manage Domain Wide Delegation → Add new*: Client ID
   the Unique ID, OAuth scopes `https://www.googleapis.com/auth/gmail.readonly`.
   Authorize. Changes can take a few minutes to apply, rarely up to 24 hours.
4. **Put the key on the server.** `base64 < labeling-gmail-ingest-key.json | tr -d '\n'`,
   then in `~/halo-insight/.env` set the same lines as A5 but with
   `LABELING_GMAIL_SERVICE_ACCOUNT_JSON=<the base64 output>` instead of the three OAuth
   lines. Delete the key file. The setting also accepts the raw JSON on one line, or a path.

If both are set, the OAuth lines win.

### Restart

```bash
cd ~/halo-insight && ./deploy.sh production
```

The first check runs 30 seconds after start, then every 5 minutes. The first run reads
the last 3 days (`LABELING_GMAIL_INITIAL_LOOKBACK_DAYS`). Data health shows the result.
To test from a laptop with the same `.env`:

```bash
python ingest_labeling_gmail.py --since 2026-11-01 --dry-run
```

### If it fails

- `invalid_grant` / `Token has been expired or revoked` (A): the inbox's password changed
  or access was revoked. Run `authorize_labeling_gmail.py` again.
- `The Gmail refresh token is for …, not …` (A): someone approved as the wrong account.
  Run the script again signed in as the inbox.
- `access_denied` / `admin_policy_enforced` in the browser (A): IT has to trust the OAuth
  client in App access control, or the consent screen is not Internal.
- `unauthorized_client` / `Client is unauthorized to retrieve access tokens` (B): step B3
  is missing, has the wrong client ID, or the scope does not exactly match. It can also
  mean delegation has not applied yet.
- `Precondition check failed` / `failedPrecondition`: the mailbox is not a Gmail-enabled
  user.
- `Gmail API has not been used in project …`: step A1.

## How it avoids duplicates and gaps

- **Cursor:** `labeling-jobs/gmail_ingest_state_<mode>.json` in the labeling bucket. It
  holds the newest email time seen and the message ids already handled. Each run reads
  from one day before the cursor and skips handled ids, so a deploy restart resumes where
  the last run stopped.
- **Re-runs and backfills are safe.** An email is skipped when its id is in the cursor,
  or when its batch is already in staging. For the ingester's own batches that means
  `_meta.json` with `ingest_complete: true`. For Make's batches it means any extracted
  file. A batch cut off by a restart is written again. Process staging also de-duplicates
  sessions across emails.
- **Failures:** an email that fails is retried by id on every run. After 5 failures it is
  left alone and listed under Data health errors.
- **No overlap:** runs never overlap each other. In live mode a poll skips while Process
  staging, compact or promote is running. Those jobs refuse to start (409) while a live run
  is writing to staging.
- Emails with no session logs (no zip, or a zip without `*_session_*.txt`) write nothing.
  They are counted as *no logs*.

## Settings

| Setting | Default | |
|---|---|---|
| `LABELING_GMAIL_INGEST_ENABLED` | `false` | Starts the background poll |
| `LABELING_GMAIL_INGEST_MAILBOX` | `ai_logs_ingest@halocollar.com` | Inbox to impersonate |
| `LABELING_GMAIL_INGEST_MODE` | `shadow` | `shadow` or `live` |
| `LABELING_GMAIL_SHADOW_PREFIX` | `staging-gmail/` | Shadow output |
| `LABELING_GMAIL_OAUTH_CLIENT_ID` | — | OAuth access (A) |
| `LABELING_GMAIL_OAUTH_CLIENT_SECRET` | — | OAuth access (A) |
| `LABELING_GMAIL_OAUTH_REFRESH_TOKEN` | — | OAuth access (A); takes precedence over B |
| `LABELING_GMAIL_SERVICE_ACCOUNT_JSON` | — | Service account key (B): base64, JSON or path |
| `LABELING_GMAIL_INGEST_POLL_SEC` | `300` | Seconds between checks (minimum 60) |
| `LABELING_GMAIL_INGEST_QUERY` | `has:attachment` | Extra Gmail search terms |
| `LABELING_GMAIL_INITIAL_LOOKBACK_DAYS` | `3` | First run with no cursor |
| `LABELING_GROUP_SENDERS` | `ai_logs@halocollar.com` | Never treated as a labeler |

## Admin endpoints

- `POST /api/labeling/gmail-ingest/run` with `{}`: check now. With
  `{"since": "2026-11-01", "until": "2026-11-03", "dry_run": false}`: backfill.
- `POST /api/labeling/gmail-ingest/compare` `{"since"?: "YYYY-MM-DD"}`: Gmail shadow
  compared with Make.
- `GET /api/labeling/status` → `gmail_ingest`: last run, totals, recent errors, retrying
  count, `stalled`, and the latest comparison.
