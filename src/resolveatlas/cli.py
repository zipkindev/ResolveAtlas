"""Small offline-first command line interface."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from resolveatlas.analysis import analyze_bundle
from resolveatlas.connectors.synthetic import SyntheticSupportConnector
from resolveatlas.providers.local import LocalEvidenceProvider
from resolveatlas.providers.router import ProviderRouter


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="resolveatlas")
    parser.add_argument(
        "--fixture", type=Path, required=True, help="path to a synthetic fixture"
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    analyze = subcommands.add_parser(
        "analyze-case", help="render a source-linked offline digest"
    )
    analyze.add_argument("case_id")
    return parser


async def _run(args: argparse.Namespace) -> int:
    connector = SyntheticSupportConnector(args.fixture)
    provider = LocalEvidenceProvider()
    router = ProviderRouter(
        {provider.provider_id: provider}, {"case-summary": provider.provider_id}
    )
    bundle = await connector.fetch_case(args.case_id)
    result = await analyze_bundle(
        bundle,
        task="case-summary",
        instructions="Organize the supplied evidence without adding facts.",
        router=router,
    )
    print(result.response.text)
    print(f"Evidence fingerprint: {result.fingerprint}")
    return 0


def main() -> int:
    return asyncio.run(_run(_parser().parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
