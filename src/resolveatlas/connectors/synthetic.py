"""Read-only connector for the canonical synthetic ResolveAtlas fixture."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from resolveatlas.core.models import EvidenceBundle, EvidenceItem, SourceReference


def _timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class SyntheticSupportConnector:
    """Expose fictional cases and issues through the public connector contracts."""

    connector_id = "synthetic-support"

    def __init__(self, fixture_path: Path) -> None:
        raw = json.loads(fixture_path.read_text(encoding="utf-8"))
        if raw.get("fixture_kind") != "synthetic":
            raise ValueError(
                "the demo connector accepts explicitly synthetic fixtures only"
            )
        self._cases = {record["id"]: record for record in raw.get("cases", [])}
        self._issues = {record["id"]: record for record in raw.get("issues", [])}

    async def fetch_case(self, case_id: str) -> EvidenceBundle:
        try:
            record = self._cases[case_id]
        except KeyError as error:
            raise LookupError(f"synthetic case not found: {case_id}") from error
        items = tuple(
            EvidenceItem(
                evidence_id=entry["id"],
                kind=entry["kind"],
                title=f"{entry['kind'].replace('_', ' ').title()} by {entry['author']}",
                body=entry["body"],
                source=SourceReference(
                    system=self.connector_id,
                    record_id=case_id,
                    locator=f"synthetic://case/{case_id}#{entry['id']}",
                    captured_at=_timestamp(entry["timestamp"]),
                ),
                metadata={"author": entry["author"], "status": record["status"]},
            )
            for entry in record["timeline"]
        )
        return EvidenceBundle(
            subject_id=case_id,
            subject_type="case",
            items=items,
            metadata={
                "title": record["title"],
                "status": record["status"],
                "product_tags": ",".join(record["product_tags"]),
                "references": ",".join(record["references"]),
            },
        )

    async def search_cases(
        self, query: str, *, limit: int
    ) -> tuple[EvidenceBundle, ...]:
        return await self._search(self._cases, query, limit, self.fetch_case)

    async def fetch_issue(self, issue_id: str) -> EvidenceBundle:
        try:
            record = self._issues[issue_id]
        except KeyError as error:
            raise LookupError(f"synthetic issue not found: {issue_id}") from error
        items = tuple(
            EvidenceItem(
                evidence_id=entry["id"],
                kind="issue_comment",
                title=f"Issue comment by {entry['author']}",
                body=entry["body"],
                source=SourceReference(
                    system=self.connector_id,
                    record_id=issue_id,
                    locator=f"synthetic://issue/{issue_id}#{entry['id']}",
                    captured_at=_timestamp(entry["timestamp"]),
                ),
                metadata={"author": entry["author"], "status": record["status"]},
            )
            for entry in record["comments"]
        )
        return EvidenceBundle(
            subject_id=issue_id,
            subject_type="issue",
            items=items,
            metadata={
                "title": record["title"],
                "status": record["status"],
                "project": record["project"],
            },
        )

    async def search_issues(
        self, query: str, *, limit: int
    ) -> tuple[EvidenceBundle, ...]:
        return await self._search(self._issues, query, limit, self.fetch_issue)

    @staticmethod
    async def _search(records, query, limit, fetch):
        if limit < 1:
            raise ValueError("limit must be positive")
        needle = query.strip().lower()
        if not needle:
            raise ValueError("query must not be empty")
        matching = [
            record_id
            for record_id, record in records.items()
            if needle in f"{record_id} {record['title']}".lower()
        ][:limit]
        return tuple([await fetch(record_id) for record_id in matching])
