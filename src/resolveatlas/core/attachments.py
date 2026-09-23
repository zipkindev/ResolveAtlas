"""Bounded normalization for explicitly supported text attachments."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import PurePath

from resolveatlas.core.models import EvidenceItem, SourceReference


@dataclass(frozen=True, slots=True)
class TextAttachmentPolicy:
    max_bytes: int = 1_000_000
    allowed_media_types: frozenset[str] = frozenset(
        {"text/plain", "text/markdown", "application/json"}
    )

    def __post_init__(self) -> None:
        if self.max_bytes < 1:
            raise ValueError("max_bytes must be positive")
        if not self.allowed_media_types:
            raise ValueError("allowed_media_types must not be empty")

    def normalize(
        self,
        *,
        filename: str,
        media_type: str,
        content: bytes,
        source_system: str,
        source_record_id: str,
        captured_at: datetime,
    ) -> EvidenceItem:
        """Validate and decode a text attachment without writing it to disk."""

        safe_name = PurePath(filename).name
        if safe_name != filename or safe_name in {"", ".", ".."}:
            raise ValueError("filename must be a single safe path component")
        normalized_type = media_type.strip().lower()
        if normalized_type not in self.allowed_media_types:
            raise ValueError("attachment media type is not allowlisted")
        if len(content) > self.max_bytes:
            raise ValueError("attachment exceeds the configured byte limit")
        if b"\x00" in content:
            raise ValueError("text attachment contains a null byte")
        try:
            body = content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("text attachment must be valid UTF-8") from error
        if not body.strip():
            raise ValueError("text attachment must not be empty")

        digest = hashlib.sha256(content).hexdigest()
        return EvidenceItem(
            evidence_id=f"attachment:{digest}",
            kind="attachment_text",
            title=safe_name,
            body=body,
            source=SourceReference(
                system=source_system,
                record_id=source_record_id,
                captured_at=captured_at,
            ),
            metadata={
                "filename": safe_name,
                "media_type": normalized_type,
                "sha256": digest,
                "size_bytes": str(len(content)),
            },
        )
