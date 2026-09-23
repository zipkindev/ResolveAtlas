import tempfile
import unittest
from pathlib import Path

from scripts.audit_public_tree import audit


class PublicAuditTests(unittest.TestCase):
    def test_accepts_reserved_example_hosts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "example.toml").write_text(
                'endpoint = "https://jira.example.com/api"\n', encoding="utf-8"
            )
            self.assertEqual(audit(root), [])

    def test_reports_rule_and_path_without_secret_value(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "bad.txt").write_text(
                "-----BEGIN " + "PRIVATE KEY-----\nsensitive material\n",
                encoding="utf-8",
            )
            findings = audit(root)
            self.assertEqual(findings, [("private-key", "bad.txt")])
