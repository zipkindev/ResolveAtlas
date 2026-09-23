import json
import unittest
from pathlib import Path

FIXTURE = Path(__file__).parent / "fixtures" / "synthetic" / "support_records.json"


class SyntheticFixtureTests(unittest.TestCase):
    def test_fixture_is_explicitly_synthetic_and_uses_demo_identifiers(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))

        self.assertEqual(data["fixture_kind"], "synthetic")
        identifiers = [case["id"] for case in data["cases"]]
        identifiers.extend(issue["id"] for issue in data["issues"])
        self.assertTrue(all("DEMO" in identifier for identifier in identifiers))

    def test_fixture_uses_reserved_example_domain(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))

        self.assertTrue(data["organization"]["domain"].endswith(".example.com"))


if __name__ == "__main__":
    unittest.main()
