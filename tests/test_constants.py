"""Tests for API constants."""


from junes.constants import (
    BASE_URL,
    API_KEY_HEADER,
    CONTENT_TYPE_HEADER,
    SOURCES_ENDPOINT,
    SESSIONS_ENDPOINT,
    SESSION_DETAIL_ENDPOINT,
    SESSION_DELETE_ENDPOINT,
    SESSION_APPROVE_ENDPOINT,
    ACTIVITIES_ENDPOINT,
    MESSAGES_ENDPOINT,
)


class TestBaseURL:
    """Tests for the base URL constant."""

    def test_base_url_is_defined(self):
        """BASE_URL should be defined."""
        assert BASE_URL is not None

    def test_base_url_is_string(self):
        """BASE_URL should be a string."""
        assert isinstance(BASE_URL, str)

    def test_base_url_format(self):
        """BASE_URL should be a valid URL format."""
        assert BASE_URL.startswith("https://")
        assert "/v1" in BASE_URL


class TestHeaders:
    """Tests for header constants."""

    def test_api_key_header(self):
        """API_KEY_HEADER should be 'x-goog-api-key'."""
        assert API_KEY_HEADER == "x-goog-api-key"

    def test_content_type_header(self):
        """CONTENT_TYPE_HEADER should be 'content-type'."""
        assert CONTENT_TYPE_HEADER == "content-type"


class TestEndpoints:
    """Tests for endpoint constants."""

    def test_sources_endpoint(self):
        """SOURCES_ENDPOINT should be '/sources'."""
        assert SOURCES_ENDPOINT == "/sources"

    def test_sessions_endpoint(self):
        """SESSIONS_ENDPOINT should be '/sessions'."""
        assert SESSIONS_ENDPOINT == "/sessions"

    def test_session_detail_endpoint_format(self):
        """SESSION_DETAIL_ENDPOINT should contain session_id placeholder."""
        assert "/sessions/" in SESSION_DETAIL_ENDPOINT
        assert "{session_id}" in SESSION_DETAIL_ENDPOINT

    def test_session_delete_endpoint_format(self):
        """SESSION_DELETE_ENDPOINT should contain session_id placeholder."""
        assert "/sessions/" in SESSION_DELETE_ENDPOINT
        assert "{session_id}" in SESSION_DELETE_ENDPOINT

    def test_session_approve_endpoint_format(self):
        """SESSION_APPROVE_ENDPOINT should use :approvePlan action."""
        assert "/sessions/" in SESSION_APPROVE_ENDPOINT
        assert "{session_id}" in SESSION_APPROVE_ENDPOINT
        assert ":approvePlan" in SESSION_APPROVE_ENDPOINT

    def test_activities_endpoint_format(self):
        """ACTIVITIES_ENDPOINT should contain session_id placeholder."""
        assert "/sessions/" in ACTIVITIES_ENDPOINT
        assert "{session_id}" in ACTIVITIES_ENDPOINT
        assert "/activities" in ACTIVITIES_ENDPOINT

    def test_messages_endpoint_format(self):
        """MESSAGES_ENDPOINT should use :sendMessage action."""
        assert "/sessions/" in MESSAGES_ENDPOINT
        assert "{session_id}" in MESSAGES_ENDPOINT
        assert ":sendMessage" in MESSAGES_ENDPOINT
