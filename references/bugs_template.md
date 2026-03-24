# Bug Log Template

Use this file for recurring or instructive bugs that the project is likely to hit again. Keep entries brief, dated, and easy to scan.

## Canonical format

Each entry should use this shape:

```markdown
### YYYY-MM-DD - Brief Bug Description
- **Issue**: What went wrong
- **Root Cause**: Why it happened
- **Solution**: What fixed it
- **Prevention**: How to avoid it next time
- **Related**: `issues.md` TICKET-ID, `decisions.md` ADR-001, `architecture.md` Known Gotchas  # optional
```

## Example entries

### 2025-01-15 - Docker Architecture Mismatch
- **Issue**: Container failed to start with `exec format error` in production.
- **Root Cause**: The image was built on ARM64 but deployed to an AMD64 runtime.
- **Solution**: Added `--platform linux/amd64` to the build command.
- **Prevention**: Pin the deployment platform in build scripts and release docs.
- **Related**: `issues.md` PROJ-124

### 2025-01-22 - Database Connection Pool Exhaustion
- **Issue**: The API returned 500s under sustained load.
- **Root Cause**: The default connection pool was too small for peak traffic.
- **Solution**: Increased the pool size and max overflow in the database config.
- **Prevention**: Run a quick load test before production releases that change query behavior.
- **Related**: `decisions.md` ADR-003, `architecture.md` Change Hazards

## Tips

- Favor bugs that teach the project something durable.
- Keep the description short; the important part is the lesson, not a full incident report.
- If a bug teaches a repo-level sharp edge that fresh sessions should see early, mirror a concise note in `architecture.md`.
- If an old entry is obsolete, archive or remove it deliberately rather than leaving misleading advice behind.
