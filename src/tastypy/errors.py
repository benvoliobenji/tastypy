# https://developer.tastytrade.com/api-overview/#api-overview - Error Codes


class InvalidRequestError(Exception):
    """Exception raised for invalid requests to the API."""

    code = 400

    def __init__(self, message):
        self.message = f"Code: {self.code} -  Invalid request from API (probably invalid parameters) {message}"
        super().__init__(self.message)


class AuthorizationExpiredError(Exception):
    """Exception raised for expired authorization."""

    code = 401

    def __init__(self, message):
        self.message = f"Code: {self.code} -  Authorization expired (try logging in again) {message}"
        super().__init__(self.message)


class UnauthorizedError(Exception):
    """Exception raised for unauthorized access."""

    code = 403

    def __init__(self, message):
        self.message = f"Code: {self.code} -  Unauthorized access (might be accessing the wrong account with the wrong customer) {message}"
        super().__init__(self.message)


class NotFoundError(Exception):
    """Exception raised for not found errors."""

    code = 404

    def __init__(self, message):
        self.message = f"Code: {self.code} -  Not found (data may not exist) {message}"
        super().__init__(self.message)


class UnprocessableContentError(Exception):
    """Exception raised for unprocessable content errors."""

    code = 422

    def __init__(self, message):
        self.message = f"Code: {self.code} -  Unprocessable content (invalid action performed) {message}"
        super().__init__(self.message)


class TooManyRequestsError(Exception):
    """Exception raised for too many requests."""

    code = 429

    def __init__(self, message):
        self.message = (
            f"Code: {self.code} -  Too many requests (rate limit exceeded) {message}"
        )
        super().__init__(self.message)


class InternalServerError(Exception):
    """Exception raised for internal server errors."""

    code = 500

    def __init__(self, message):
        self.message = (
            f"Code: {self.code} -  Internal server error (try again later) {message}"
        )
        super().__init__(self.message)


__all_errors = {
    400: InvalidRequestError,
    401: AuthorizationExpiredError,
    403: UnauthorizedError,
    404: NotFoundError,
    422: UnprocessableContentError,
    429: TooManyRequestsError,
    500: InternalServerError,
}


def translate_error_code(code: int, message: str) -> Exception:
    """
    Translate error codes to exceptions.
    """
    if code in __all_errors:
        return __all_errors[code](message)
    return Exception(f"Unknown error: {message}")
