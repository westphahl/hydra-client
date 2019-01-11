class HydraException(Exception):
    pass


class UnboundResourceError(HydraException):
    pass


class TransportError(HydraException):
    pass


class ConnectionError(TransportError):
    pass


class HTTPError(HydraException):
    pass


class BadRequest(HTTPError):
    pass


class Unauthorized(HTTPError):
    pass


class Forbidden(HTTPError):
    pass


class NotFound(HTTPError):
    pass


class ServerError(HTTPError):
    pass


status_map = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    500: ServerError,
}
