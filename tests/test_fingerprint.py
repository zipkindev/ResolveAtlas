import unittest
from datetime import datetime, timezone

from resolveatlas.core import (
    EvidenceBundle,
    EvidenceItem,
    SourceReference,
    fingerprint_bundle,
)


class FingerprintTests(unittest.TestCase):
    def test_fingerprint_is_order_independent_after_normalization(self):
        source = SourceReference(
            "demo",
            "CASE-DEMO-001",
            captured_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        first = EvidenceItem("E-001", "comment", "One", "First", source)
        second = EvidenceItem("E-002", "comment", "Two", "Second", source)

        left = EvidenceBundle("CASE-DEMO-001", "case", (first, second))
        right = EvidenceBundle("CASE-DEMO-001", "case", (second, first))

        self.assertEqual(fingerprint_bundle(left), fingerprint_bundle(right))

    def test_fingerprint_changes_with_evidence(self):
        source = SourceReference(
            "demo",
            "CASE-DEMO-001",
            captured_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        first = EvidenceBundle(
            "CASE-DEMO-001",
            "case",
            (EvidenceItem("E-001", "comment", "One", "First", source),),
        )
        changed = EvidenceBundle(
            "CASE-DEMO-001",
            "case",
            (EvidenceItem("E-001", "comment", "One", "Changed", source),),
        )

        self.assertNotEqual(fingerprint_bundle(first), fingerprint_bundle(changed))


if __name__ == "__main__":
    unittest.main()
