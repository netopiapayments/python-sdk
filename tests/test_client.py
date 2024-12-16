import unittest
from netopia_sdk.config import Config
from netopia_sdk.client import PaymentClient
from netopia_sdk.logger import logger as default_logger

class TestPaymentClient(unittest.TestCase):
    def setUp(self):
        self.config = Config(
            api_key="test_api_key",
            pos_signature="test_pos_signature",
            is_live=False,
            notify_url="https://notify_url",
            redirect_url="https://redirect_url",
            public_key_str="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
            pos_signature_set=["test_pos_signature"]
        )
        self.client = PaymentClient(self.config)

    def test_get_logger_default(self):
        logger = self.client.get_logger()
        self.assertIs(logger, default_logger)

    def test_get_logger_custom(self):
        custom_logger = default_logger.getChild("custom")
        client_with_custom_logger = PaymentClient(self.config, logger_instance=custom_logger)
        self.assertIs(client_with_custom_logger.get_logger(), custom_logger)

    def test_base_url_for_sandbox(self):
        self.assertEqual(self.client.base_url(), "https://secure-sandbox.netopia-payments.com")

    def test_base_url_for_live(self):
        self.config.is_live = True
        self.client = PaymentClient(self.config)
        self.assertEqual(self.client.base_url(), "https://secure.netopia-payments.com")

    def test_invalid_config_raises_value_error(self):
        with self.assertRaises(ValueError):
            PaymentClient(None)

if __name__ == '__main__':
    unittest.main()