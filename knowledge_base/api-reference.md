# NovaTech API Reference

## Authentication

All API requests require a Bearer token in the Authorization header. Generate tokens from the Settings > API Keys page in the dashboard.

```
Authorization: Bearer nt_live_xxxxxxxxxxxx
```

Tokens prefixed with `nt_live_` are production tokens. Tokens prefixed with `nt_test_` are sandbox tokens that do not affect production data.

## Rate Limits

- Starter plan: 100 requests per minute
- Professional plan: 1000 requests per minute
- Enterprise plan: 10000 requests per minute

Exceeding rate limits returns HTTP 429 with a Retry-After header.

## Endpoints

### POST /api/v2/connections
Create a new data source connection.

Required fields: `name`, `type`, `credentials`
Optional fields: `schema_override`, `sync_frequency`, `tags`

### GET /api/v2/connections/{id}/status
Returns the current sync status of a connection.

Response includes: `status` (active, paused, error), `last_sync_at`, `records_processed`, `error_message`

### POST /api/v2/queries
Execute an analytics query against connected sources.

Required fields: `sql`, `connection_ids`
Optional fields: `timeout_seconds`, `cache_ttl`

### DELETE /api/v2/connections/{id}
Remove a connection and all associated metadata. This does NOT delete the underlying data source.