# Key Facts Template

Use this file for frequently needed **non-secret** project facts. Organize information by category and keep it safe to commit.

## Security rules

**Never store passwords, API keys, tokens, private keys, or other secret values in this file.**

**Do store:**

- public URLs
- service-account email addresses
- project IDs, regions, cluster names, and port numbers
- environment variable names
- secret locations such as `.env`, Vault paths, or Secret Manager names

**Do not store:**

- raw credential values
- full DSNs that contain usernames and passwords
- private key material
- copied shell placeholders that imply secret values in tracked documentation
- anything that could be pasted into a terminal or client to authenticate directly

## Canonical structure

### Project Information
- Project ID: `my-company-prod`
- Region: `us-central1`
- Primary environment: `production`

### Database Configuration

**Cluster:**
- Cluster Name: `prod-cluster`
- Instance Name: `prod-primary`
- Region: `us-central1`
- Local proxy port: `5432`

**Connection Notes:**
- Use AlloyDB Auth Proxy for local development.
- Local environment variable name: `DATABASE_URL`
- Secret location: local `.env` for development; Secret Manager secret `database-url` for deployed environments

**Authentication:**
- Service account email: `alloydb-client@my-company-prod.iam.gserviceaccount.com`
- Local credential file is selected via `GOOGLE_APPLICATION_CREDENTIALS`; do not record the file contents here.

### API Configuration

**Endpoints:**
- Production URL: `https://api.mycompany.com`
- Staging URL: `https://api-staging.mycompany.com`
- Local URL: `http://localhost:8000`

**Identity:**
- OAuth Client ID (public): `123456789-abcdefg.apps.googleusercontent.com`
- OAuth client secret location: Secret Manager secret `oauth-client-secret`
- Local environment variable name: `OAUTH_CLIENT_SECRET`
- Local callback ports: `3000`, `5173`

### Local Development
- Backend API port: `8000`
- Frontend port: `3000`
- Alternate frontend port: `5173`
- Redis port: `6379`

### Important URLs
- Cloud Console: `https://console.cloud.google.com/home/dashboard?project=my-company-prod`
- Logs: `https://console.cloud.google.com/logs?project=my-company-prod`
- Runbook: `https://wiki.mycompany.com/runbook`

## Tips

- Prefer names and locations over values.
- Keep the highest-signal facts near the top of each section because fresh sessions may skim this file quickly.
- For large repositories, keep environment-wide facts here and put subsystem structure in `architecture.md`.
- Mark deprecated facts clearly with dates or status notes.
- Remove stale facts once a migration is complete so future sessions do not inherit dead config.
