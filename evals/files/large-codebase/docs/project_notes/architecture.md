# Architecture Overview

## System Overview
- This monorepo contains a public API, a background worker, and an admin UI.
- Fresh sessions should start here, then read `decisions.md` and `key_facts.md` before exploring service-specific code.

## Component Map
- `services/api` -> public HTTP API, auth, and work enqueueing
- `services/worker` -> async jobs, retries, and downstream sync
- `web/admin` -> operator UI and local auth entry points
- `packages/contracts` -> shared event and queue payload schemas

## Key Entry Points
- API bootstrap: `services/api/src/main.py`
- Auth callbacks: `services/api/src/auth/callbacks.py`
- Worker runner: `services/worker/src/runner.py`
- Admin app entry: `web/admin/src/main.tsx`

## Critical Flows
- Login -> identity provider -> `/auth/callback` -> session bootstrap -> admin UI
- Order submit -> API write -> outbox row -> worker -> downstream ERP sync

## Known Gotchas
- Local login breaks when frontend dev ports are missing from the callback allowlist.
- Retry logic must stay idempotent because the worker redelivers on transient failures.
- Queue payloads live in `packages/contracts`; changing worker payloads without updating contracts causes drift.

## Change Hazards
- Auth, queue contracts, and outbox publishing have cross-service coupling.
- Migration changes affect both API writes and worker replay.

## Related Memory
- `decisions.md` ADR-001
- `decisions.md` ADR-002
- `bugs.md` 2026-02-12 - Local login callback allowlist drift
- `bugs.md` 2026-02-19 - Worker replay duplicated downstream sync
