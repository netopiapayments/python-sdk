from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class ErrorDetails:
    code: str
    message: str
    field: str
    attributes: Dict[str, str]


@dataclass
class ErrorWithDetails:
    code: str
    message: str
    details: List[ErrorDetails]


@dataclass
class PaymentResponseData:
    method: Optional[str] = None
    allowedMethods: Optional[List[str]] = None
    ntpID: Optional[str] = None
    rrn: Optional[str] = None
    status: Optional[int] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    paymentURL: Optional[str] = None
    token: Optional[str] = None
    operationDate: Optional[str] = None
    options: Optional[Dict] = None
    binding: Optional[Dict] = None
    instrument: Optional[Dict] = None
    data: Optional[Dict[str, str]] = None


@dataclass
class ApiResponse:
    code: Optional[str] = None
    message: Optional[str] = None
    error: Optional[ErrorWithDetails] = None


@dataclass
class StartPaymentResponse(ApiResponse):
    payment: Optional[PaymentResponseData] = None
    customerAction: Optional[Dict] = None


@dataclass
class StatusResponse(ApiResponse):
    bnpl: Optional[Dict] = None
    merchant: Optional[Dict] = None
    config: Optional[Dict] = None
    order: Optional[Dict] = None
    payment: Optional[PaymentResponseData] = None
    customerAction: Optional[Dict] = None


@dataclass
class VerifyAuthResponse(ApiResponse):
    payment: Optional[PaymentResponseData] = None


@dataclass
class IpnVerifyResponse:
    errorType: int
    errorCode: Optional[int]
    errorMessage: Optional[str]
    status: Optional[int]
    message: Optional[str]
