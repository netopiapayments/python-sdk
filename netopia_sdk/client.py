from .config import Config
from .logger import logger


class PaymentClient:
    def __init__(self, config: Config, logger_instance=None):
        if not config:
            raise ValueError("Config cannot be None.")
        self.config = config
        self.logger = logger_instance or logger

    def get_logger(self):
        return self.logger

    def base_url(self) -> str:
        return self.config.base_url
