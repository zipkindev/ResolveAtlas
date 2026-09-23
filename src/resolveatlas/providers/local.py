"""Deterministic offline provider for demos, tests, and privacy-safe evaluation."""

from __future__ import annotations

from resolveatlas.providers.base import GenerationRequest, GenerationResponse


class LocalEvidenceProvider:
    """Render a source-linked digest without network access or model inference."""

    provider_id = "local-evidence"

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        lines = [
            f"Analysis task: {request.task}",
            f"Subject: {request.evidence.subject_id}",
            "Evidence:",
        ]
        for item in request.evidence.items:
            lines.append(f"- [{item.evidence_id}] {item.title}: {item.body}")
        lines.append(
            "Review required: this digest is evidence organization, not a root-cause decision."
        )
        return GenerationResponse(
            text="\n".join(lines),
            provider=self.provider_id,
            model="deterministic-v1",
            usage={"input_items": len(request.evidence.items)},
        )
