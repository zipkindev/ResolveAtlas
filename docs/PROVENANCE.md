# Source and asset provenance

This inventory applies to the alpha candidate working tree. It must be reviewed
again for the exact release commit and built artifacts.

| Paths | Origin | Redistribution status |
|---|---|---|
| Root Markdown policies and project documents | Newly authored for ResolveAtlas in the clean repository | Apache-2.0 |
| `docs/**` | Newly authored architecture, decisions, controls, and runbooks | Apache-2.0 |
| `src/resolveatlas/**` | Newly authored implementation against public Python, Gemini REST, and AWS Bedrock Converse contracts | Apache-2.0 |
| `tests/**` | Newly authored tests; data is the fictional Example Manufacturing Cooperative dataset | Apache-2.0 |
| `scripts/audit_public_tree.py` | Newly authored candidate safety tool | Apache-2.0 |
| `examples/**` | Newly authored neutral configuration using no live endpoint or credential | Apache-2.0 |
| `.github/**` | Newly authored repository automation and contribution template using public GitHub Actions | Apache-2.0 |
| `.editorconfig`, `.gitattributes`, `.gitignore`, `pyproject.toml` | Newly authored project/build configuration | Apache-2.0 |
| `LICENSE` | Unmodified Apache License 2.0 text | Apache-2.0 |

No private-upstream implementation, Git object, logo, screenshot, font, binary,
Office document, vendored library, customer record, employee record, copied
prompt, or internal research document is present. There are no generated files
intended for distribution in the current tree.

## External contracts and dependencies

- Python standard library: runtime implementation and offline workflow.
- Gemini public `generateContent` REST contract: request/response adapter shape.
- AWS Bedrock Runtime public `Converse` contract: request/response adapter shape.
- `boto3`: optional runtime dependency for the normal public AWS credential and
  service client chain; not vendored.
- Hatchling: build backend only; not vendored.
- pytest: optional test convenience; the canonical suite also runs with
  `unittest`; not vendored.
- GitHub-maintained checkout, setup-python, CodeQL, and dependency-review
  Actions: referenced by workflow tag; not vendored.

No external prose or source was copied into the repository. API behavior is
implemented from public documentation and verified through injected contract
tests rather than copied SDK or internal bridge code.

## Owner attestation

On 2026-09-23, the project owner stated that the project implementation was
created on personal time and personal equipment and authorized its release.
Accordingly, Apache-2.0 is applied to this clean repository. This attestation
does not extend to material from the private upstream; such material remains
excluded unless independently re-authored and reviewed.
