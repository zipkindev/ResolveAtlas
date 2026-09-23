"""Stable evidence fingerprints for cache freshness and provenance checks."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import EvidenceBundle, EvidenceItem, SourceReference


def _source_payload(source: SourceReference) -> dict[str, Any]:
    return {
        "captured_at": source.captured_at.isoformat(),
        "locator": source.locator,
        "record_id": source.record_id,
        "system": source.system,
    }


def _item_payload(item: EvidenceItem) -> dict[str, Any]:
    return {
        "body": item.body,
        "evidence_id": item.evidence_id,
        "kind": item.kind,
        "metadata": dict(item.metadata),
        "source": _source_payload(item.source),
        "title": item.title,
    }


def fingerprint_bundle(bundle: EvidenceBundle) -> str:
    """Return a versioned SHA-256 fingerprint of normalized bundle content."""

    payload = {
        "fingerprint_version": 1,
        "items": [_item_payload(item) for item in bundle.items],
        "metadata": dict(bundle.metadata),
        "subject_id": bundle.subject_id,
        "subject_type": bundle.subject_type,
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"
