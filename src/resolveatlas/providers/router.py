"""Explicit task-to-provider routing with no implicit data egress fallback."""

from __future__ import annotations

from collections.abc import Mapping

from resolveatlas.providers.base import (
    AnalysisProvider,
    GenerationRequest,
    GenerationResponse,
)


class ProviderRouter:
    """Route each configured task to exactly one registered provider."""

    def __init__(
        self,
        providers: Mapping[str, AnalysisProvider],
        task_routes: Mapping[str, str],
    ) -> None:
        self._providers = dict(providers)
        self._routes = dict(task_routes)
        if len(self._providers) != len(set(self._providers)):
            raise ValueError("provider identifiers must be unique")
        for provider_id, provider in self._providers.items():
            if provider_id != provider.provider_id:
                raise ValueError(
                    f"provider key {provider_id!r} does not match provider_id"
                )
        missing = set(self._routes.values()) - set(self._providers)
        if missing:
            raise ValueError(
                f"unregistered provider route(s): {', '.join(sorted(missing))}"
            )

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate using only the provider explicitly configured for the task."""

        provider_id = self._routes.get(request.task)
        if provider_id is None:
            raise LookupError(f"no provider route configured for task {request.task!r}")
        return await self._providers[provider_id].generate(request)
