"""Deterministic, explainable scoring for related records."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone

_TOKEN = re.compile(r"[a-z0-9][a-z0-9._-]+", re.IGNORECASE)


def _normalized(values: frozenset[str]) -> frozenset[str]:
    return frozenset(value.strip().lower() for value in values if value.strip())


def _keywords(text: str) -> frozenset[str]:
    return frozenset(match.group(0).lower() for match in _TOKEN.finditer(text))


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("updated_at must be timezone-aware")
    return value.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class CandidateFeatures:
    """Comparable features derived without an AI model."""

    record_id: str
    title: str
    product_tags: frozenset[str]
    references: frozenset[str]
    updated_at: datetime

    def __post_init__(self) -> None:
        record_id = self.record_id.strip()
        title = self.title.strip()
        if not record_id:
            raise ValueError("record_id must not be empty")
        if not title:
            raise ValueError("title must not be empty")
        object.__setattr__(self, "record_id", record_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "product_tags", _normalized(self.product_tags))
        object.__setattr__(self, "references", _normalized(self.references))
        object.__setattr__(self, "updated_at", _utc(self.updated_at))


@dataclass(frozen=True, slots=True)
class CorrelationScore:
    """Normalized score and human-readable contributing reasons."""

    record_id: str
    score: float
    reasons: tuple[str, ...]


def _overlap(left: frozenset[str], right: frozenset[str]) -> frozenset[str]:
    return left & right


def _recency_points(seed: datetime, candidate: datetime) -> tuple[float, str | None]:
    days = abs((seed - candidate).total_seconds()) / 86400
    if days > 180:
        return 0.0, None
    points = 15.0 * math.exp(-days / 60)
    return points, f"updated within {math.ceil(days)} days"


def score_candidate(
    seed: CandidateFeatures,
    candidate: CandidateFeatures,
) -> CorrelationScore:
    """Score one candidate using explicit overlaps and recency.

    The score is an investigation aid, not a root-cause conclusion.
    """

    if seed.record_id == candidate.record_id:
        return CorrelationScore(candidate.record_id, 0.0, ("same record",))

    score = 0.0
    reasons: list[str] = []

    shared_refs = _overlap(seed.references, candidate.references)
    if shared_refs:
        score += min(45.0, 25.0 + 5.0 * len(shared_refs))
        reasons.append(f"{len(shared_refs)} shared reference(s)")

    shared_products = _overlap(seed.product_tags, candidate.product_tags)
    if shared_products:
        score += min(25.0, 10.0 + 5.0 * len(shared_products))
        reasons.append(f"{len(shared_products)} shared product tag(s)")

    title_overlap = _overlap(_keywords(seed.title), _keywords(candidate.title))
    if title_overlap:
        score += min(15.0, 3.0 * len(title_overlap))
        reasons.append(f"{len(title_overlap)} shared title keyword(s)")

    recency, recency_reason = _recency_points(seed.updated_at, candidate.updated_at)
    score += recency
    if recency_reason:
        reasons.append(recency_reason)

    return CorrelationScore(
        record_id=candidate.record_id,
        score=round(min(100.0, score), 2),
        reasons=tuple(reasons) if reasons else ("no matching signals",),
    )
