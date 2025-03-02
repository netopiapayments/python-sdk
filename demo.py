from netopia_sdk.config import Config
from netopia_sdk.client import PaymentClient
from netopia_sdk.payment import PaymentService, PaymentSession
from netopia_sdk.requests.models import (
    StartPaymentRequest, ConfigData, PaymentData, PaymentOptions, Instrument,
    OrderData, BillingData, ShippingData, ProductsData
)

# init configuration
config = Config(
    api_key="YOUR_API_KEY",
    pos_signature="POS_SIGNATURE",
    is_live=False,
    notify_url="https://your_notify_url",
    redirect_url="https://your_redirect_url",
    public_key_str="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
    pos_signature_set=["POS_SIGNATURE"],
)

# Create client, service and session
client = PaymentClient(config)
payment_service = PaymentService(client)
payment_session = PaymentSession()

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
        instrument=Instrument(
            type="card",
            account="4111111111111111",
            expMonth=12,
            expYear=2050,
            secretCode="123",
            token="",
            clientID="",
        ),
        data={},
    ),
    order=OrderData(
        ntpID=None,
        posSignature=None,
        dateTime="2024-12-13T12:00:00Z",
        orderID=payment_session.order_id,
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

# ✅ Start Payment
response = payment_service.start_payment(start_payment_request)
print("\nStart Payment Response:", response)

# ✅ Salvare variabile în obiectul payment_session
payment_session.ntp_id = response.payment.get('ntpID')
payment_session.auth_token = response.payment.get('data', {}).get('AuthCode')

# ✅ Get Payment Status
response = payment_service.get_status(
    ntpID=payment_session.ntp_id,
    orderID=payment_session.order_id)

print("\nOrder Status Response:", response)

# ✅ Verify Auth
response = payment_service.verify_auth(
    authenticationToken=payment_session.auth_token,
    ntpID=payment_session.ntp_id,
)
print("\nVerifyAuth Response:", response)
