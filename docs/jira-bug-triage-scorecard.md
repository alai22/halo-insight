# Jira Bug Triage — scorecard mode

The Bug Triage Copilot backlog overview (`POST /api/jira/backlog-overview`) can run in two ways for **priority recommendations**:

1. **Legacy (default)** — Pass 2 asks the model for a markdown `### Recommended Jira priority changes` table directly.
2. **Scorecard (opt-in)** — Pass 2 is a JSON **shortlist** of keys, then a JSON **rubric** per key; the server computes a weighted score, maps it to an implied Jira priority, and emits Raise/Lower rows only when thresholds pass. Optional pass 2b re-scores with **description excerpts** for keys that appear in the recommendation table.

## Where settings are defined

All variables are read from the process environment. The Flask app loads a root `.env` file via `python-dotenv` in [`backend/utils/config.py`](../backend/utils/config.py) (`load_dotenv()` at import time).

Runtime values live on the `Config` class in the same file, for example:

- `Config.JIRA_TRIAGE_SCORECARD_ENABLED`
- `Config.JIRA_TRIAGE_SCORECARD_WEIGHTS_JSON`
- `Config.JIRA_TRIAGE_SCORECARD_THRESHOLDS_JSON`

Implementation references:

- Pipeline: [`backend/api/routes/jira_routes.py`](../backend/api/routes/jira_routes.py) (`_iter_backlog_overview_events`, `use_scorecard`).
- Scoring and markdown generation: [`backend/services/jira_triage_scorecard.py`](../backend/services/jira_triage_scorecard.py).

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `JIRA_TRIAGE_SCORECARD_ENABLED` | `0` (off) | Set to `1`, `true`, or `yes` to use shortlist + scorecard + deterministic merge. |
| `JIRA_TRIAGE_SCORECARD_MAX_KEYS` | `40` | Max keys scored per run (shortlist cap; GA blockers may be prepended when enabled below). |
| `JIRA_TRIAGE_SCORECARD_INCLUDE_GA_BLOCKERS` | `1` (on) | Union issues with `gaBlocker: true` into the scored set (still capped by `MAX_KEYS`). |
| `JIRA_TRIAGE_SCORECARD_MIN_CONFIDENCE` | `2` | Rubric `confidence` (1–5) must be ≥ this to emit a Raise/Lower row. |
| `JIRA_TRIAGE_SCORECARD_MIN_DELTA_RANKS` | `1` | Minimum ladder steps between current Jira priority and implied priority. |
| `JIRA_TRIAGE_SCORECARD_WEIGHTS_JSON` | _(unset)_ | Optional JSON object overriding dimension weights (`severity`, `frequency`, `customer_impact`, `scope`, `release_risk`, `confidence`). |
| `JIRA_TRIAGE_SCORECARD_THRESHOLDS_JSON` | _(unset)_ | Optional JSON `{"breakpoints":[...]}` mapping composite score to implied priority (see module defaults in code). |
| `JIRA_TRIAGE_SCORECARD_SCHEMA_VERSION` | `1` | Label surfaced in API meta for audit trails. |
| `JIRA_TRIAGE_SCORECARD_SHORTLIST_MAX_TOKENS` | `1536` | Max tokens for the shortlist Claude call. |
| `JIRA_BACKLOG_OVERVIEW_TEMPERATURE` | `0` | Applies to **all** backlog-overview Claude calls (including scorecard passes). Keep at `0` for stable runs. |
| `JIRA_BACKLOG_OVERVIEW_DEEP_PASS` | `1` | When enabled, pass 2b runs after recommendations exist (description-enriched **scorecard** JSON when scorecard mode is on). |

`JIRA_TRIAGE_SCORECARD_WEIGHTS_JSON` and `JIRA_TRIAGE_SCORECARD_THRESHOLDS_JSON` are **optional**. If omitted, defaults inside `jira_triage_scorecard.py` apply.

## Should scorecard be on by default?

**Current choice: off by default.**

- **Legacy behavior** stays unchanged for existing deployments.
- **Scorecard mode uses more Claude calls** (shortlist + score, plus optional 2b), so cost and latency change.
- After your team validates outputs, set `JIRA_TRIAGE_SCORECARD_ENABLED=1` in `.env` (or the host environment) for that environment only.

If you want scorecard everywhere, flip the default in `Config` from `'0'` to `'1'` in `config.py` and document the change in release notes.

## API response

When scorecard mode is enabled, the terminal `meta` object includes:

- `scorecard_enabled`, `scorecards_by_key`, `scorecard_config_hash`, `scorecard_schema_version`
- `scorecard_shortlist_size`, `scorecard_scored_keys`, `scorecard_errors`

The UI (`BugTriageCopilot`) shows a **Scorecard triage** panel when `scorecard_enabled` is true.

## Example `.env` snippet

```bash
# Scorecard triage (optional)
JIRA_TRIAGE_SCORECARD_ENABLED=1
# JIRA_TRIAGE_SCORECARD_WEIGHTS_JSON={"severity":1.2,"frequency":1.0,"customer_impact":1.2,"scope":0.8,"release_risk":1.0,"confidence":0.5}
# JIRA_TRIAGE_SCORECARD_THRESHOLDS_JSON={"breakpoints":[{"min_score":88,"priority":"blocker"},{"min_score":72,"priority":"critical"},{"min_score":58,"priority":"major"},{"min_score":44,"priority":"normal"},{"min_score":30,"priority":"minor"},{"min_score":0,"priority":"trivial"}]}
```

## Tests

See [`tests/unit/test_jira_triage_scorecard.py`](../tests/unit/test_jira_triage_scorecard.py) and [`tests/unit/test_jira_priority_validator.py`](../tests/unit/test_jira_priority_validator.py).
