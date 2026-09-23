# Publication gates

ResolveAtlas must remain private and local until all gates pass for the exact
candidate commit and archive.

## Authority

- The project owner attested on 2026-09-23 that the clean implementation was
  authored on personal time and equipment and may be released under Apache-2.0.
- No contributor-owned or third-party copied implementation is present.
- A preliminary name and trademark search is recorded; the owner must accept
  the result or obtain any desired professional review before reservation.

## Content

- Every file has recorded provenance and an approved extraction disposition.
- No company branding, internal research, copied internal source, private
  provider, private deployment, production evidence, or private Git object is
  present.
- All fixtures, screenshots, and binary artifacts are synthetic and reviewable.

## Security and privacy

- Secret, PII, internal-host, binary, dependency, and provenance scans pass.
- The security model covers credentials, SSRF, uploads, archives, converters,
  filesystem access, jobs, mutations, retention, and AI-provider boundaries.
- No documented feature requires private infrastructure.

## Quality

- A clean clone installs and tests using public dependencies only.
- The documented v1 workflows pass unit, integration, contract, UI, and offline
  smoke tests.
- An independent reviewer approves the exact commit and archive.

## Publication

- Only the new ResolveAtlas history is pushed.
- Branch protection, required checks, dependency alerts, secret scanning, and
  private vulnerability reporting are enabled.
- Release checksums, SBOM, changelog, and support policy are published.
