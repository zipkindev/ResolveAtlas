"""Read-only Jira Cloud REST v3 connector with configurable transport."""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable, Mapping
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote, urlsplit

from resolveatlas.core.models import EvidenceBundle, EvidenceItem, SourceReference
from resolveatlas.security.outbound import OutboundPolicy

JsonTransport = Callable[
    [str, str, Mapping[str, Any] | None], Awaitable[dict[str, Any]]
]
_PROJECT_KEY = re.compile(r"[A-Z][A-Z0-9_]{0,19}\Z")
_ISSUE_KEY = re.compile(r"[A-Z][A-Z0-9_]{0,19}-[1-9][0-9]*\Z")


def _adf_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(filter(None, (_adf_text(item) for item in value))).strip()
    if isinstance(value, dict):
        own = value.get("text", "")
        children = _adf_text(value.get("content", []))
        return " ".join(filter(None, (str(own).strip(), children))).strip()
    return ""


def _jira_time(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class JiraCloudConnector:
    """Retrieve issue evidence using Jira Cloud's documented read APIs."""

    connector_id = "jira-cloud-v3"

    def __init__(
        self, *, base_url: str, project_key: str, transport: JsonTransport
    ) -> None:
        project = project_key.strip().upper()
        if not _PROJECT_KEY.fullmatch(project):
            raise ValueError("project_key must be a valid Jira project key")
        parsed = urlsplit(base_url.strip())
        if (
            parsed.hostname is None
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError(
                "base_url must be an HTTPS origin without path, query, or fragment"
            )
        policy = OutboundPolicy(frozenset({parsed.hostname}))
        self._base_url = policy.validate(base_url).rstrip("/")
        self._policy = policy
        self._project = project
        self._transport = transport

    async def fetch_issue(self, issue_id: str) -> EvidenceBundle:
        key = issue_id.strip().upper()
        if not _ISSUE_KEY.fullmatch(key) or not key.startswith(f"{self._project}-"):
            raise ValueError("issue_id must belong to the configured project")
        url = f"{self._base_url}/rest/api/3/issue/{quote(key)}"
        raw = await self._transport("GET", self._policy.validate(url), None)
        return self._bundle(raw)

    async def search_issues(
        self, query: str, *, limit: int
    ) -> tuple[EvidenceBundle, ...]:
        expression = query.strip()
        if not expression:
            raise ValueError("query must not be empty")
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        url = f"{self._base_url}/rest/api/3/search/jql"
        raw = await self._transport(
            "POST",
            self._policy.validate(url),
            {
                "jql": f'project = "{self._project}" AND ({expression})',
                "maxResults": limit,
                "fields": ["summary", "description", "status", "updated", "comment"],
            },
        )
        issues = raw.get("issues")
        if not isinstance(issues, list):
            raise RuntimeError("Jira search returned an unexpected response shape")
        return tuple(self._bundle(issue) for issue in issues)

    def _bundle(self, raw: Mapping[str, Any]) -> EvidenceBundle:
        key = str(raw.get("key", "")).strip().upper()
        fields = raw.get("fields")
        if not _ISSUE_KEY.fullmatch(key) or not key.startswith(f"{self._project}-"):
            raise RuntimeError("Jira returned an issue outside the configured project")
        if not isinstance(fields, dict):
            raise RuntimeError("Jira issue returned an unexpected response shape")

        summary = str(fields.get("summary", "")).strip()
        if not summary:
            raise RuntimeError("Jira issue is missing its summary")
        updated = _jira_time(fields.get("updated"))
        items = [
            EvidenceItem(
                evidence_id=f"{key}:summary",
                kind="issue_summary",
                title=summary,
                body=_adf_text(fields.get("description")) or "No description supplied.",
                source=SourceReference(
                    system=self.connector_id,
                    record_id=key,
                    locator=f"{self._base_url}/browse/{quote(key)}",
                    captured_at=updated,
                ),
            )
        ]
        comments = fields.get("comment", {}).get("comments", [])
        if not isinstance(comments, list):
            raise RuntimeError("Jira comments returned an unexpected response shape")
        for comment in comments:
            comment_id = str(comment.get("id", "")).strip()
            body = _adf_text(comment.get("body"))
            if not comment_id or not body:
                continue
            items.append(
                EvidenceItem(
                    evidence_id=f"{key}:comment:{comment_id}",
                    kind="issue_comment",
                    title=f"Comment {comment_id}",
                    body=body,
                    source=SourceReference(
                        system=self.connector_id,
                        record_id=key,
                        locator=f"{self._base_url}/browse/{quote(key)}?focusedCommentId={quote(comment_id)}",
                        captured_at=_jira_time(
                            comment.get("updated") or comment.get("created")
                        ),
                    ),
                )
            )
        status = fields.get("status", {})
        status_name = (
            status.get("name", "unknown") if isinstance(status, dict) else "unknown"
        )
        return EvidenceBundle(
            subject_id=key,
            subject_type="issue",
            items=tuple(items),
            metadata={
                "title": summary,
                "status": str(status_name),
                "project": self._project,
            },
        )
