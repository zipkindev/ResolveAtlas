"""Provider-neutral evidence models used across ResolveAtlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Mapping


def _required(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("captured_at must be timezone-aware")
    return value.astimezone(timezone.utc)


def _metadata(value: Mapping[str, str]) -> Mapping[str, str]:
    normalized: dict[str, str] = {}
    for raw_key, raw_value in value.items():
        key = _required(str(raw_key), "metadata key")
        normalized[key] = str(raw_value)
    return MappingProxyType(dict(sorted(normalized.items())))


@dataclass(frozen=True, slots=True)
class SourceReference:
    """Traceable origin for an evidence item."""

    system: str
    record_id: str
    locator: str | None = None
    captured_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        object.__setattr__(self, "system", _required(self.system, "system"))
        object.__setattr__(self, "record_id", _required(self.record_id, "record_id"))
        if self.locator is not None:
            object.__setattr__(self, "locator", _required(self.locator, "locator"))
        object.__setattr__(self, "captured_at", _utc(self.captured_at))


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    """One normalized, source-linked unit of evidence."""

    evidence_id: str
    kind: str
    title: str
    body: str
    source: SourceReference
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evidence_id", _required(self.evidence_id, "evidence_id")
        )
        object.__setattr__(self, "kind", _required(self.kind, "kind"))
        object.__setattr__(self, "title", _required(self.title, "title"))
        object.__setattr__(self, "body", _required(self.body, "body"))
        object.__setattr__(self, "metadata", _metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class EvidenceBundle:
    """Deterministically ordered evidence for one analysis subject."""

    subject_id: str
    subject_type: str
    items: tuple[EvidenceItem, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "subject_id", _required(self.subject_id, "subject_id"))
        object.__setattr__(
            self, "subject_type", _required(self.subject_type, "subject_type")
        )
        if not self.items:
            raise ValueError("items must contain at least one evidence item")

        evidence_ids = [item.evidence_id for item in self.items]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("evidence_id values must be unique within a bundle")

        object.__setattr__(
            self,
            "items",
            tuple(sorted(self.items, key=lambda item: item.evidence_id)),
        )
        object.__setattr__(self, "metadata", _metadata(self.metadata))
