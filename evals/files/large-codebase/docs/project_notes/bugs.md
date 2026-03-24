# Project Bug Log

### 2026-02-12 - Local login callback allowlist drift
- **Issue**: Engineers could authenticate in staging from production hosts but not from local admin UI sessions.
- **Root Cause**: The identity provider allowlist included port 3000 but not the alternate Vite dev port 5173.
- **Solution**: Added both local callback ports to the staging OAuth application settings.
- **Prevention**: Treat frontend dev ports as a tracked key fact and review the allowlist when local tooling changes.
- **Related**: `issues.md` WEB-88, `key_facts.md` Identity, `architecture.md` Known Gotchas

### 2026-02-19 - Worker replay duplicated downstream sync
- **Issue**: A transient downstream timeout caused the worker to resend the same ERP sync more than once.
- **Root Cause**: The retry path was not checking the idempotency key before publishing the downstream request.
- **Solution**: Added an idempotency check keyed by the outbox event ID before each retry.
- **Prevention**: Keep worker retries idempotent and verify the outbox event ID is present in every replay path.
- **Related**: `issues.md` OPS-412, `decisions.md` ADR-001, `architecture.md` Change Hazards
