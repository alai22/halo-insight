# Daily labeling recap in Slack

Every morning the server posts a celebratory recap of yesterday's labeling to a Slack
channel: sessions and minutes per model (activity, indoor/outdoor), shout-outs to the
labelers, the dogs involved, streaks and milestones. Mismatches stay on the dashboard.

## How it runs

1. `.github/workflows/labeling-daily-report.yml` runs at 16:00 UTC (9:00 Pacific in
   summer) and calls `POST /api/labeling/daily-report` with an `X-Report-Secret` header.
2. The server refreshes the all-time summary if it is more than 6 hours old, builds
   yesterday's stats from the summary snapshot, and posts with `chat.postMessage`.
3. The posted day is saved in `labeling-jobs/daily_report_state.json`, so a re-run the
   same day does not post twice. Pass `force: true` to post again.

Labelers are named from the collar owner list (Edit owners on the dashboard) using the
collar they labeled most; otherwise the part of their email before `@`.

## Setup

1. Pick the Slack app to post as and give it the `chat:write` scope. Invite it to the
   channel (`/invite @app-name`).
2. On the server, set `LABELING_REPORT_SLACK_CHANNEL` (channel ID),
   `LABELING_REPORT_SLACK_TOKEN` (or rely on `SLACK_BOT_TOKEN`) and
   `LABELING_REPORT_SECRET` (`openssl rand -hex 32`), then redeploy.
3. In GitHub repo secrets, set `LABELING_REPORT_URL` (the app's base URL) and
   `LABELING_REPORT_SECRET` (same value).
4. Run the workflow by hand once (Actions > Labeling daily report > Run workflow).

## Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `GET` | `/api/labeling/daily-report/preview?date=` | admin | Recap text from data already computed; posts nothing |
| `POST` | `/api/labeling/daily-report` | `X-Report-Secret` or admin session | Post the recap (body: `date`, `force`) |
