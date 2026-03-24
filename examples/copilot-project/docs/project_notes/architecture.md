# Architecture Overview

## System Overview
- This repository centers on a Python API service plus a small operator UI.
- Fresh sessions should start here, then read `decisions.md` for migration constraints and `key_facts.md` for environment facts.

## Component Map
- `app/api/` -> HTTP endpoints and request validation
- `app/auth/` -> login flow, callback handling, and local session bootstrap
- `migrations/` -> Alembic migration history
- `web/` -> operator UI and local auth entry points

## Key Entry Points
- API app entry: `app/main.py`
- Auth callback handling: `app/auth/callbacks.py`
- Alembic config: `alembic.ini`
- Frontend bootstraps on ports `3000` and `5173` in local dev

## Critical Flows
- Browser login -> identity provider -> callback handler -> local session bootstrap
- Schema change -> Alembic migration -> deploy

## Known Gotchas
- Local login fails when callback URLs for ports `3000` or `5173` are not allowlisted in staging OAuth config.
- Migration tooling should stay on Alembic unless an ADR explicitly supersedes it.

## Change Hazards
- Auth callback changes often require config updates in both the identity provider and local dev docs.
- Database schema changes must update migrations and rollout notes together.

## Related Memory
- `decisions.md` ADR-001
- `bugs.md` 2026-03-01 - Staging API returned 401 in local development
- `issues.md` API-142
