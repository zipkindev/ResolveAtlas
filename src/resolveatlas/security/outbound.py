"""Fail-closed validation for operator-configured outbound HTTP endpoints."""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from urllib.parse import urlsplit


class OutboundPolicyError(ValueError):
    """Raised when an outbound URL violates connector network policy."""


def _normalize_host(value: str) -> str:
    candidate = value.strip().lower().rstrip(".")
    if not candidate:
        raise OutboundPolicyError("allowed host must not be empty")
    if "://" in candidate or "/" in candidate or "@" in candidate:
        raise OutboundPolicyError("allowed hosts must be hostnames, not URLs")
    return candidate


def _is_loopback(host: str) -> bool:
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


@dataclass(frozen=True, slots=True)
class OutboundPolicy:
    """Validate scheme, authority, port, and exact destination host."""

    allowed_hosts: frozenset[str]
    allow_http_loopback: bool = False
    allowed_ports: frozenset[int] = frozenset({443})

    def __post_init__(self) -> None:
        hosts = frozenset(_normalize_host(host) for host in self.allowed_hosts)
        if not hosts:
            raise OutboundPolicyError("at least one allowed host is required")
        if any(port < 1 or port > 65535 for port in self.allowed_ports):
            raise OutboundPolicyError("allowed ports must be between 1 and 65535")
        object.__setattr__(self, "allowed_hosts", hosts)

    def validate(self, raw_url: str) -> str:
        """Return a normalized URL or raise without making a network request."""

        value = raw_url.strip()
        if not value:
            raise OutboundPolicyError("outbound URL must not be empty")

        parsed = urlsplit(value)
        if parsed.scheme not in {"https", "http"}:
            raise OutboundPolicyError("outbound URL must use https")
        if parsed.username is not None or parsed.password is not None:
            raise OutboundPolicyError("credentials are not allowed in outbound URLs")
        if parsed.fragment:
            raise OutboundPolicyError("outbound URL must not include a fragment")
        if parsed.hostname is None:
            raise OutboundPolicyError("outbound URL must include a hostname")

        host = parsed.hostname.lower().rstrip(".")
        if host not in self.allowed_hosts:
            raise OutboundPolicyError("outbound hostname is not allowlisted")

        if parsed.scheme == "http" and not (
            self.allow_http_loopback and _is_loopback(host)
        ):
            raise OutboundPolicyError(
                "plain HTTP is allowed only for configured loopback"
            )

        try:
            port = parsed.port
        except ValueError as exc:
            raise OutboundPolicyError("outbound URL has an invalid port") from exc

        effective_port = port or (443 if parsed.scheme == "https" else 80)
        if effective_port not in self.allowed_ports:
            raise OutboundPolicyError("outbound port is not allowlisted")

        if parsed.scheme == "https" and effective_port == 443:
            authority = host
        elif parsed.scheme == "http" and effective_port == 80:
            authority = host
        else:
            authority = f"{host}:{effective_port}"

        path = parsed.path or "/"
        normalized = f"{parsed.scheme}://{authority}{path}"
        if parsed.query:
            normalized = f"{normalized}?{parsed.query}"
        return normalized
