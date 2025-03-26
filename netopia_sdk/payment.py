from .client import PaymentClient
from .transport import Transport
from .requests.models import (
    StartPaymentRequest,
    PaymentStatusParam,
    PaymentVerifyAuthParam,
)
from .responses.models import (
    StartPaymentResponse,
    StatusResponse,
    VerifyAuthResponse,
    IpnVerifyResponse
)

from .ipn import IpnVerifier


class PaymentService:
    def __init__(self, client: PaymentClient):
        self.client = client
        self.transport = Transport(
            base_url=self.client.base_url(),
            api_key=self.client.config.api_key
        )
        self.ipn_verifier = IpnVerifier(
            pos_signature=self.client.config.pos_signature,
            pos_signature_set=self.client.config.pos_signature_set,
            public_key_str=self.client.config.public_key_str,
            hash_method=self.client.config.hash_method,
            alg=self.client.config.alg,
        )

    def start_payment(self, request: StartPaymentRequest) -> StartPaymentResponse:
        if not request.order:
            raise ValueError("Order data cannot be None.")

        request.order.posSignature = self.client.config.pos_signature
        request.config.notifyUrl = self.client.config.notify_url
        request.config.redirectUrl = self.client.config.redirect_url
        request.config.language = request.config.language or "ro"

        endpoint = "/payment/card/start"
        return self.transport.send_request(endpoint, request, StartPaymentResponse)

    def get_status(self, ntpID: str, orderID: str) -> StatusResponse:
        request = PaymentStatusParam(
            posID=self.client.config.pos_signature,
            ntpID=ntpID,
            orderID=orderID,
        )

        endpoint = "/operation/status"
        return self.transport.send_request(endpoint, request, StatusResponse)

    def verify_auth(self, authenticationToken: str, ntpID: str, formData: dict) -> VerifyAuthResponse:
        request = PaymentVerifyAuthParam(
            authenticationToken=authenticationToken,
            ntpID=ntpID,
            formData=formData,
        )

        endpoint = "/payment/card/verify-auth"
        return self.transport.send_request(endpoint, request, VerifyAuthResponse)
    
    def verify_ipn(self, request) -> IpnVerifyResponse:
        verification_token = request.headers.get("Verification-token")
        raw_data = request.data.decode("utf-8")
        return self.ipn_verifier.verify(
            verification_token=verification_token,
            raw_data=raw_data
        )
