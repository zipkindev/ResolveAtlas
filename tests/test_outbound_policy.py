import unittest

from resolveatlas.security import OutboundPolicy, OutboundPolicyError


class OutboundPolicyTests(unittest.TestCase):
    def test_allows_exact_https_host(self):
        policy = OutboundPolicy(frozenset({"jira.example.com"}))

        result = policy.validate("https://jira.example.com/api/issues?q=open")

        self.assertEqual(result, "https://jira.example.com/api/issues?q=open")

    def test_rejects_subdomain_confusion_and_embedded_credentials(self):
        policy = OutboundPolicy(frozenset({"jira.example.com"}))

        rejected = (
            "https://jira.example.com.attacker.example/api",
            "https://jira.example.com@attacker.example/api",
            "https://user:secret@jira.example.com/api",
        )
        for url in rejected:
            with self.subTest(url=url), self.assertRaises(OutboundPolicyError):
                policy.validate(url)

    def test_http_requires_explicit_loopback_configuration(self):
        default = OutboundPolicy(
            frozenset({"localhost"}), allowed_ports=frozenset({80})
        )
        local = OutboundPolicy(
            frozenset({"localhost"}),
            allow_http_loopback=True,
            allowed_ports=frozenset({80}),
        )

        with self.assertRaisesRegex(OutboundPolicyError, "plain HTTP"):
            default.validate("http://localhost/health")
        self.assertEqual(
            local.validate("http://localhost/health"), "http://localhost/health"
        )

    def test_rejects_unlisted_port(self):
        policy = OutboundPolicy(frozenset({"api.example.com"}))

        with self.assertRaisesRegex(OutboundPolicyError, "port"):
            policy.validate("https://api.example.com:8443/v1")


if __name__ == "__main__":
    unittest.main()
