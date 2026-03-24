# Architectural Decisions

### ADR-001: Use Alembic for schema migrations (2026-02-20)
- **Status**: Accepted

**Context:**
- The team needs reviewable, versioned database migrations.
- Raw SQL scripts were causing merge conflicts and drift.

**Decision:**
- Use Alembic for all schema migrations.

**Alternatives Considered:**
- Raw SQL scripts -> Rejected: too easy to lose ordering and rollback intent.
- Framework-specific migration tooling -> Rejected: not shared across services.

**Consequences:**
- ✅ Consistent migration workflow.
- ✅ Easier code review.
- ❌ Developers must remember to generate and check migrations.
- **Related**: `issues.md` API-128, `architecture.md` Critical Flows
