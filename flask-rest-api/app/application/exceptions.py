class ApplicationError(Exception):
    """Base class for errors raised by use cases.

    Use cases raise these instead of returning HTTP status codes, so they
    stay framework-agnostic; the interfaces/http layer maps them to
    responses.
    """


class ValidationError(ApplicationError):
    pass


class NotFoundError(ApplicationError):
    pass


class ConflictError(ApplicationError):
    pass


class AuthenticationError(ApplicationError):
    pass
