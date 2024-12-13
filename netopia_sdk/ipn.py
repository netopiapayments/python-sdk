import json
import base64
import hashlib
from typing import Optional
from jwt import decode, PyJWKClient, InvalidTokenError, InvalidSignatureError
from .constants import ErrorType, ErrorCode, PaymentStatus
from .errors import (
    MissingVerificationTokenError,
    WrongVerificationTokenError,
    InvalidIssuerError,
    EmptyAudienceError,
    InvalidAudienceError,
    AudienceNotInSetError,
    PayloadHashMismatchError,
    MissingHashMethodError,
    UnsupportedHashMethodError
)
from responses.models import IpnVerifyResponse

class IpnVerifier:
    def __init__(self, pos_signature: str, pos_signature_set: list, public_key_str: str, hash_method: str = "sha512", alg: str = "RS512"):
        self.pos_signature = pos_signature
        self.pos_signature_set = set(pos_signature_set)
        self.public_key_str = public_key_str
        self.hash_method = hash_method or "sha512"
        self.alg = alg or "RS512"

    def verify(self, verification_token: str, raw_data: str) -> IpnVerifyResponse:
        output = IpnVerifyResponse(
            errorType=ErrorType.ERROR_TYPE_NONE,
            errorCode=None,
            errorMessage=None,
            status=None,
            message=None
        )

        if not verification_token:
            raise MissingVerificationTokenError("Missing Verification-token header")

        parts = verification_token.split('.')
        if len(parts) != 3:
            raise WrongVerificationTokenError("Wrong_Verification_Token")

        try:
            header_bytes = base64.urlsafe_b64decode(self._pad_base64(parts[0]))
            header = json.loads(header_bytes)
        except Exception:
            raise WrongVerificationTokenError("Wrong token header")

        if header.get("typ") != "JWT":
            raise WrongVerificationTokenError("Wrong_Token_Type")

        if not self.public_key_str:
            return output

        jwt_algorithm = header.get("alg", self.alg)

        if not self.hash_method:
            raise MissingHashMethodError("Hash method missing")

        try:
            decoded = decode(
                verification_token,
                key=self.public_key_str,
                algorithms=[jwt_algorithm],
                options={"verify_aud": False, "verify_iss": False}
            )

            if decoded.get("iss") != "NETOPIA Payments":
                raise InvalidIssuerError("Invalid Issuer")

            aud = decoded.get("aud")
            if not aud:
                raise EmptyAudienceError("Empty Audience in token")

            actual_aud = aud[0] if isinstance(aud, list) else aud

            if actual_aud != self.pos_signature:
                raise InvalidAudienceError("Invalid audience")

            if actual_aud not in self.pos_signature_set:
                raise AudienceNotInSetError("Audience not in posSignatureSet")

            payload_hash = self._compute_hash(raw_data)
            if payload_hash != decoded.get("sub"):
                raise PayloadHashMismatchError("Payload hash mismatch")

            obj_ipn = json.loads(raw_data)
            status = obj_ipn["payment"]["status"]
            message = self._status_message(status)

            output.status = status
            output.message = message
            # No error
            return output

        except (InvalidTokenError, InvalidSignatureError, KeyError, ValueError) as e:
            return IpnVerifyResponse(
                errorType=ErrorType.ERROR_TYPE_PERMANENT,
                errorCode=ErrorCode.E_VERIFICATION_FAILED_GENERAL,
                errorMessage=str(e),
                status=None,
                message=None
            )
        except (
            InvalidIssuerError,
            EmptyAudienceError,
            InvalidAudienceError,
            AudienceNotInSetError,
            PayloadHashMismatchError,
            MissingHashMethodError,
            UnsupportedHashMethodError
        ) as e:
            return IpnVerifyResponse(
                errorType=ErrorType.ERROR_TYPE_PERMANENT,
                errorCode=ErrorCode.E_VERIFICATION_FAILED_GENERAL,
                errorMessage=str(e),
                status=None,
                message=None
            )

    def _compute_hash(self, data: str) -> str:
        if self.hash_method.lower() == "sha512":
            h = hashlib.sha512(data.encode('utf-8')).digest()
            return base64.b64encode(h).decode('utf-8')
        else:
            raise UnsupportedHashMethodError("Unsupported hash method")

    def _status_message(self, status: int) -> str:
        if status in [PaymentStatus.STATUS_NEW, PaymentStatus.STATUS_PAID, PaymentStatus.STATUS_CONFIRMED]:
            return "payment was confirmed; deliver goods"
        elif status == PaymentStatus.STATUS_CREDIT:
            return "a previously confirmed payment was refunded; cancel goods delivery"
        elif status == PaymentStatus.STATUS_CANCELED:
            return "payment was cancelled; do not deliver goods"
        elif status == PaymentStatus.STATUS_PENDING_AUTH:
            return "update payment status, last modified date&time in your system"
        elif status == PaymentStatus.STATUS_FRAUD:
            return "payment in reviewing"
        else:
            return "no specific action"

    @staticmethod
    def _pad_base64(b64_str: str) -> str:
        return b64_str + '=' * ((4 - len(b64_str) % 4) % 4)