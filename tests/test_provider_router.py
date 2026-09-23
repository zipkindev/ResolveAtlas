import unittest

from resolveatlas.core.models import EvidenceBundle, EvidenceItem, SourceReference
from resolveatlas.providers.base import GenerationRequest
from resolveatlas.providers.local import LocalEvidenceProvider
from resolveatlas.providers.router import ProviderRouter


def _request(task="case-summary"):
    bundle = EvidenceBundle(
        subject_id="CASE-DEMO-001",
        subject_type="case",
        items=(
            EvidenceItem(
                evidence_id="E-DEMO-001",
                kind="note",
                title="Synthetic note",
                body="A fictional worker waited for capacity.",
                source=SourceReference("synthetic", "CASE-DEMO-001"),
            ),
        ),
    )
    return GenerationRequest(
        task=task, instructions="Organize evidence.", evidence=bundle
    )


class ProviderRouterTests(unittest.IsolatedAsyncioTestCase):
    async def test_routes_to_explicit_provider_and_preserves_citations(self):
        provider = LocalEvidenceProvider()
        router = ProviderRouter(
            {provider.provider_id: provider}, {"case-summary": provider.provider_id}
        )

        response = await router.generate(_request())

        self.assertEqual(response.provider, "local-evidence")
        self.assertIn("[E-DEMO-001]", response.text)

    async def test_has_no_implicit_fallback(self):
        provider = LocalEvidenceProvider()
        router = ProviderRouter({provider.provider_id: provider}, {})
        with self.assertRaisesRegex(LookupError, "no provider route"):
            await router.generate(_request("unconfigured-task"))

    def test_rejects_unregistered_provider_route(self):
        with self.assertRaisesRegex(ValueError, "unregistered provider"):
            ProviderRouter({}, {"case-summary": "missing"})
