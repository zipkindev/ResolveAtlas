# Decision record

## D-001: Product name

- Decision: ResolveAtlas
- Tagline: Map support signals to resolution.
- Status: selected; formal name/trademark clearance pending.

## D-002: License policy

- Decision: Apache-2.0 for the approved public repository.
- Status: applied after project-owner authorship and release attestation on
  2026-09-23; organization-content verification remains required.
- Consequence: no license is added to copied implementation until authority is
  confirmed. Required attributions will be recorded in `NOTICE`.

## D-003: Repository history

- Decision: create one new public history from a reviewed allowlist.
- Consequence: no commit, tag, branch, stash, reflog, LFS object, or release
  artifact from the private upstream is copied.

## D-004: Initial feature scope

- Decision: focused case, Jira, correlation, provider, and runtime core.
- Consequence: reporting, mutation-heavy RCA audit, and the internal tracker are
  deferred until they have independent generic boundaries and synthetic assets.

## D-005: Provider boundary

- Decision: public Gemini and direct AWS Bedrock providers in v1; private bridge
  behavior remains outside the public repository.
- Consequence: task routing uses a provider interface and must run without any
  private endpoint or model alias.

## D-006: Case connector boundary

- Decision: v1 publishes the generic case connector contract and a synthetic
  reference connector, not a browser-login flow or deployment-specific case
  system adapter.
- Consequence: production case integrations remain independently configured
  adapters until their authentication, schema, and redistribution boundaries
  receive dedicated review.

## D-007: Jira support

- Decision: the initial concrete issue adapter targets the read-only Jira Cloud
  REST v3 issue and enhanced JQL search contracts.
- Consequence: Jira Data Center/Server and write operations are not implied;
  the deployment supplies credentials through an injected transport and every
  query is scoped to one configured project.
