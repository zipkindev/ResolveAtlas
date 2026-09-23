# Security policy

## Supported versions

ResolveAtlas has not published a supported release. Security support begins with
the first approved public version.

## Reporting a vulnerability

Do not disclose suspected vulnerabilities, credentials, customer data, or
exploitation details in a public issue. A private reporting address and GitHub
private vulnerability-reporting workflow will be configured before publication.

Until then, report findings directly to the repository owner through an already
trusted private channel. Include affected version or commit, reproduction steps,
impact, and the minimum evidence necessary to validate the issue. Do not include
real customer data or active credentials.

## Security boundaries

ResolveAtlas treats connector credentials, support evidence, attachments,
generated analyses, caches, and reports as sensitive deployment data. Operators
are responsible for access controls, retention, provider configuration, and
network policy. The project will document tested defaults before its first
release.

Dependencies and GitHub Actions are checked monthly through Dependabot. Static
analysis, vulnerability auditing, candidate scans, and artifact inspection are
rerun for every release candidate and after any security-relevant dependency or
provider-contract change.
