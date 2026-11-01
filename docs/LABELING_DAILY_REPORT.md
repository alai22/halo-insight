# Daily labeling recap in Slack

Every morning the server posts a celebratory recap of yesterday's labeling to a Slack
channel: sessions and minutes per model (activity, indoor/outdoor), shout-outs to the
labelers, the dogs involved, streaks and milestones. Mismatches stay on the dashboard.

## How it runs

1. `.github/workflows/labeling-daily-report.yml` runs at 16:00 UTC (9:00 Pacific in
   summer, 8:00 in winter) and calls `POST /api/labeling/daily-report` with an
   `X-Report-Secret` header.
2. The server refreshes the all-time summary if it is more than 6 hours old, builds
   yesterday's stats from the summary snapshot, and posts to Slack.
3. The posted day is saved in `labeling-jobs/daily_report_state.json`, so a re-run the
   same day does not post twice. Pass `force: true` to post again.

Labelers are named from the collar owner list (Edit owners on the dashboard) using the
collar they labeled most; otherwise the part of their email before `@`.

## Setup

About 15 minutes. You need: admin access to the Slack app, SSH access to the EC2
server, and admin access to the GitHub repo.

### 1. Slack: get an incoming webhook URL

Any Slack app you manage works, such as the one made for Make. A dedicated app from IT
can replace it later (see "Switching apps" below). The webhook can only post to the one
channel you pick, so the server never holds a token with the app's other permissions.

1. Open <https://api.slack.com/apps> and click the app.
2. In the left sidebar, under **Features**, click **Incoming Webhooks**.
3. Turn on **Activate Incoming Webhooks**.
4. At the bottom, click **Add New Webhook to Workspace**, choose the channel for the
   recap (for example `#labeling`), and click **Allow**.
   - If your workspace requires approval for app changes, this becomes a request to a
     Slack admin. Continue once it is approved.
5. Copy the new **Webhook URL** (`https://hooks.slack.com/services/T…/B…/…`). Treat it
   like a password: anyone with it can post to that channel.
6. Optional check from your laptop:

   ```bash
   curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello from the labeling dashboard 👋"}' 'PASTE_WEBHOOK_URL'
   ```

   The message appears in the channel under the app's name and icon.

Adding a webhook doesn't change the app's bot token, but Slack reinstalls the app to add
the webhook. Check that your Make scenarios still run once afterwards.

### 2. Server: add the settings

1. Make a shared secret for the scheduled job (keep the output for step 3):

   ```bash
   openssl rand -hex 32
   ```

2. SSH to the EC2 server and open `~/halo-insight/.env`. Add:

   ```
   LABELING_REPORT_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
   LABELING_REPORT_SECRET=the-output-of-openssl
   ```

   Also make sure `APP_BASE_URL` is set to the dashboard's address (for example
   `https://insight.example.com`) so the recap links to it. `LABELING_REPORT_TIMEZONE`
   defaults to `America/Los_Angeles`.

3. Restart with the new settings:

   ```bash
   cd ~/halo-insight && ./deploy.sh production
   ```

4. On the dashboard, click **Slack recap**. The panel should show yesterday's preview
   and no "Slack is not set up yet" note. Click **Send to Slack now** to post one.

### 3. GitHub: schedule it

1. In the repo on GitHub, go to **Settings → Secrets and variables → Actions → New
   repository secret** and add:
   - `LABELING_REPORT_URL`: the dashboard's base URL, the same as `APP_BASE_URL`
   - `LABELING_REPORT_SECRET`: the same value as on the server
2. Go to **Actions → Labeling daily report → Run workflow** and run it once. Leave the
   date empty for yesterday. If yesterday was already posted from the dashboard, tick
   "Post again".
3. A green run means the server accepted it; the post follows within a minute or two.
   If nothing shows in Slack, open **Slack recap** on the dashboard: it shows the last
   error.

From then on it posts every morning by itself.

## Switching apps

When IT sets up a dedicated Slack app, repeat step 1 with that app, replace
`LABELING_REPORT_SLACK_WEBHOOK_URL` in `.env`, and redeploy. Then remove the old webhook
from the Make app (**Incoming Webhooks**, click **Remove** next to it) so the old URL stops
working.

A bot token works too: set `LABELING_REPORT_SLACK_CHANNEL` (channel ID) and
`LABELING_REPORT_SLACK_TOKEN` (an `xoxb-` token with `chat:write`, with the bot invited to
the channel) and leave the webhook URL empty.

## Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `GET` | `/api/labeling/daily-report/preview?date=&days=` | admin | Recap text from data already computed; posts nothing |
| `POST` | `/api/labeling/daily-report` | `X-Report-Secret` or admin session | Post the recap (body: `date`, `days`, `force`, `refresh`) |
| `GET` | `/api/labeling/daily-report/status` | admin | The send in progress (stage) and the last result |

`days` is 1 by default; 7 covers the week ending on `date`. The dashboard's **Slack recap**
panel has a **Day / Last 7 days** switch for manual sends. A weekly post does not count as
that day's daily post, so the scheduled run still posts the next morning.
