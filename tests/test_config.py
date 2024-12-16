import unittest
from netopia_sdk.config import Config

class TestConfig(unittest.TestCase):
    def test_valid_config(self):
        config = Config(
            api_key="test_api_key",
            pos_signature="test_pos_signature",
            is_live=False,
            notify_url="https://notify_url",
            redirect_url="https://redirect_url",
            public_key_str="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
            pos_signature_set=["test_pos_signature"]
        )
        self.assertEqual(config.api_key, "test_api_key")
        self.assertEqual(config.base_url, "https://secure-sandbox.netopia-payments.com")

    def test_invalid_config_missing_api_key(self):
        with self.assertRaises(ValueError):
            Config(
                api_key="",
                pos_signature="test_pos_signature",
                is_live=False,
                notify_url="https://notify_url",
                redirect_url="https://redirect_url",
                public_key_str="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
                pos_signature_set=["test_pos_signature"]
            )

if __name__ == '__main__':
    unittest.main()