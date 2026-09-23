#!/usr/bin/env python3
"""Conservative, value-suppressing checks for a ResolveAtlas candidate tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKIP_PARTS = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__"}
TEXT_SUFFIXES = {
    "",
    ".cff",
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
RULES = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws-access-key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "github-token": re.compile(r"\bgh[opsu]_[A-Za-z0-9_]{30,}\b"),
    "non-example-http-host": re.compile(
        r"https?://(?!localhost(?=[:/\s'\"])|127\.0\.0\.1(?=[:/\s'\"])|www\.apache\.org(?=[:/\s'\"])|generativelanguage\.googleapis\.com(?=[:/\s'\"])|[^/]*\.example(?:\.com|\.org|\.net)?(?=[:/\s'\"]))[^\s'\"]+",
        re.IGNORECASE,
    ),
}


def audit(root: Path) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() not in TEXT_SUFFIXES:
            findings.append(("unreviewed-binary", relative))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(("non-utf8-file", relative))
            continue
        if relative == "scripts/audit_public_tree.py":
            continue
        for rule, pattern in RULES.items():
            if pattern.search(text):
                findings.append((rule, relative))
    return findings


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings = audit(root)
    for rule, path in findings:
        print(f"blocker\t{rule}\t{path}")
    print(f"summary\tblockers={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
