from netopia_sdk.config import Config
from netopia_sdk.client import PaymentClient
from netopia_sdk.payment import PaymentService
from netopia_sdk.requests.models import (
    StartPaymentRequest, ConfigData, PaymentData, PaymentOptions, Instrument,
    OrderData, BillingData, ShippingData, ProductsData
)

# init configuration
config = Config(
    api_key="api_key",
    pos_signature="pos_signature",
    is_live=False,
    notify_url="https://notify_url",
    redirect_url="https://redirect_url",
    public_key_str="-----BEGIN CERTIFICATE-----CERTIFICATE-----END CERTIFICATE-----",
    pos_signature_set=["pos_signature"],
    private_key_str="-----BEGIN PRIVATE KEY-----PRIVATE_KEY-----END PRIVATE KEY-----"
)

# create client and service
client = PaymentClient(config)
payment_service = PaymentService(client)

# example request
start_payment_request = StartPaymentRequest(
    config=ConfigData(
        emailTemplate="default",
        emailSubject="Order Confirmation",
        cancelUrl="https://your_cancel_url",
        notifyUrl="https://your_notify_url",
        redirectUrl="https://your_redirect_url",
        language="ro",
    ),
    payment=PaymentData(
        options=PaymentOptions(installments=0, bonus=0),
        # You can collect the card details from the user and pass them here OR
        # set instrument=None to let Netopia handle the payment form
        instrument=Instrument(
            type="card",
            account="9900004810225098",
            expMonth=12,
            expYear=2050,
            secretCode="111",
            token="",
            clientID="",
        ),
        instrument=None,
        data={},
    ),
    order=OrderData(
        ntpID=None,
        posSignature=None,
        dateTime="2024-12-13T12:00:00Z",
        orderID="6122331273",
        description="Test order",
        amount=10.0,
        currency="RON",
        billing=BillingData(
            email="john.doe@example.com",
            phone="1234567890",
            firstName="John",
            lastName="Doe",
            city="Bucharest",
            country=1,
            countryName="Romania",
            state="Bucharest",
            postalCode="010101",
            details="Some details",
        ),
        shipping=ShippingData(
            email="john.doe@example.com",
            phone="1234567890",
            firstName="John",
            lastName="Doe",
            city="Bucharest",
            country=1,
            countryName="Romania",
            state="Bucharest",
            postalCode="010101",
            details="Some details",
        ),
        products=[
            ProductsData(
                name="Product1", code="P1", category="Category1", price=10.0, vat=0.0
            )
        ],
        installments={"selected": 0, "available": []},
        data={},
    ),
)

response = payment_service.start_payment(start_payment_request)
