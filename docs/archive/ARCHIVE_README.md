# Archived Files

This directory contains legacy files that have been superseded by the current implementation but are kept for historical reference.

## Files in this Archive

### `app_original.py`
**Status**: Superseded  
**Date Archived**: November 2025  
**Reason**: Original monolithic Flask application (500+ lines) before refactoring

**What it was**: The original monolithic Flask backend that contained all routes, business logic, and initialization code in a single file.

**Why archived**: Replaced by the modular architecture in `app.py` which uses:
- Service layer architecture (`backend/services/`)
- Blueprint-based routing (`backend/api/routes/`)
- Dependency injection via service container
- Proper middleware and error handling

**Key differences from current `app.py`**:
- Used direct imports: `claude_api_client`, `public_s3_analyzer`
- All logic inline in routes
- No service abstraction
- No dependency injection
- Basic error handling

**Note**: The modules `claude_api_client.py` and `public_s3_analyzer.py` still exist in the root directory as they are standalone CLI tools, not backend dependencies.

---

### `app_new.py`
**Status**: Superseded  
**Date Archived**: November 2025  
**Reason**: Intermediate refactoring version, missing production features

**What it was**: An intermediate version during the refactoring process that introduced the modular blueprint structure but was incomplete.

**Why archived**: Missing critical production features that are present in current `app.py`:
- Download routes (`download_bp`)
- Survicate routes (`survicate_bp`)
- Auth routes (`auth_bp`)
- Service container pattern
- Request logging middleware
- Session management
- Werkzeug header size configuration

**Key differences from current `app.py`**:
- Only 4 blueprints vs 7 in production
- No service container (dependency injection)
- No request logging
- No session management
- Simpler error handling

---

## Current Production Entry Point

The current production application uses:
- **`app.py`** - Main Flask application with full feature set
- **`serve.py`** - Production server wrapper (used by Docker)

Both files import from `app.py`, ensuring a single source of truth.

---

## Migration Notes

If you need to reference these files:
1. Check `REFACTORING_SUMMARY.md` for the refactoring history
2. See `ARCHITECTURE_IMPROVEMENTS.md` for architectural decisions
3. Current implementation is in `app.py` and `backend/` directory

---

**Last Updated**: November 2025

