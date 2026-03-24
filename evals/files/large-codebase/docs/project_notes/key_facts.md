# Key Facts

## API and UI Endpoints
- Production API URL: `https://api.example.com`
- Staging API URL: `https://staging-api.example.com`
- Local admin UI URLs: `http://localhost:3000`, `http://localhost:5173`

## Identity
- OAuth client secret location: Secret Manager secret `admin-oauth-client-secret`
- Callback allowlist must include both local admin UI ports: `3000` and `5173`

## Queueing
- Primary queue name: `order-sync`
- Dead-letter queue name: `order-sync-dlq`

## Data
- Migration tool: Alembic
- Outbox table name: `event_outbox`
