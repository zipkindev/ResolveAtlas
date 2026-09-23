# Extraction ledger

No implementation file is approved merely because its directory appears here.
Each imported file will receive a disposition and reviewer before it enters the
public candidate.

Disposition values:

- `copy-after-review`: generic and independently reviewed.
- `generalize`: reusable mechanics remain after configuration and naming work.
- `re-author`: behavior may remain, but the source or text must be recreated.
- `private-adapter`: excluded from public code behind a published interface.
- `exclude`: not part of ResolveAtlas.

## Area-level starting classification

| Private upstream area | Initial disposition | ResolveAtlas destination | Reason |
|---|---|---|---|
| Shared supervisor/health/job helpers | Generalize | `src/resolveatlas/runtime/` | Useful mechanics; names, paths, and service assumptions require review |
| Home/session shell | Generalize | `apps/web/` and core identity interfaces | Authentication and UI are coupled to private naming and schema |
| Case analysis | Generalize file by file | `src/resolveatlas/cases/` | Core evidence behavior is reusable; prompts, schema, branding, fixtures, and providers are mixed |
| Jira analysis | Generalize file by file | `src/resolveatlas/issues/` | Connector and credential behavior need endpoint/project generalization |
| Case correlation | Generalize | `src/resolveatlas/correlation/` | Scoring is a public-core candidate after identifiers and connector assumptions are removed |
| Public Gemini adapter | Generalize | `src/resolveatlas/providers/gemini.py` | Retain documented public API behavior only |
| Direct AWS Bedrock adapter | Generalize | `src/resolveatlas/providers/bedrock.py` | Retain documented public AWS behavior only |
| Internal AI bridge and probes | Private adapter | Not exported | Private endpoint, aliases, behavior, and benchmarks |
| Reverse proxy | Generalize selectively | `deploy/examples/` | Keep neutral local examples; exclude certificate/deployment assumptions not needed by v1 |
| Reporting applications | Deferred | Future packages | Templates, customer fields, and binary fixtures need independent extraction |
| RCA Audit mutations | Deferred/private adapter | Future workflow interface | Business rules and source mutations require stronger configuration boundary |
| Internal tracker | Deferred | Undecided | Product fit and identity assumptions need review |
| Research, history, plans, benchmarks, and generated artifacts | Exclude | Not exported | Private provenance or production-derived content |
| Existing README, agent rules, examples, and product docs | Re-author | Root and `docs/` | Avoid carrying private names, examples, and claims |

## Batch record

| Batch | Scope | Status | Verification |
|---|---|---|---|
| 0 | Clean repository and original governance/architecture documents | Complete | Candidate scan clean; zero Git objects/remotes; manual review |
| 1 | Newly authored evidence models, fingerprints, interfaces, and correlation | Complete | Eight unit tests pass; candidate scan clean |
| 2 | Outbound policy and canonical synthetic support dataset | Complete | Six unit tests pass; manual fixture review; candidate scan clean |
| 3 | Configuration, explicit provider routing, demo connector, offline provider, analysis service, and CLI | Complete | Ten unit/contract tests and offline smoke test pass; candidate scan clean |
| 4 | Public Gemini REST and AWS Bedrock Converse adapters | Complete | Three injected-transport contract tests pass; official API documentation reviewed |
| 5 | Public CI, candidate audit, threat model, provider guide, release runbook, and provenance inventory | Complete | 29 tests pass; both candidate scans clean; workflows manually reviewed |
| 6 | Isolated installation and installed CLI smoke test | Complete | Editable wheel built in a fresh temporary venv; installed CLI passed offline smoke test |
| 7 | Bounded text attachments and read-only Jira Cloud v3 connector | Complete | Six unit/contract tests; official REST API review; candidate scans clean |
| 8 | Pre-release source distribution and wheel inspection | Complete | Artifacts built without isolation; file lists reviewed; both scanners clean on unpacked artifacts; SHA-256 checksums generated locally |
| 9 | Apache-2.0 application and organization-content re-audit | Complete | License embedded in wheel/sdist metadata; 35 tests pass; expanded organization/customer scan and both tree/artifact scanners clean |
| 10 | Remaining-gate reconciliation, namespace review, SBOM, dependency licenses/vulnerabilities, Ruff, and Bandit | Complete | Low observed name collision; CycloneDX 1.6 SBOM; no known dependency vulnerabilities; compatible licenses; quality/security checks pass |
| 11 | Clean root commit and fresh-clone verification | Complete | One root commit; 35 tests and quality/security checks pass; wheel/sdist rebuilt and both unpacked artifacts scan clean |
