import unittest

from resolveatlas.connectors.jira_cloud import JiraCloudConnector

ISSUE = {
    "key": "DEMO-9",
    "fields": {
        "summary": "Synthetic queue delay",
        "description": {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Fictional evidence."}],
                }
            ],
        },
        "status": {"name": "Investigating"},
        "updated": "2026-01-14T12:00:00Z",
        "comment": {
            "comments": [
                {
                    "id": "1001",
                    "body": {
                        "type": "doc",
                        "content": [{"type": "text", "text": "Synthetic comment."}],
                    },
                    "created": "2026-01-14T11:00:00Z",
                }
            ]
        },
    },
}


class JiraCloudConnectorTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.calls = []

        async def transport(method, url, payload):
            self.calls.append((method, url, payload))
            if url.endswith("/search/jql"):
                return {"issues": [ISSUE]}
            return ISSUE

        self.connector = JiraCloudConnector(
            base_url="https://jira.example.com",
            project_key="DEMO",
            transport=transport,
        )

    async def test_fetches_and_normalizes_adf_evidence(self):
        bundle = await self.connector.fetch_issue("DEMO-9")
        self.assertEqual(bundle.subject_id, "DEMO-9")
        self.assertEqual(len(bundle.items), 2)
        self.assertTrue(
            any("Fictional evidence." in item.body for item in bundle.items)
        )
        self.assertEqual(self.calls[0][0], "GET")

    async def test_search_scopes_jql_to_configured_project(self):
        bundles = await self.connector.search_issues("status != Done", limit=10)
        payload = self.calls[0][2]
        self.assertEqual(len(bundles), 1)
        self.assertEqual(payload["jql"], 'project = "DEMO" AND (status != Done)')
        self.assertEqual(payload["maxResults"], 10)

    async def test_rejects_cross_project_keys_and_unbounded_limits(self):
        with self.assertRaisesRegex(ValueError, "configured project"):
            await self.connector.fetch_issue("OTHER-1")
        with self.assertRaisesRegex(ValueError, "between 1 and 100"):
            await self.connector.search_issues("status != Done", limit=101)

    def test_rejects_base_url_paths(self):
        async def transport(method, url, payload):
            return {}

        with self.assertRaisesRegex(ValueError, "HTTPS origin"):
            JiraCloudConnector(
                base_url="https://jira.example.com/private/path",
                project_key="DEMO",
                transport=transport,
            )
