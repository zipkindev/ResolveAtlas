import unittest
from datetime import datetime, timezone

from resolveatlas.core import EvidenceBundle, EvidenceItem, SourceReference


class CoreModelTests(unittest.TestCase):
    def test_bundle_orders_items_and_freezes_metadata(self):
        source = SourceReference(
            system="demo",
            record_id="CASE-DEMO-001",
            captured_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        later = EvidenceItem("E-002", "comment", "Second", "Later evidence", source)
        earlier = EvidenceItem(
            "E-001",
            "description",
            "First",
            "Initial evidence",
            source,
            {"state": "open"},
        )

        bundle = EvidenceBundle("CASE-DEMO-001", "case", (later, earlier))

        self.assertEqual(
            [item.evidence_id for item in bundle.items], ["E-001", "E-002"]
        )
        with self.assertRaises(TypeError):
            earlier.metadata["state"] = "closed"  # type: ignore[index]

    def test_bundle_rejects_duplicate_evidence_ids(self):
        source = SourceReference("demo", "CASE-DEMO-001")
        first = EvidenceItem("E-001", "comment", "One", "First", source)
        second = EvidenceItem("E-001", "comment", "Two", "Second", source)

        with self.assertRaisesRegex(ValueError, "unique"):
            EvidenceBundle("CASE-DEMO-001", "case", (first, second))

    def test_source_requires_timezone_aware_capture(self):
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            SourceReference(
                "demo",
                "CASE-DEMO-001",
                captured_at=datetime(2026, 1, 1),
            )


if __name__ == "__main__":
    unittest.main()
