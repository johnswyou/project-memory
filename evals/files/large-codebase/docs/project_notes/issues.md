# Work Log

### 2026-02-21 - OPS-412: Stabilize worker replay idempotency
- **Status**: Completed
- **Description**: Added an idempotency check keyed by outbox event ID before worker retries publish downstream sync requests.
- **URL**: https://jira.example.com/browse/OPS-412
- **Notes**: Replay safety now depends on the outbox event ID being preserved across retries.
- **Related**: `bugs.md` Worker replay duplicated downstream sync, `decisions.md` ADR-001, `architecture.md` Critical Flows

### 2026-03-03 - WEB-88: Allow Vite auth callback port in staging
- **Status**: Completed
- **Description**: Added port 5173 to the staging callback allowlist and documented both supported local admin UI ports.
- **URL**: https://jira.example.com/browse/WEB-88
- **Notes**: Local login must support both port 3000 and port 5173.
- **Related**: `bugs.md` Local login callback allowlist drift, `architecture.md` Known Gotchas
