"""Provider-neutral generation contracts."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from resolveatlas.core.models import EvidenceBundle


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    """Bounded request sent to an analysis provider."""

    task: str
    instructions: str
    evidence: EvidenceBundle
    model: str | None = None
    max_output_tokens: int = 4096

    def __post_init__(self) -> None:
        if not self.task.strip():
            raise ValueError("task must not be empty")
        if not self.instructions.strip():
            raise ValueError("instructions must not be empty")
        if self.model is not None and not self.model.strip():
            raise ValueError("model must be omitted or non-empty")
        if self.max_output_tokens < 1:
            raise ValueError("max_output_tokens must be positive")


@dataclass(frozen=True, slots=True)
class GenerationResponse:
    """Provider response plus non-secret execution metadata."""

    text: str
    provider: str
    model: str
    usage: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("text must not be empty")
        if not self.provider.strip():
            raise ValueError("provider must not be empty")
        if not self.model.strip():
            raise ValueError("model must not be empty")
        if any(value < 0 for value in self.usage.values()):
            raise ValueError("usage values must not be negative")
        object.__setattr__(self, "usage", MappingProxyType(dict(self.usage)))


@runtime_checkable
class AnalysisProvider(Protocol):
    """Generate an analysis from a bounded, source-linked request."""

    @property
    @abstractmethod
    def provider_id(self) -> str:
        """Return the provider identifier recorded in result metadata."""
        raise NotImplementedError

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate one response without mutating source systems."""
        raise NotImplementedError
