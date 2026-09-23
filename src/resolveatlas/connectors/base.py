"""Protocols implemented by public and deployment-specific connectors."""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from resolveatlas.core.models import EvidenceBundle


@runtime_checkable
class CaseConnector(Protocol):
    """Retrieve normalized evidence for support cases."""

    @property
    @abstractmethod
    def connector_id(self) -> str:
        """Return a stable identifier used in configuration and provenance."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_case(self, case_id: str) -> EvidenceBundle:
        """Fetch one case and return a source-linked evidence bundle."""
        raise NotImplementedError

    @abstractmethod
    async def search_cases(self, query: str, *, limit: int) -> Sequence[EvidenceBundle]:
        """Return a bounded sequence of matching case bundles."""
        raise NotImplementedError


@runtime_checkable
class IssueConnector(Protocol):
    """Retrieve normalized evidence for engineering issues."""

    @property
    @abstractmethod
    def connector_id(self) -> str:
        """Return a stable identifier used in configuration and provenance."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_issue(self, issue_id: str) -> EvidenceBundle:
        """Fetch one issue and return a source-linked evidence bundle."""
        raise NotImplementedError

    @abstractmethod
    async def search_issues(
        self, query: str, *, limit: int
    ) -> Sequence[EvidenceBundle]:
        """Return a bounded sequence of matching issue bundles."""
        raise NotImplementedError
