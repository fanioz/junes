"""Custom exception classes for Jules API errors."""


class JulesAPIError(Exception):
    """Base exception for all Jules API errors."""

    pass


class AuthenticationError(JulesAPIError):
    """Raised when authentication fails (invalid API key, token expired, etc.)."""

    pass


class ResourceNotFoundError(JulesAPIError):
    """Raised when a requested resource is not found (404)."""

    pass


class RateLimitError(JulesAPIError):
    """Raised when API rate limit is exceeded (429)."""

    pass


class ServerError(JulesAPIError):
    """Raised when the server returns an error (5xx)."""

    pass


class NetworkError(JulesAPIError):
    """Raised when a network error occurs (connection refused, timeout, etc.)."""

    pass


class ConfigurationError(JulesAPIError):
    """Raised when there is a configuration error."""

    pass
