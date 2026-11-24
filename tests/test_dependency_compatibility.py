"""Offline transport checks: no real credentials, contacts or outbound requests."""
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests
import resend
from dotenv import dotenv_values, set_key
from requests.adapters import HTTPAdapter
from PIL import Image


class DependencyCompatibilityTests(unittest.TestCase):
    def test_image_decoders_preserve_dimensions(self):
        for format_name in ("PNG", "JPEG", "TIFF"):
            with self.subTest(format=format_name):
                stream = io.BytesIO()
                Image.new("RGB", (12, 8), (80, 120, 160)).save(stream, format=format_name)
                stream.seek(0)
                with Image.open(stream) as decoded:
                    decoded.load()
                    self.assertEqual(decoded.size, (12, 8))

    def test_main_streamlit_page_renders_without_network(self):
        from streamlit.testing.v1 import AppTest

        with patch("socket.socket.connect", side_effect=AssertionError("Network disabled")):
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "streamlit_app.py")).run(timeout=30)
            self.assertFalse(app.exception, [item.message for item in app.exception])
            self.assertEqual(len(app.metric), 5)

    def test_tls_verification_gets_a_distinct_pool_configuration(self):
        request = requests.Request("GET", "https://example.invalid/").prepare()
        adapter = HTTPAdapter()
        _, verified = adapter.build_connection_pool_key_attributes(request, True)
        _, unverified = adapter.build_connection_pool_key_attributes(request, False)
        self.assertNotEqual(verified, unverified)
        self.assertEqual(verified["cert_reqs"], "CERT_REQUIRED")
        self.assertEqual(unverified["cert_reqs"], "CERT_NONE")

    def test_dotenv_does_not_overwrite_a_symlink_target(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "original.env"
            target.write_text("VALUE=original\n", encoding="utf-8")
            link = Path(directory) / ".env"
            link.symlink_to(target)
            set_key(link, "VALUE", "updated")
            self.assertEqual(target.read_text(encoding="utf-8"), "VALUE=original\n")
            self.assertEqual(dotenv_values(link)["VALUE"], "updated")

    def test_real_resend_sdk_preserves_payload_and_response_contract(self):
        captured = []

        class OfflineTransport:
            def request(self, **kwargs):
                captured.append(kwargs)
                return json.dumps({"id": "synthetic-id"}), 200, {"content-type": "application/json"}

        with patch.dict(os.environ, {"RESEND_API_KEY": "re_synthetic_test_only", "SENDER_EMAIL": "sender@example.invalid"}, clear=True), \
             patch("dotenv.load_dotenv"), \
             patch("socket.socket.connect", side_effect=AssertionError("Network disabled")), \
             patch.object(resend, "default_http_client", OfflineTransport()):
            from automated_email_sender import SBSEmailAutomation

            client = SBSEmailAutomation()
            self.assertTrue(client.send_via_resend("recipient@example.invalid", "Synthetic", "Line one\nLine two"))

        self.assertEqual(len(captured), 1)
        request = captured[0]
        self.assertEqual(request["method"].lower(), "post")
        self.assertEqual(request["url"], "https://api.resend.com/emails")
        self.assertEqual(request["json"]["to"], ["recipient@example.invalid"])
        self.assertEqual(request["json"]["reply_to"], "sender@example.invalid")
        self.assertEqual(request["json"]["html"], "Line one<br>Line two")

    def test_real_resend_sdk_rejects_provider_failure(self):
        class OfflineTransport:
            def request(self, **kwargs):
                return json.dumps({"message": "Synthetic failure", "name": "validation_error"}), 422, {"content-type": "application/json"}

        with patch.dict(os.environ, {"RESEND_API_KEY": "re_synthetic_test_only", "SENDER_EMAIL": "sender@example.invalid"}, clear=True), \
             patch("socket.socket.connect", side_effect=AssertionError("Network disabled")), \
             patch.object(resend, "default_http_client", OfflineTransport()):
            from automated_email_sender import SBSEmailAutomation

            self.assertFalse(SBSEmailAutomation().send_via_resend("recipient@example.invalid", "Synthetic", "Text"))


if __name__ == "__main__":
    unittest.main()
