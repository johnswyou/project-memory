# Architecture Overview Template

Use this file for large, long-lived, or multi-component repositories when a fresh session needs a fast orientation before exploring the full codebase.

## Canonical format

```markdown
# Architecture Overview

## System Overview
- One or two bullets on what the repository contains and where a fresh session should start.

## Component Map
- `path/or/component` -> responsibility
- `another/component` -> responsibility

## Key Entry Points
- API entry: `src/server/main.py`
- Frontend entry: `web/src/main.tsx`
- Worker entry: `jobs/runner.py`

## Critical Flows
- User login -> callback handler -> session bootstrap
- Schema change -> migration generation -> review -> deploy

## Known Gotchas
- Non-obvious constraint or prior misunderstanding
- Cross-link to `bugs.md` or `decisions.md` when helpful

## Change Hazards
- Areas with hidden coupling or rollout risk

## Related Memory
- `decisions.md` ADR-001
- `bugs.md` Brief Bug Description
- `issues.md` TICKET-ID
```

## Example entry

### Example

```markdown
# Architecture Overview

## System Overview
- Monorepo with an API service, a background worker, and an admin UI.
- Fresh sessions should start here, then read `decisions.md` and `key_facts.md`.

## Component Map
- `services/api` -> public HTTP API and request validation
- `services/worker` -> async jobs and retries
- `web/admin` -> operator UI and auth entry points

## Key Entry Points
- API bootstrap: `services/api/src/main.py`
- Worker runner: `services/worker/src/runner.py`
- Admin app: `web/admin/src/main.tsx`

## Critical Flows
- Login -> auth callback -> session bootstrap
- Order submit -> outbox -> worker -> downstream sync

## Known Gotchas
- Local login breaks when callback ports are missing from the allowlist.
- Queue payloads must stay aligned with the shared contracts package.

## Change Hazards
- Auth and callback work spans API config plus frontend local-dev settings.
- Queue contract changes affect both API producers and worker consumers.
```

## Tips

- Keep this file high-signal; it should help a fresh session decide what to inspect next.
- Prefer stable structure over ephemeral sprint notes.
- If a detail becomes stale, mark it deprecated or remove it deliberately.
- Cross-link to `bugs.md`, `decisions.md`, and `issues.md` instead of duplicating too much detail.
