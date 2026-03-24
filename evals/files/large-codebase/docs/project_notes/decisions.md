# Architectural Decisions

### ADR-001: Use transactional outbox for API-to-worker handoff (2026-02-05)
- **Status**: Accepted

**Context:**
- API writes and worker dispatch were drifting apart under transient failures.
- The team needed a reliable handoff that survives retries and restarts.

**Decision:**
- Use a transactional outbox table for API-to-worker handoff.

**Alternatives Considered:**
- Direct publish after commit -> Rejected: too easy to lose events.
- Best-effort background thread publish -> Rejected: not durable enough.

**Consequences:**
- ✅ Worker handoff is durable and replayable.
- ✅ Easier to reason about delivery state.
- ❌ Outbox events must stay idempotent across retries.
- **Related**: `issues.md` OPS-412, `architecture.md` Critical Flows

### ADR-002: Keep queue contracts in packages/contracts (2026-02-11)
- **Status**: Accepted

**Context:**
- API producers and worker consumers were drifting when payload schemas changed independently.
- Shared event names and fields need one source of truth.

**Decision:**
- Keep queue contracts in `packages/contracts` and update both sides together.

**Alternatives Considered:**
- Duplicate schemas in each service -> Rejected: high drift risk.
- Generate contracts at runtime -> Rejected: too much incidental complexity.

**Consequences:**
- ✅ Producers and consumers share reviewed schemas.
- ✅ Changes are visible in one place.
- ❌ Contract changes now require coordinated updates across services.
- **Related**: `architecture.md` Component Map
