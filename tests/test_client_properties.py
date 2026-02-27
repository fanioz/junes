"""Property-based tests for API client."""

from unittest import mock

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

import responses

from jules_cli.client import JulesAPIClient
from jules_cli.constants import BASE_URL, API_KEY_HEADER
from jules_cli.exceptions import ServerError


class TestAPIKeyHeaderInclusionProperty:
    """Property 4: API Key Header Inclusion (Requirements 1.6)"""

    @given(api_key=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=['L', 'N'], blacklist_characters='\x00')))
    @settings(max_examples=100)
    def test_api_key_header_always_included(self, api_key):
        """API key should always be included in request headers."""
        with responses.RequestsMock() as rsps:
            rsps.get(
                f"{BASE_URL}/test",
                json={"result": "success"},
                status=200,
            )

            client = JulesAPIClient(api_key=api_key, verbose=False)
            client._make_request("GET", "/test")

            assert len(rsps.calls) == 1
            assert rsps.calls[0].request.headers[API_KEY_HEADER] == api_key


class TestAPIErrorDisplayProperty:
    """Property 2: API Error Display (Requirements 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3)"""

    @given(
        status_code=st.sampled_from([401, 404, 429, 500, 503]),
        error_message=st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=['L', 'N'], blacklist_characters='\x00')),
    )
    @settings(max_examples=100)
    def test_api_errors_have_descriptive_messages(self, status_code, error_message):
        """All API error responses should have descriptive error messages."""
        with responses.RequestsMock() as rsps:
            rsps.get(
                f"{BASE_URL}/test",
                json={"error": error_message},
                status=status_code,
            )

            client = JulesAPIClient(api_key="test-key", verbose=False)

            try:
                client._make_request("GET", "/test")
                pytest.fail(f"Expected exception for status code {status_code}")
            except Exception as e:
                # Exception should have a message
                assert str(e)
                assert len(str(e)) > 0


class TestServerErrorHandlingProperty:
    """Property 9: Server Error Handling (Requirements 9.4)"""

    @given(status_code=st.sampled_from([500, 502, 503, 504]))
    @settings(max_examples=50)
    def test_all_5xx_codes_raise_server_error(self, status_code):
        """All 5xx status codes should raise ServerError."""
        with responses.RequestsMock() as rsps:
            rsps.get(
                f"{BASE_URL}/test",
                json={"error": "Server error"},
                status=status_code,
            )

            client = JulesAPIClient(api_key="test-key", verbose=False)

            with pytest.raises(ServerError):
                client._make_request("GET", "/test")


class TestVerboseHTTPLoggingProperty:
    """Property 16: Verbose HTTP Logging (Requirements 14.2, 14.3)"""

    @given(
        method=st.sampled_from(["GET", "POST"]),
        endpoint=st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=['L', 'N'], blacklist_characters='\x00')),
    )
    @settings(max_examples=100)
    def test_verbose_mode_logs_requests(self, method, endpoint):
        """Verbose mode should log HTTP request details."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                getattr(responses, method),
                f"{BASE_URL}/{endpoint}",
                json={"result": "success"},
                status=200,
            )

            with mock.patch("jules_cli.client.logger") as mock_logger:
                client = JulesAPIClient(api_key="test-key", verbose=True)
                client._make_request(method, f"/{endpoint}")

                # Logger should have been called
                assert mock_logger.debug.called
                # At least 2 calls (request + response)
                assert mock_logger.debug.call_count >= 2


class TestAPIKeyRedactionProperty:
    """Property 17: API Key Redaction (Requirements 14.4)"""

    @given(api_key=st.text(min_size=10, max_size=50, alphabet=st.characters(whitelist_categories=['L', 'N'])))
    @settings(max_examples=100)
    def test_api_key_redacted_in_logs(self, api_key):
        """API key should be redacted in verbose logs."""
        with responses.RequestsMock() as rsps:
            rsps.get(
                f"{BASE_URL}/test",
                json={"result": "success"},
                status=200,
            )

            with mock.patch("jules_cli.client.logger") as mock_logger:
                client = JulesAPIClient(api_key=api_key, verbose=True)
                client._make_request("GET", "/test")

                # Get all logged messages
                log_messages = [call.args[0] for call in mock_logger.debug.call_args_list]

                # None of the log messages should contain the full API key
                for msg in log_messages:
                    assert api_key not in str(msg), f"API key found in log: {msg}"
