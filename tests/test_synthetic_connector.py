import unittest
from pathlib import Path

from resolveatlas.connectors.synthetic import SyntheticSupportConnector

FIXTURE = Path(__file__).parent / "fixtures" / "synthetic" / "support_records.json"


class SyntheticConnectorTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.connector = SyntheticSupportConnector(FIXTURE)

    async def test_fetch_case_builds_traceable_evidence(self):
        bundle = await self.connector.fetch_case("CASE-DEMO-001")
        self.assertEqual(bundle.subject_type, "case")
        self.assertEqual(len(bundle.items), 2)
        self.assertTrue(
            all(item.source.locator.startswith("synthetic://") for item in bundle.items)
        )

    async def test_fetch_issue_builds_traceable_evidence(self):
        bundle = await self.connector.fetch_issue("ISSUE-DEMO-009")
        self.assertEqual(bundle.subject_type, "issue")
        self.assertEqual(bundle.metadata["project"], "DEMO")

    async def test_search_is_bounded(self):
        results = await self.connector.search_cases("inventory", limit=1)
        self.assertEqual(len(results), 1)

    async def test_unknown_record_fails_closed(self):
        with self.assertRaisesRegex(LookupError, "not found"):
            await self.connector.fetch_case("CASE-DEMO-404")
