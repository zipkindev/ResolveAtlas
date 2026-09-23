# ResolveAtlas agent instructions

These instructions apply to coding and review agents in this repository.

## Publication state

- This repository is a clean extraction workspace, not yet approved for public
  release.
- Do not add a remote, publish packages, create releases, or change repository
  visibility without explicit authorization and completed publication gates.
- Do not copy Git objects, commits, tags, branches, generated artifacts, or
  unreviewed files from the private upstream.

## Source and data rules

- Import only files recorded in `docs/EXTRACTION_LEDGER.md` with an approved
  disposition.
- Treat all upstream customer, employee, ticket, case, infrastructure, research,
  benchmark, branding, prompt, and deployment material as private by default.
- Examples and tests must use the documented synthetic dataset. Do not transform
  production identifiers or paraphrase production narratives into fixtures.
- External URLs, object names, field mappings, project keys, workflow states,
  and mutations must be operator configuration.
- Never print suspected secret values. Report only rule, path, and remediation.

## Architecture rules

- Keep connectors, AI providers, evidence processing, domain analysis, and HTTP
  presentation behind explicit interfaces.
- Public providers may use documented public APIs only.
- External mutations require authorization, explicit user intent, idempotency,
  and auditable results.
- Preserve evidence citations and freshness/fingerprint checks across AI paths.
- Prefer guard clauses and clear failure paths over deep nesting.
- Do not leave stubs or placeholder implementations in final code.

## Verification

- Run the narrowest relevant tests for local changes.
- Run the private upstream candidate scanner after each extraction batch.
- Before release, run secret, PII, internal-host, binary, provenance, dependency,
  and clean-clone checks against the exact commit and archive.
