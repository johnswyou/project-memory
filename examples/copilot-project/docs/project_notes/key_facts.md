# Key Facts

## API Configuration
- Production URL: `https://api.example.com`
- Staging URL: `https://staging-api.example.com`
- Local URL: `http://localhost:8000`

## Identity
- OAuth client secret location: Secret Manager secret `oauth-client-secret`
- Local frontend dev ports that must be allowlisted for auth callbacks: `3000`, `5173`

## Local Development
- Backend API port: `8000`
- Frontend port: `3000`
- Alternate frontend port: `5173`
- Redis port: `6379`

## Deployment
- Cloud Run service: `api-service`
- Region: `us-central1`
- Deploy image registry: `us-central1-docker.pkg.dev/example-org/platform/api`
