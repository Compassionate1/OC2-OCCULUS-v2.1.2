from __future__ import annotations

import unittest

from scripts.integration_smoke import _post_seed


class IntegrationSmokeValidationTests(unittest.TestCase):
    def test_rejects_remote_host(self) -> None:
        with self.assertRaises(ValueError):
            _post_seed("http://example.com:8088", "token")

    def test_rejects_https_scheme(self) -> None:
        with self.assertRaises(ValueError):
            _post_seed("https://127.0.0.1:8088", "token")

    def test_rejects_credentials(self) -> None:
        with self.assertRaises(ValueError):
            _post_seed("http://user:pass@127.0.0.1:8088", "token")


if __name__ == "__main__":
    unittest.main()
