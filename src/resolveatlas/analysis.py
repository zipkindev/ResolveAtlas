"""Application service for bounded, fingerprinted evidence analysis."""

from __future__ import annotations

from dataclasses import dataclass

from resolveatlas.core.fingerprint import fingerprint_bundle
from resolveatlas.core.models import EvidenceBundle
from resolveatlas.providers.base import GenerationRequest, GenerationResponse
from resolveatlas.providers.router import ProviderRouter


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    fingerprint: str
    response: GenerationResponse


async def analyze_bundle(
    bundle: EvidenceBundle,
    *,
    task: str,
    instructions: str,
    router: ProviderRouter,
) -> AnalysisResult:
    """Fingerprint evidence before sending a bounded request to its configured route."""

    request = GenerationRequest(task=task, instructions=instructions, evidence=bundle)
    response = await router.generate(request)
    return AnalysisResult(fingerprint=fingerprint_bundle(bundle), response=response)
