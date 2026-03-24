# Architectural Decisions

### ADR-001: Use Alembic for Database Migrations (2025-01-12)
- **Status**: Accepted

**Context:**
- Multiple developers update the schema.
- The project needs versioned, reviewable migrations.

**Decision:**
- Use Alembic for schema migrations.

**Alternatives Considered:**
- Raw SQL scripts -> Rejected: hard to sequence and review.
- Django migrations -> Rejected: not aligned with the service stack.

**Consequences:**
- ✅ Easier migration review.
- ✅ Better rollback support.
- ❌ Team members must keep migrations in sync with code changes.
