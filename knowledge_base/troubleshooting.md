# NovaTech Troubleshooting Guide

## Connection Failures

### Error: CONN_TIMEOUT
The platform cannot reach the data source within 30 seconds.

Fix: Check that the source's firewall allows inbound connections from NovaTech IP ranges (listed in Settings > Network). Verify the hostname and port are correct.

### Error: AUTH_FAILED
Authentication credentials are invalid or expired.

Fix: Regenerate credentials in the source system and update them in NovaTech via PUT /api/v2/connections/{id}. For OAuth sources, re-authorize through the dashboard.

### Error: SCHEMA_MISMATCH
The source schema has changed since the last sync.

Fix: Run a schema refresh from the connection details page or POST /api/v2/connections/{id}/refresh-schema. Review the detected changes before approving.

## Sync Issues

### Partial Sync Failures
If a sync partially completes, check the sync logs at GET /api/v2/connections/{id}/logs. Common causes: network interruption, source rate limiting, or row-level permission errors.

### Duplicate Records
NovaTech uses event IDs for deduplication. If you see duplicates, ensure your source provides unique identifiers. Configure the dedup key in connection settings.

## Performance

### Slow Queries
Queries taking over 10 seconds may benefit from materialized views. Create them via POST /api/v2/materialized-views. Ensure your query uses indexed columns for filtering.

### How to Reset Your API Key
Navigate to Settings > API Keys, click the three-dot menu next to your key, select "Regenerate". The old key is immediately invalidated. Update all applications using the old key.