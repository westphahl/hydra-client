class HydraException(Exception):
    pass


class UnboundResourceError(HydraException):
    pass


class HTTPError(HydraException):
    pass


class TransportError(HydraException):
    pass


class ConnectionError(TransportError):
    pass
