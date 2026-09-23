import unittest
from datetime import datetime, timedelta, timezone

from resolveatlas.correlation import CandidateFeatures, score_candidate


class CorrelationTests(unittest.TestCase):
    def test_score_explains_matching_signals(self):
        now = datetime(2026, 1, 15, tzinfo=timezone.utc)
        seed = CandidateFeatures(
            "CASE-DEMO-001",
            "Scheduled scan results delayed",
            frozenset({"asset-inventory"}),
            frozenset({"ISSUE-DEMO-009"}),
            now,
        )
        candidate = CandidateFeatures(
            "CASE-DEMO-002",
            "Delayed scheduled scan processing",
            frozenset({"asset-inventory"}),
            frozenset({"ISSUE-DEMO-009"}),
            now - timedelta(days=2),
        )

        result = score_candidate(seed, candidate)

        self.assertGreater(result.score, 60)
        self.assertIn("1 shared reference(s)", result.reasons)
        self.assertIn("1 shared product tag(s)", result.reasons)

    def test_same_record_is_not_a_candidate(self):
        feature = CandidateFeatures(
            "CASE-DEMO-001",
            "Example issue",
            frozenset(),
            frozenset(),
            datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

        result = score_candidate(feature, feature)

        self.assertEqual(result.score, 0)
        self.assertEqual(result.reasons, ("same record",))

    def test_unrelated_old_record_has_no_matching_signals(self):
        seed = CandidateFeatures(
            "CASE-DEMO-001",
            "Scanner timeout",
            frozenset({"scanner"}),
            frozenset(),
            datetime(2026, 7, 1, tzinfo=timezone.utc),
        )
        candidate = CandidateFeatures(
            "CASE-DEMO-002",
            "Billing display mismatch",
            frozenset({"billing"}),
            frozenset(),
            datetime(2025, 1, 1, tzinfo=timezone.utc),
        )

        result = score_candidate(seed, candidate)

        self.assertEqual(result.score, 0)
        self.assertEqual(result.reasons, ("no matching signals",))


if __name__ == "__main__":
    unittest.main()
