# ResolveAtlas

Map support signals to resolution.

ResolveAtlas is an evidence-first support intelligence workspace for connecting
customer cases, engineering issues, attachments, timelines, AI-assisted
analysis, and root-cause work. It is designed around traceable sources and
human-reviewed outcomes rather than opaque automation.

## Project status

ResolveAtlas is a production-informed, clean-room reimplementation of an
evidence-first support intelligence system. The predecessor workflows were
operated successfully in a production environment; this repository contains an
independently authored, history-clean rebuild with clearer security and
integration boundaries.

The implemented vertical slice is functional and covered by unit and contract
tests. ResolveAtlas is currently an alpha: the rearchitected system as a whole
has not completed production qualification, and integrations added during the
rebuild require validation in their intended deployment environments.

ResolveAtlas is licensed under Apache-2.0. The project owner has attested that
the clean-room implementation was created on personal time and equipment and is
authorized for release. Publication checks remain focused on ensuring that the
exact candidate contains no former-employer or customer material.

## Security automation highlights

- Exact-host outbound policy to constrain connector and provider traffic.
- Explicit AI task routing with no implicit provider fallback.
- Deterministic evidence fingerprints for freshness and substitution checks.
- Bounded attachment and connector inputs that fail closed.
- Evidence identifiers preserved through analysis for reviewable citations.
- Read-only external connectors and no source-system mutation in the alpha core.

## Planned v1

- Case timeline and attachment evidence processing.
- Jira issue and bounded-search analysis through configurable connectors.
- Explainable case-to-issue correlation.
- Provider-neutral AI routing with public Gemini and direct AWS Bedrock adapters.
- Evidence fingerprints, citations, cache freshness, and explicit generation
  controls.
- Neutral local runtime and reverse-proxy examples.

Reporting suites, source-record mutation workflows, and organization-specific
adapters are intentionally deferred until their configuration and fixture
boundaries are proven generic.

## Design principles

- Evidence before synthesis.
- Human authority before external mutation.
- Configuration instead of organization-specific constants.
- Synthetic examples only.
- Private credentials stay server-side and out of logs and browser storage.
- Public functionality must not require private networks, packages, or assets.
- Every distributed file must have documented provenance.

## Repository map

The current structure is documented in [Architecture](docs/ARCHITECTURE.md).
Publication safeguards and extraction provenance are tracked in
[Publication gates](docs/PUBLICATION_GATES.md) and
[Extraction ledger](docs/EXTRACTION_LEDGER.md). See
[Provider configuration](docs/PROVIDER_CONFIGURATION.md), the
[Threat model](docs/THREAT_MODEL.md), and [Provenance](docs/PROVENANCE.md) for
the current trust boundaries. The exact remaining work is tracked in
[Release readiness](docs/RELEASE_READINESS.md), with runtime coverage in
[Supported environments](docs/SUPPORTED_ENVIRONMENTS.md).

## Offline demonstration

The current vertical slice uses only Python's standard library and the clearly
fictional fixture in `tests/fixtures/synthetic/`. From the repository root:

```shell
PYTHONPATH=src python3 -m resolveatlas.cli \
  --fixture tests/fixtures/synthetic/support_records.json \
  analyze-case CASE-DEMO-001
```

The command prints a deterministic, evidence-cited digest and a content
fingerprint. It makes no network requests and needs no credentials. The sample
configuration in `examples/resolveatlas.toml` demonstrates explicit task
routing and a deny-by-default outbound host list.

## Security

Do not report suspected vulnerabilities in a public issue. Follow
[SECURITY.md](SECURITY.md). The reporting address will be activated before the
repository becomes public.
