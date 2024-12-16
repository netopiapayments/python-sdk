import re
from typing import List


class Config:
    def __init__(
        self,
        api_key: str,
        pos_signature: str,
        is_live: bool,
        notify_url: str,
        redirect_url: str,
        public_key_str: str,
        pos_signature_set: List[str],
        hash_method: str = "sha512",
        alg: str = "RS512",
    ):
        self.api_key = api_key
        self.pos_signature = pos_signature
        self.is_live = is_live
        self.notify_url = notify_url
        self.redirect_url = redirect_url
        self.public_key_str = public_key_str
        self.pos_signature_set = pos_signature_set
        self.hash_method = hash_method
        self.alg = alg

        self.validate()

    def validate(self):
        if not self.api_key:
            raise ValueError("Missing apiKey")
        if not self.pos_signature:
            raise ValueError("Missing posSignature")
        if not self.pos_signature_set:
            raise ValueError("posSignatureSet must not be empty")
        if not self.notify_url or not self.redirect_url:
            raise ValueError("Both notifyURL and redirectURL must be set")
        if not self.public_key_str:
            raise ValueError("PublicKey must be provided")
        if not self._is_valid_url(self.notify_url):
            raise ValueError("notifyUrl is invalid")
        if not self._is_valid_url(self.redirect_url):
            raise ValueError("redirectUrl is invalid")

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        pattern = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'[^ ]+$'  # One or more chars (no spaces)
        )
        return bool(pattern.match(url))

    @property
    def base_url(self) -> str:
        return (
            "https://secure.netopia-payments.com"
            if self.is_live
            else "https://secure-sandbox.netopia-payments.com"
        )
