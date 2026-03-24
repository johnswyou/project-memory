# Issues / Work Log Template

Use this file for a lightweight, dated work log. This is not a replacement for Jira or GitHub Issues; it is a quick shared memory aid.

## Canonical format

Use one entry per dated task or ticket:

```markdown
### YYYY-MM-DD - TICKET-ID: Brief Description
- **Status**: Completed / In Progress / Blocked
- **Description**: One or two lines of context
- **URL**: https://tracker.example.com/TICKET-ID
- **Notes**: Important follow-up or scope notes
- **Related**: `bugs.md` Brief Bug Description, `decisions.md` ADR-001, `architecture.md` Key Entry Points  # optional
```

## Example entries

### 2025-01-15 - PROJ-123: Implement Contact API
- **Status**: Completed
- **Description**: Added CRUD endpoints with request validation and unit tests.
- **URL**: https://jira.company.com/browse/PROJ-123
- **Notes**: Coverage reached 85 percent for the new endpoints.

### 2025-01-16 - PROJ-124: Fix Docker Build Issues
- **Status**: Completed
- **Description**: Fixed the image-platform mismatch for Cloud Run deployments.
- **URL**: https://jira.company.com/browse/PROJ-124
- **Notes**: The build scripts now pin the deployment platform.
- **Related**: `bugs.md` Docker Architecture Mismatch, `architecture.md` Change Hazards

### 2025-01-22 - GH-45: Add OAuth2 Authentication
- **Status**: In Progress
- **Description**: Backend OAuth flow is complete and frontend integration is in progress.
- **URL**: https://github.com/company/repo/issues/45
- **Notes**: Waiting on final callback URL review.
- **Related**: `architecture.md` Critical Flows

## Tips

- Keep one entry per task instead of switching to weekly grouped summaries.
- Use the tracker URL as the source of full detail.
- If an item becomes stale, update the status instead of rewriting history.
- Promote durable lessons out of `issues.md` into `bugs.md`, `decisions.md`, or `architecture.md` when they will matter across sessions.
