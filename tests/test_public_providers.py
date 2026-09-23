import json
import unittest

from resolveatlas.core.models import EvidenceBundle, EvidenceItem, SourceReference
from resolveatlas.providers.base import GenerationRequest
from resolveatlas.providers.bedrock import BedrockProvider
from resolveatlas.providers.gemini import GeminiProvider


def _request():
    return GenerationRequest(
        task="case-summary",
        instructions="Summarize only supplied facts.",
        evidence=EvidenceBundle(
            subject_id="CASE-DEMO-001",
            subject_type="case",
            items=(
                EvidenceItem(
                    evidence_id="E-DEMO-001",
                    kind="note",
                    title="Synthetic note",
                    body="Fictional evidence.",
                    source=SourceReference("synthetic", "CASE-DEMO-001"),
                ),
            ),
        ),
    )


class PublicProviderTests(unittest.IsolatedAsyncioTestCase):
    async def test_gemini_uses_header_key_and_bounded_payload(self):
        captured = {}

        async def transport(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return {
                "candidates": [{"content": {"parts": [{"text": "See [E-DEMO-001]."}]}}],
                "usageMetadata": {"promptTokenCount": 12, "candidatesTokenCount": 4},
            }

        provider = GeminiProvider(
            api_key="test-only-key",
            default_model="gemini-test-model",
            transport=transport,
        )
        response = await provider.generate(_request())

        self.assertNotIn("test-only-key", captured["request"].full_url)
        self.assertEqual(captured["request"].headers["X-goog-api-key"], "test-only-key")
        body = json.loads(captured["request"].data)
        self.assertIn("[E-DEMO-001]", body["contents"][0]["parts"][0]["text"])
        self.assertEqual(response.usage["input_tokens"], 12)

    async def test_bedrock_uses_converse_and_explicit_model(self):
        class FakeClient:
            def __init__(self):
                self.arguments = None

            async def converse(self, **kwargs):
                self.arguments = kwargs
                return {
                    "output": {"message": {"content": [{"text": "See [E-DEMO-001]."}]}},
                    "usage": {"inputTokens": 8, "outputTokens": 3},
                }

        client = FakeClient()
        provider = BedrockProvider(client=client, default_model="bedrock-test-model")
        response = await provider.generate(_request())

        self.assertEqual(client.arguments["modelId"], "bedrock-test-model")
        self.assertIn(
            "[E-DEMO-001]", client.arguments["messages"][0]["content"][0]["text"]
        )
        self.assertEqual(response.provider, "bedrock")

    async def test_malformed_provider_response_fails_closed(self):
        provider = GeminiProvider(
            api_key="test-only-key",
            default_model="gemini-test-model",
            transport=self._empty_response,
        )
        with self.assertRaisesRegex(RuntimeError, "unexpected response shape"):
            await provider.generate(_request())

    @staticmethod
    async def _empty_response(request, timeout):
        return {}
