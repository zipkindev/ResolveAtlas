# Release runbook

No release may begin until every item in `PUBLICATION_GATES.md` is complete for
the exact candidate commit.

1. Record rightsholder authorization, name clearance, independent reviewer, and
   approval references outside the repository.
2. Verify the Apache-2.0 license and package metadata, then add only confirmed
   copyright or third-party attribution notices. An empty or speculative
   `NOTICE` file is not required.
3. From a fresh clone, install only documented public dependencies and run the
   compile, unit/contract, offline smoke, and public-tree audit commands in CI.
4. Run an independent secret scanner, dependency vulnerability/license audit,
   SAST, PII/internal-host review, and binary/archive inspection.
5. Build source and wheel artifacts; inspect their file lists and unpacked
   contents. Generate an SBOM and SHA-256 checksums for every artifact.
6. Confirm the repository has only the intended branch and no inherited tags,
   alternate refs, LFS objects, artifacts, issues, or release attachments.
7. Push only the reviewed ResolveAtlas history. Enable required reviews/checks,
   secret scanning and push protection, dependency alerts, CodeQL, and private
   vulnerability reporting before announcing the repository.
8. Sign and publish the reviewed artifacts, SBOM, checksums, changelog, and
   support policy. Re-scan the downloaded release artifacts.

Any changed byte invalidates the prior review and requires the applicable scans
and sign-off to run again.
