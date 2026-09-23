"""Stable serialization of source-linked evidence for public AI providers."""

from __future__ import annotations

from resolveatlas.providers.base import GenerationRequest


def render_request(request: GenerationRequest) -> str:
    """Render only the bounded request and explicit evidence citations."""

    lines = [
        request.instructions,
        "",
        f"Subject: {request.evidence.subject_id}",
        "Evidence:",
    ]
    for item in request.evidence.items:
        lines.extend(
            (
                f"[{item.evidence_id}] {item.title}",
                item.body,
                f"Source system: {item.source.system}; record: {item.source.record_id}",
            )
        )
    lines.append(
        "Cite evidence identifiers in square brackets and do not add unsupported facts."
    )
    return "\n".join(lines)
