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
)


class PaymentService:
    def __init__(self, client: PaymentClient):
        self.client = client
        self.transport = Transport(
            base_url=self.client.base_url(),
            api_key=self.client.config.api_key
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

    def verify_auth(self, auth_token: str, ntpID: str, pa_res: str) -> VerifyAuthResponse:
        request = PaymentVerifyAuthParam(
            authenticationToken=auth_token,
            ntpID=ntpID,
            formData={"paRes": pa_res},
        )

        endpoint = "/payment/card/verify-auth"
        return self.transport.send_request(endpoint, request, VerifyAuthResponse)
