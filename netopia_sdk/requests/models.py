from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class PaymentOptions:
    installments: int
    bonus: int
    split: List[Dict[str, float]] = field(default_factory=list)


@dataclass
class Instrument:
    type: str
    account: str
    expMonth: int
    expYear: int
    secretCode: str
    token: str
    clientID: str


@dataclass
class PaymentData:
    options: PaymentOptions
    instrument: Optional[Instrument] 
    data: Dict[str, str]


@dataclass
class BillingData:
    email: str
    phone: str
    firstName: str
    lastName: str
    city: str
    country: int
    countryName: str
    state: str
    postalCode: str
    details: str


@dataclass
class ShippingData:
    email: str
    phone: str
    firstName: str
    lastName: str
    city: str
    country: int
    countryName: str
    state: str
    postalCode: str
    details: str


@dataclass
class ProductsData:
    name: str
    code: str
    category: str
    price: float
    vat: float


@dataclass
class OrderData:
    ntpID: Optional[str]
    posSignature: Optional[str]
    dateTime: str
    orderID: str
    description: str
    amount: float
    currency: str
    billing: BillingData
    shipping: ShippingData
    products: List[ProductsData]
    installments: Dict[str, object]
    data: Dict[str, str]


@dataclass
class ConfigData:
    emailTemplate: str
    emailSubject: str
    cancelUrl: str
    notifyUrl: str
    redirectUrl: str
    language: str


@dataclass
class StartPaymentRequest:
    config: ConfigData
    payment: PaymentData
    order: OrderData


@dataclass
class PaymentStatusParam:
    posID: str
    ntpID: str
    orderID: str


@dataclass
class PaymentVerifyAuthParam:
    authenticationToken: str
    ntpID: str
    formData: Dict[str, str]


@dataclass
class IpnParams:
    posSignature: str
    posSignatureSet: List[str]
    hashMethod: Optional[str]
    alg: Optional[str]
    publicKeyStr: str
