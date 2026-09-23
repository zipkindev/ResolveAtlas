import unittest
from datetime import datetime, timezone

from resolveatlas.core.attachments import TextAttachmentPolicy


class AttachmentPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = TextAttachmentPolicy(max_bytes=20)

    def normalize(self, content=b"synthetic note"):
        return self.policy.normalize(
            filename="demo.txt",
            media_type="text/plain",
            content=content,
            source_system="synthetic",
            source_record_id="CASE-DEMO-001",
            captured_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

    def test_normalizes_text_with_hash_and_size(self):
        item = self.normalize()
        self.assertEqual(item.metadata["size_bytes"], "14")
        self.assertEqual(len(item.metadata["sha256"]), 64)

    def test_rejects_paths_binary_content_and_size_overflow(self):
        with self.assertRaisesRegex(ValueError, "single safe path"):
            self.policy.normalize(
                filename="../demo.txt",
                media_type="text/plain",
                content=b"safe",
                source_system="synthetic",
                source_record_id="CASE-DEMO-001",
                captured_at=datetime.now(timezone.utc),
            )
        with self.assertRaisesRegex(ValueError, "null byte"):
            self.normalize(b"bad\x00text")
        with self.assertRaisesRegex(ValueError, "byte limit"):
            self.normalize(b"x" * 21)
