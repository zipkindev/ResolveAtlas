"""Security policies shared by connectors and providers."""

from .outbound import OutboundPolicy, OutboundPolicyError

__all__ = ["OutboundPolicy", "OutboundPolicyError"]
