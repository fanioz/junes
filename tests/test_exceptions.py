"""Tests for custom exception classes."""

import pytest

from jules_cli.exceptions import (
    JulesAPIError,
    AuthenticationError,
    ResourceNotFoundError,
    RateLimitError,
    ServerError,
    NetworkError,
    ConfigurationError,
)


class TestJulesAPIError:
    """Tests for the base JulesAPIError exception."""

    def test_is_base_exception(self):
        """JulesAPIError should inherit from Exception."""
        assert issubclass(JulesAPIError, Exception)

    def test_can_be_instantiated_with_message(self):
        """JulesAPIError should accept a message parameter."""
        error = JulesAPIError("Test error message")
        assert str(error) == "Test error message"
        assert error.args == ("Test error message",)

    def test_can_be_instantiated_without_message(self):
        """JulesAPIError should work without a message."""
        error = JulesAPIError()
        assert str(error) == ""
        assert error.args == ()


class TestAuthenticationError:
    """Tests for AuthenticationError exception."""

    def test_inherits_from_jules_api_error(self):
        """AuthenticationError should inherit from JulesAPIError."""
        assert issubclass(AuthenticationError, JulesAPIError)

    def test_can_be_instantiated_with_message(self):
        """AuthenticationError should accept a message parameter."""
        error = AuthenticationError("Invalid API key")
        assert str(error) == "Invalid API key"
        assert isinstance(error, JulesAPIError)


class TestResourceNotFoundError:
    """Tests for ResourceNotFoundError exception."""

    def test_inherits_from_jules_api_error(self):
        """ResourceNotFoundError should inherit from JulesAPIError."""
        assert issubclass(ResourceNotFoundError, JulesAPIError)

    def test_can_be_instantiated_with_message(self):
        """ResourceNotFoundError should accept a message parameter."""
        error = ResourceNotFoundError("Session not found")
        assert str(error) == "Session not found"
        assert isinstance(error, JulesAPIError)


class TestRateLimitError:
    """Tests for RateLimitError exception."""

    def test_inherits_from_jules_api_error(self):
        """RateLimitError should inherit from JulesAPIError."""
        assert issubclass(RateLimitError, JulesAPIError)

    def test_can_be_instantiated_with_message(self):
        """RateLimitError should accept a message parameter."""
        error = RateLimitError("Rate limit exceeded")
        assert str(error) == "Rate limit exceeded"
        assert isinstance(error, JulesAPIError)


class TestServerError:
    """Tests for ServerError exception."""

    def test_inherits_from_jules_api_error(self):
        """ServerError should inherit from JulesAPIError."""
        assert issubclass(ServerError, JulesAPIError)

    def test_can_be_instantiated_with_message(self):
        """ServerError should accept a message parameter."""
        error = ServerError("Internal server error")
        assert str(error) == "Internal server error"
        assert isinstance(error, JulesAPIError)


class TestNetworkError:
    """Tests for NetworkError exception."""

    def test_inherits_from_jules_api_error(self):
        """NetworkError should inherit from JulesAPIError."""
        assert issubclass(NetworkError, JulesAPIError)

    def test_can_be_instantiated_with_message(self):
        """NetworkError should accept a message parameter."""
        error = NetworkError("Connection failed")
        assert str(error) == "Connection failed"
        assert isinstance(error, JulesAPIError)


class TestConfigurationError:
    """Tests for ConfigurationError exception."""

    def test_inherits_from_jules_api_error(self):
        """ConfigurationError should inherit from JulesAPIError."""
        assert issubclass(ConfigurationError, JulesAPIError)

    def test_can_be_instantiated_with_message(self):
        """ConfigurationError should accept a message parameter."""
        error = ConfigurationError("Invalid configuration")
        assert str(error) == "Invalid configuration"
        assert isinstance(error, JulesAPIError)


class TestExceptionCatchability:
    """Tests that exceptions can be caught by their base types."""

    def test_all_exceptions_catchable_by_jules_api_error(self):
        """All custom exceptions should be catchable by JulesAPIError."""
        exceptions = [
            AuthenticationError(),
            ResourceNotFoundError(),
            RateLimitError(),
            ServerError(),
            NetworkError(),
            ConfigurationError(),
        ]

        for exc in exceptions:
            try:
                raise exc
            except JulesAPIError:
                pass  # Expected
            else:
                pytest.fail(f"{type(exc).__name__} should be catchable by JulesAPIError")
