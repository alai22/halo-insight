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

## Google Workspace setup (needs a Workspace super admin)

About 15 minutes. You need admin access to admin.google.com, a Google Cloud project, and
SSH access to the EC2 server.

1. **Check the inbox.** `ai_logs_ingest@halocollar.com` must be a real Workspace user
   with Gmail turned on (a licensed user, not an alias or a group). It must be a member of
   `ai_logs@halocollar.com` with delivery set to *Each email*. It already is if Make reads
   it today. Leave Make's connection to it alone.

2. **Create a Cloud project and turn on the Gmail API.** At
   <https://console.cloud.google.com>, pick or create a project (e.g. `halo-labeling-ingest`).
   Then go to *APIs & Services → Library → Gmail API → Enable*.

3. **Create a service account.** Go to *IAM & Admin → Service Accounts → Create service
   account*. Name it `labeling-gmail-ingest`, grant no roles, and finish. Open it and note
   the **Unique ID** (a long number; this is the OAuth client ID). Under *Keys → Add key →
   Create new key → JSON*, download the key file. Treat this file as a password.
   - If key creation is blocked, the org policy `iam.disableServiceAccountKeyCreation` is
     on. A super admin can allow keys for this one project under *IAM & Admin →
     Organization Policies*.

4. **Grant domain-wide delegation, read-only.** At <https://admin.google.com> go to
   *Security → Access and data control → API controls → Manage Domain Wide Delegation → Add
   new*:
   - Client ID: the Unique ID from step 3
   - OAuth scopes: `https://www.googleapis.com/auth/gmail.readonly`

   Authorize. This is the only scope the ingester asks for. It can read mail in the
   mailbox it impersonates, but it cannot send, delete or change anything. Changes can
   take a few minutes to apply, rarely up to 24 hours.

5. **Put the key on the server.** On your laptop:

   ```bash
   base64 < labeling-gmail-ingest-key.json | tr -d '\n'
   ```

   SSH to the EC2 server and add these lines to `~/halo-insight/.env`:

   ```
   LABELING_GMAIL_INGEST_ENABLED=true
   LABELING_GMAIL_INGEST_MODE=shadow
   LABELING_GMAIL_INGEST_MAILBOX=ai_logs_ingest@halocollar.com
   LABELING_GMAIL_SERVICE_ACCOUNT_JSON=<the base64 output>
   ```

   Then delete the downloaded key file. The setting also accepts the raw JSON on one line,
   or a path to the key file inside the container.

6. **Restart:**

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

- `unauthorized_client` / `Client is unauthorized to retrieve access tokens`: step 4 is
  missing, has the wrong client ID, or the scope does not exactly match. It can also mean
  delegation has not applied yet.
- `Precondition check failed` / `failedPrecondition`: the mailbox is not a Gmail-enabled
  user (step 1).
- `Gmail API has not been used in project …`: step 2.

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
| `LABELING_GMAIL_SERVICE_ACCOUNT_JSON` | — | Key: base64, JSON or path |
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
