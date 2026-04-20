# Claude Model Compatibility Guide

## Overview

This document tracks which Claude models are available and working with our API configuration. Models may become deprecated or unavailable, so we maintain a fallback system.

**Key recommendation**: Use **non-dated model aliases** (for example `claude-haiku-4-5`, `claude-sonnet-4`) so Anthropic can route to the latest snapshot automatically.

## Recommended models (2026)

### Primary (app default): Haiku 4.5

- **Model**: `claude-haiku-4-5` (non-dated alias)
- **Why**: Successor to retired Claude Haiku 3 (`claude-3-haiku-20240307`, retired April 2026). Fast and cost-effective for backlog and triage workloads.

### Alternative: Sonnet 4

- **Model**: `claude-sonnet-4` (non-dated alias)
- **Why**: Strong choice for heavier RAG and analysis when quality matters more than minimum cost.

### Quick reference

| Model Name | Type | Notes |
|-----------|------|--------|
| `claude-haiku-4-5` | Non-dated alias | Default in code; speed/cost |
| `claude-haiku-4-5-20251001` | Dated snapshot | Explicit Haiku 4.5 snapshot |
| `claude-sonnet-4` | Non-dated alias | Recommended for demanding RAG |
| `claude-opus-4` | Non-dated alias | Highest capability, higher cost |

## Retired / do not use

| Model Name | Notes |
|-----------|--------|
| `claude-3-haiku-20240307` | Retired April 2026 — use `claude-haiku-4-5` |
| `claude-3-5-haiku-20241022` | Retired — use `claude-haiku-4-5` |
| `claude-3-opus-20240229` | Retired — use `claude-opus-4` |

The backend maps legacy model IDs to current aliases where possible (`backend/utils/config.py` → `MODEL_ALIASES`).

## API version

- **2023-06-01**: Use with the Messages API for current Claude 4.x models.

## Best practices

1. Prefer non-dated aliases for Haiku and Sonnet unless you must pin a snapshot.
2. Before deploys, spot-check your key against the [Anthropic model deprecations](https://docs.claude.com/en/docs/resources/model-deprecations) page.
3. Set `CLAUDE_MODEL` in `.env` on the server if you want to override the application default.

## Testing model availability

Run on the server (adjust container name if needed):

```bash
docker exec gladly-prod python3 -c "
import requests, os
key = os.getenv('ANTHROPIC_API_KEY')
h = {'x-api-key': key, 'Content-Type': 'application/json', 'anthropic-version': '2023-06-01'}
for m in ['claude-haiku-4-5', 'claude-sonnet-4', 'claude-opus-4']:
    r = requests.post('https://api.anthropic.com/v1/messages', headers=h, json={'model': m, 'max_tokens': 10, 'messages': [{'role': 'user', 'content': 'hi'}]}, timeout=10)
    print(f'{m}: {\"OK\" if r.status_code == 200 else r.status_code}')
"
```

## Last updated

- **Date**: April 2026
- **Application default**: `claude-haiku-4-5` (see `backend/utils/config.py`)
