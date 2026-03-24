# Architectural Decisions Template

Use this file for architecture or workflow choices that should survive across sessions. Keep ADRs short, explicit, and honest about trade-offs.

## Canonical format

Each ADR should use this shape:

```markdown
### ADR-001: Decision Title (YYYY-MM-DD)
- **Status**: Accepted

**Context:**
- Why the decision was needed
- What problem it solves

**Decision:**
- What was chosen

**Alternatives Considered:**
- Option A -> Why rejected
- Option B -> Why rejected

**Consequences:**
- Benefits
- Trade-offs

- **Related**: `bugs.md` Brief Bug Description, `issues.md` TICKET-ID, `architecture.md` Critical Flows  # optional
```

## Example entries

### ADR-001: Use Workload Identity Federation for GitHub Actions (2025-01-10)
- **Status**: Accepted

**Context:**
- Need secure authentication from GitHub Actions to GCP.
- Want to avoid long-lived service account keys.

**Decision:**
- Use Workload Identity Federation for CI authentication.

**Alternatives Considered:**
- Service account JSON keys -> Rejected: higher leakage and rotation risk.
- Environment-specific static credentials -> Rejected: harder to audit and manage.

**Consequences:**
- ✅ No long-lived credentials in CI.
- ✅ Better audit trail.
- ❌ Slightly more setup complexity.

### ADR-002: Use Alembic for Database Migrations (2025-01-12)
- **Status**: Accepted

**Context:**
- Multiple developers change the schema.
- Manual SQL scripts were becoming difficult to coordinate.

**Decision:**
- Use Alembic for versioned schema migrations.

**Alternatives Considered:**
- Raw SQL scripts -> Rejected: hard to review and sequence.
- Framework-specific migration tools -> Rejected: too coupled to app-framework choices.

**Consequences:**
- ✅ Versioned schema history.
- ✅ Easier rollback and review.
- ❌ Team members must remember to generate and review migrations.
- **Related**: `issues.md` PROJ-125, `architecture.md` Critical Flows

## Tips

- Never reuse ADR numbers.
- If a decision changes, keep the old ADR and set its status to something like `Superseded by ADR-005`.
- Focus on why the choice exists, not a full implementation tutorial.
- If an ADR changes how future sessions should orient themselves, refresh `architecture.md` too.
