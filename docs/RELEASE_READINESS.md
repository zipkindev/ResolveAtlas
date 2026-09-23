# Release readiness review

Reviewed: 2026-09-23

## Decision

The clean ResolveAtlas history and implemented vertical slice are now available
as a public alpha. The rebuild has not completed production qualification, and
no stable package or release has been published. Independent review, namespace
reservation, branch rules, and final release-artifact checks remain outstanding.

## Completed evidence

- Project-owner authorization and Apache-2.0 application are recorded.
- The tree was re-authored in a new repository with zero inherited commits,
  objects, refs, tags, LFS data, or remotes.
- Thirty-five unit and contract tests plus offline source and installed-CLI smoke
  tests pass.
- Ruff formatting/lint and Bandit static security checks pass.
- The source tree, wheel, and source distribution pass the public and private
  candidate scanners with zero findings.
- Expanded targeted scans found no former-organization name/domain, known
  customer name, internal ticket pattern, Salesforce identifier, branding,
  binary asset, production identifier, or private-history marker.
- The optional AWS runtime dependency set has no known published vulnerability
  after toolchain update. Runtime licenses are Apache-2.0, MIT, or BSD compatible.
- A valid CycloneDX 1.6 environment SBOM was generated. The final release SBOM
  must be regenerated from the exact release environment.
- The GitHub repository is public. Secret scanning, push protection, Dependabot
  alerts and security updates, automated security fixes, private vulnerability
  reporting, dependency review, and CodeQL are enabled and passing.

## Name and namespace review

Read-only checks on 2026-09-23 found:

| Namespace | Result |
|---|---|
| GitHub repository search | Zero repositories named ResolveAtlas |
| Intended owner/repository path | Not found |
| GitHub user and organization handles | Not found |
| PyPI `resolveatlas` | Not found |
| npm `resolveatlas` | Not found |
| Docker Hub search | Zero results |
| `resolveatlas.com` and `resolveatlas.dev` RDAP | Not found |
| Exact-mark web searches across USPTO/EUIPO/Canadian/Justia indexes | No results |

These results indicate low observed collision risk, but they are not a legal
trademark opinion and do not reserve any namespace. Availability can change at
any time.

## Remaining release gates

1. Preserve the owner's authorship and Apache-2.0 authorization in a durable
   record outside the Git repository.
2. Accept the preliminary name review or obtain any desired professional
   trademark review, then reserve the chosen GitHub/package/domain namespaces.
3. Have someone other than the extractor review the exact commit, file inventory,
   provenance record, and unpacked wheel/source archive.
4. Configure branch rules and required checks appropriate for an owner-maintained
   alpha without preventing emergency maintenance.
5. Generate the final SBOM, checksums, changelog entry, and signed release from
   the approved commit; scan the downloaded release artifacts once more.

## Not release blockers for focused v1

- Salesforce/browser login, a web UI, reporting suites, binary Office fixtures,
  mutation workflows, reverse proxy, supervisor, and deployment automation are
  intentionally outside the focused v1 scope.
- The private upstream's historical research credentials are absent from the
  clean candidate. Any rotation is a private-upstream operational matter, not a
  ResolveAtlas publication dependency.
- A `NOTICE` file is not required because no copied work carrying a required
  notice is distributed.
