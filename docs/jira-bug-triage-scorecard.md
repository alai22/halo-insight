# Jira Bug Triage — scorecard mode (v2)

The Bug Triage Copilot backlog overview (`POST /api/jira/backlog-overview`) can run in two ways for **priority recommendations**:

1. **Legacy (default)** — Pass 2 asks the model for a markdown `### Recommended Jira priority changes` table directly.
2. **Scorecard (opt-in)** — A JSON **shortlist** of keys, then a JSON **rubric** (schema **v2**) with five additive dimensions (max **14** points). The server **recomputes** `raw_total`, **GA verdict**, and **implied Jira priority** from fixed rules, then emits Raise/Lower rows when `JIRA_TRIAGE_SCORECARD_MIN_DELTA_RANKS` is satisfied. Optional **pass2b** re-scores with **description excerpts** for keys that appeared in the recommendation table.

**GA verdict** (Block GA / Fix if capacity / PostGA) follows **raw total only**. **Jira priority** can still be **Blocker** under a **safety override** (feature importance 4 plus engineering signals) even when the total is low—so PostGA and Blocker can both appear for the same ticket. That matches the product rubric.

## Rubric summary (implemented in code + system prompt)

| Dimension | Range |
|-----------|--------|
| `feature_importance` | 0–4 |
| `reach` | 0–3 |
| `technical_severity` | 0–3 |
| `workaround_quality` | 0–2 |
| `regression_risk` | 0–2 |

**GA verdict from total:** ≥10 → Block GA; 6–9 → Fix if capacity; ≤5 → PostGA.

**Implied Jira priority (server order):** Blocker if total ≥10 **or** (feature_importance == 4 **and** (technical_severity ≥2 **or** workaround_quality ≥1)); else Critical 8–9; Major 6–7; Normal 4–5; Minor ≤3.

Full wording for the model lives in `_SCORECARD_RUBRIC_INSTRUCTIONS` in [`backend/api/routes/jira_routes.py`](../backend/api/routes/jira_routes.py).

## Where settings are defined

Environment variables are read via `python-dotenv` in [`backend/utils/config.py`](../backend/utils/config.py).

Implementation:

- Pipeline: [`backend/api/routes/jira_routes.py`](../backend/api/routes/jira_routes.py) (`_iter_backlog_overview_events`, `use_scorecard`).
- Parsing and deterministic rules: [`backend/services/jira_triage_scorecard.py`](../backend/services/jira_triage_scorecard.py).

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `JIRA_TRIAGE_SCORECARD_ENABLED` | `0` (off) | Set to `1`, `true`, or `yes` for shortlist + JSON scorecard v2 + deterministic merge. |
| `JIRA_TRIAGE_SCORECARD_MAX_KEYS` | `40` | Max keys scored per run (shortlist cap; GA blockers may be prepended when enabled below). |
| `JIRA_TRIAGE_SCORECARD_INCLUDE_GA_BLOCKERS` | `1` (on) | Union issues with `gaBlocker: true` into the scored set (still capped by `MAX_KEYS`). |
| `JIRA_TRIAGE_SCORECARD_MIN_DELTA_RANKS` | `1` | Minimum ladder steps between current Jira priority and **server** implied priority to emit Raise/Lower. |
| `JIRA_TRIAGE_SCORECARD_SCHEMA_VERSION` | `2` | Label in API meta (must match parser; model must emit `"version":"2"`). |
| `JIRA_TRIAGE_SCORECARD_SHORTLIST_MAX_TOKENS` | `1536` | Max tokens for the shortlist Claude call. |
| `JIRA_BACKLOG_OVERVIEW_TEMPERATURE` | `0` | Applies to all backlog-overview Claude calls. |
| `JIRA_BACKLOG_OVERVIEW_DEEP_PASS` | `1` | Enables pass2b description-enriched scorecard when recommendations exist. |

### Legacy (v1 only — ignored for scorecard v2)

These are kept in `Config` for backwards compatibility but **do not affect** scoring when using schema v2:

- `JIRA_TRIAGE_SCORECARD_MIN_CONFIDENCE`
- `JIRA_TRIAGE_SCORECARD_WEIGHTS_JSON`
- `JIRA_TRIAGE_SCORECARD_THRESHOLDS_JSON`

## API response

When scorecard mode is enabled, terminal `meta` includes:

- `scorecard_enabled`, `scorecards_by_key`, `scorecard_config_hash` (stable hash for framework v2), `scorecard_schema_version`
- `scorecard_shortlist_size`, `scorecard_scored_keys`, `scorecard_errors` (parse issues + optional LLM vs server mismatch hints)

Each `scorecards_by_key[key]` entry includes the five scores, `raw_total`, `ga_verdict`, `implied_priority`, optional `llm_*` echoes, and `recommendation` when Raise/Lower passes the rank-delta gate.

The UI (`BugTriageCopilot`) shows a **Scorecard triage** panel when `scorecard_enabled` is true.

## Example `.env` snippet

```bash
# Scorecard triage (optional) — v2 14-point rubric
JIRA_TRIAGE_SCORECARD_ENABLED=1
JIRA_TRIAGE_SCORECARD_MAX_KEYS=40
JIRA_TRIAGE_SCORECARD_MIN_DELTA_RANKS=1
# JIRA_TRIAGE_SCORECARD_SHORTLIST_MAX_TOKENS=1536
```

## Tests

See [`tests/unit/test_jira_triage_scorecard.py`](../tests/unit/test_jira_triage_scorecard.py) and [`tests/unit/test_jira_priority_validator.py`](../tests/unit/test_jira_priority_validator.py).
