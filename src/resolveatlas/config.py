"""Strict, dependency-free configuration for ResolveAtlas runtimes."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Validated task routing and outbound-network policy."""

    task_routes: Mapping[str, str]
    allowed_hosts: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        routes: dict[str, str] = {}
        for raw_task, raw_provider in self.task_routes.items():
            task = str(raw_task).strip()
            provider = str(raw_provider).strip()
            if not task or not provider:
                raise ValueError("task route names and providers must not be empty")
            routes[task] = provider

        hosts = frozenset(str(host).strip().lower() for host in self.allowed_hosts)
        if "" in hosts:
            raise ValueError("allowed_hosts must not contain empty values")

        object.__setattr__(self, "task_routes", MappingProxyType(routes))
        object.__setattr__(self, "allowed_hosts", hosts)


def load_config(path: Path) -> AppConfig:
    """Load a small TOML configuration file and reject unknown top-level keys."""

    with path.open("rb") as stream:
        raw = tomllib.load(stream)

    unknown = set(raw) - {"routing", "network"}
    if unknown:
        raise ValueError(
            f"unknown configuration section(s): {', '.join(sorted(unknown))}"
        )

    routing = raw.get("routing", {})
    network = raw.get("network", {})
    if not isinstance(routing, dict) or not isinstance(network, dict):
        raise ValueError("routing and network must be TOML tables")

    network_unknown = set(network) - {"allowed_hosts"}
    if network_unknown:
        raise ValueError(
            f"unknown network setting(s): {', '.join(sorted(network_unknown))}"
        )

    allowed_hosts = network.get("allowed_hosts", [])
    if not isinstance(allowed_hosts, list):
        raise ValueError("network.allowed_hosts must be an array")

    return AppConfig(task_routes=routing, allowed_hosts=frozenset(allowed_hosts))
