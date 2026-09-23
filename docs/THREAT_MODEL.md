# Threat model

This model covers the implemented alpha core and identifies controls
required before higher-risk features are added.

## Protected assets

- Connector credentials and provider API credentials.
- Raw case, issue, attachment, and timeline evidence.
- Generated analyses, evidence fingerprints, caches, and audit records.
- Operator configuration and authorization decisions.

## Trust boundaries and current controls

| Boundary | Primary risk | Implemented control |
|---|---|---|
| Connector to external service | SSRF or credential disclosure | Exact-host HTTPS allowlist; URLs cannot contain credentials or fragments |
| Evidence to AI provider | Unintended data egress | Explicit task routing; no fallback provider; offline provider available |
| Provider response to analysis | Unsupported or malformed output | Response-shape validation; evidence identifiers included in prompts and local output |
| Source evidence to cache/result | Stale or substituted evidence | Canonical SHA-256 evidence fingerprint |
| Demonstration data to repository | Customer or employee disclosure | Explicit synthetic marker, reserved example domain, candidate scanner |
| Analysis to source systems | Unauthorized mutation | No mutation capability in the implemented core |

## Required controls before adding features

- Authentication and sessions: use secure, HTTP-only, same-site cookies; rotate
  sessions; enforce CSRF protection; do not put connector tokens in browsers.
- Credential persistence: use an external secret manager or OS-protected store;
  never write secrets to project configuration, logs, exception text, or output.
- Attachments and archives: impose byte/count/depth/ratio limits, validate paths
  after extraction, reject links and special files, isolate parsers, and treat
  MIME declarations as untrusted.
- Document conversion: sandbox converters with resource/time limits and no
  ambient filesystem or network access.
- Filesystem and downloads: use opaque identifiers and a fixed data root; prevent
  traversal, symlink escape, and user-selected output paths.
- Background jobs: enforce ownership, cancellation, timeouts, quotas, bounded
  queues, idempotency, and nonsecret structured logs.
- Mutations: require explicit user intent, authorization, previews, idempotency
  keys, constrained field mappings, and immutable audit outcomes.
- Retention and deletion: define per-artifact TTLs and verified deletion for raw
  evidence, attachments, caches, jobs, analyses, and backups.
- Proxy/deployment: terminate TLS safely, restrict forwarded headers and request
  size, set browser security headers, and never ship an internal hostname.

## Residual risk

An allowlist and citation contract reduce accidental egress and unsupported
claims; they do not determine whether an operator is authorized to transmit a
particular record to a configured provider. Deployments remain responsible for
data classification, provider terms, regional requirements, access policy, and
human review of consequential decisions.
