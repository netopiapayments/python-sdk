class NetopiaError(Exception):
    pass


class InvalidOrderError(NetopiaError):
    pass


class MissingVerificationTokenError(NetopiaError):
    pass


class InvalidPublicKeyError(NetopiaError):
    pass


class InvalidIssuerError(NetopiaError):
    pass


class EmptyAudienceError(NetopiaError):
    pass


class InvalidAudienceError(NetopiaError):
    pass


class AudienceNotInSetError(NetopiaError):
    pass


class PayloadHashMismatchError(NetopiaError):
    pass


class InvalidTokenError(NetopiaError):
    pass


class MissingHashMethodError(NetopiaError):
    pass


class WrongVerificationTokenError(NetopiaError):
    pass


class UnexpectedSigningMethodError(NetopiaError):
    pass


class FailedPayloadParsingError(NetopiaError):
    pass


class UnsupportedHashMethodError(NetopiaError):
    pass
