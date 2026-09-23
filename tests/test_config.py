import tempfile
import unittest
from pathlib import Path

from resolveatlas.config import AppConfig, load_config


class ConfigTests(unittest.TestCase):
    def test_loads_explicit_routes_and_hosts(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "resolveatlas.toml")
            path.write_text(
                '[routing]\ncase-summary = "local-evidence"\n'
                '[network]\nallowed_hosts = ["api.example.com"]\n',
                encoding="utf-8",
            )
            config = load_config(path)

        self.assertEqual(config.task_routes["case-summary"], "local-evidence")
        self.assertEqual(config.allowed_hosts, frozenset({"api.example.com"}))

    def test_rejects_unknown_sections(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "resolveatlas.toml")
            path.write_text("[private]\nendpoint = 'hidden'\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown configuration"):
                load_config(path)

    def test_configuration_is_immutable(self):
        config = AppConfig({"case-summary": "local-evidence"})
        with self.assertRaises(TypeError):
            config.task_routes["case-summary"] = "elsewhere"
