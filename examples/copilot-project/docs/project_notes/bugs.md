# Project Bug Log

### 2026-03-01 - Staging API returned 401 in local development
- **Issue**: Engineers could not log in against staging from local machines.
- **Root Cause**: The local callback URL was missing from the identity provider allowlist.
- **Solution**: Added the local callback URL to the staging OAuth application settings.
- **Prevention**: Review callback URLs whenever a new environment or port is introduced.
- **Related**: `issues.md` API-142, `key_facts.md` Identity, `architecture.md` Known Gotchas
