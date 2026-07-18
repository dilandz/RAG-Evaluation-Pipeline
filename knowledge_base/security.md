# NovaTech Security Policies

## Data Encryption

All data in transit is encrypted using TLS 1.3. Data at rest is encrypted using AES-256. Encryption keys are managed through AWS KMS with automatic rotation every 90 days.

## Access Control

NovaTech implements role-based access control (RBAC) with the principle of least privilege. All access changes are logged in an immutable audit trail accessible via GET /api/v2/audit-logs.

## Compliance

NovaTech is certified for:
- SOC 2 Type II
- HIPAA (with BAA)
- GDPR (EU data residency available)
- ISO 27001

## Data Retention

- Active connections: Data retained indefinitely while connection is active
- Deleted connections: Metadata removed within 24 hours, cached data purged within 7 days
- Audit logs: Retained for 2 years minimum
- Query history: Retained for 90 days

## Incident Response

Security incidents are classified as P1 (critical), P2 (high), P3 (medium), P4 (low). P1 incidents trigger immediate notification to all affected customers within 1 hour. Post-incident reports are published within 5 business days.

## Network Security

NovaTech platform egress IPs: 52.14.88.0/24 and 3.135.200.0/24 (US-East), 18.130.56.0/24 (EU-West). Allowlist these ranges in your firewall for NovaTech to reach your data sources.