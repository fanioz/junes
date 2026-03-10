"""Tests for API client."""

import json
from unittest import mock

import pytest
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import Timeout

import responses

from junes.client import JulesAPIClient
from junes.constants import BASE_URL
from junes.exceptions import (
    AuthenticationError,
    NetworkError,
    RateLimitError,
    ResourceNotFoundError,
    ServerError,
)


class TestJulesAPIClientInit:
    """Tests for JulesAPIClient initialization."""

    def test_init_with_api_key(self):
        """Client should be initialized with an API key."""
        client = JulesAPIClient(api_key="test-key")
        assert client.api_key == "test-key"

    def test_init_with_custom_base_url(self):
        """Client should accept a custom base URL."""
        client = JulesAPIClient(api_key="test-key", base_url="https://custom.example.com")
        assert client.base_url == "https://custom.example.com"

    def test_init_with_verbose_flag(self):
        """Client should accept a verbose flag."""
        client = JulesAPIClient(api_key="test-key", verbose=True)
        assert client.verbose is True

    def test_init_defaults_verbose_to_false(self):
        """Client should default verbose to False."""
        client = JulesAPIClient(api_key="test-key")
        assert client.verbose is False


class TestMakeRequest:
    """Tests for _make_request method."""

    @responses.activate
    def test_successful_get_request(self):
        """_make_request should handle successful GET requests."""
        responses.get(
            f"{BASE_URL}/test",
            json={"result": "success"},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client._make_request("GET", "/test")

        assert result == {"result": "success"}

    @responses.activate
    def test_successful_post_request(self):
        """_make_request should handle successful POST requests."""
        responses.post(
            f"{BASE_URL}/test",
            json={"created": True},
            status=201,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client._make_request("POST", "/test", json={"name": "test"})

        assert result == {"created": True}

    @responses.activate
    def test_successful_delete_request(self):
        """_make_request should handle successful DELETE requests with empty body."""
        responses.delete(
            f"{BASE_URL}/test",
            body="",
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client._make_request("DELETE", "/test")

        assert result == {}

    @responses.activate
    def test_includes_api_key_header(self):
        """_make_request should include the API key in headers."""
        responses.get(
            f"{BASE_URL}/test",
            json={"result": "success"},
            status=200,
        )

        client = JulesAPIClient(api_key="secret-key", verbose=False)
        client._make_request("GET", "/test")

        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["x-goog-api-key"] == "secret-key"

    @responses.activate
    def test_401_raises_authentication_error(self):
        """_make_request should raise AuthenticationError on 401."""
        responses.get(
            f"{BASE_URL}/test",
            json={"error": "Unauthorized"},
            status=401,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)

        with pytest.raises(AuthenticationError):
            client._make_request("GET", "/test")

    @responses.activate
    def test_404_raises_resource_not_found_error(self):
        """_make_request should raise ResourceNotFoundError on 404."""
        responses.get(
            f"{BASE_URL}/test",
            json={"error": "Not found"},
            status=404,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)

        with pytest.raises(ResourceNotFoundError):
            client._make_request("GET", "/test")

    @responses.activate
    def test_429_raises_rate_limit_error(self):
        """_make_request should raise RateLimitError on 429."""
        responses.get(
            f"{BASE_URL}/test",
            json={"error": "Too many requests"},
            status=429,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)

        with pytest.raises(RateLimitError):
            client._make_request("GET", "/test")

    @responses.activate
    def test_500_raises_server_error(self):
        """_make_request should raise ServerError on 500."""
        responses.get(
            f"{BASE_URL}/test",
            json={"error": "Internal server error"},
            status=500,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)

        with pytest.raises(ServerError):
            client._make_request("GET", "/test")

    @responses.activate
    def test_503_raises_server_error(self):
        """_make_request should raise ServerError on 503."""
        responses.get(
            f"{BASE_URL}/test",
            json={"error": "Service unavailable"},
            status=503,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)

        with pytest.raises(ServerError):
            client._make_request("GET", "/test")

    @responses.activate
    def test_connection_timeout_raises_network_error(self):
        """_make_request should raise NetworkError on connection timeout."""
        with mock.patch("requests.request", side_effect=Timeout("Connection timed out")):
            client = JulesAPIClient(api_key="test-key", verbose=False)

            with pytest.raises(NetworkError, match="Connection timed out"):
                client._make_request("GET", "/test")

    @responses.activate
    def test_connection_error_raises_network_error(self):
        """_make_request should raise NetworkError on connection failure."""
        with mock.patch("requests.request", side_effect=RequestsConnectionError("Connection refused")):
            client = JulesAPIClient(api_key="test-key", verbose=False)

            with pytest.raises(NetworkError, match="Connection refused"):
                client._make_request("GET", "/test")


class TestListSources:
    """Tests for list_sources method."""

    @responses.activate
    def test_list_sources_returns_sources(self):
        """list_sources should return a list of sources."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"sources": [{"id": "src1", "name": "Source 1"}]},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.list_sources()

        assert result == {"sources": [{"id": "src1", "name": "Source 1"}]}

    @responses.activate
    def test_list_sources_with_filters(self):
        """list_sources should pass query parameters."""
        responses.get(
            f"{BASE_URL}/sources?filter=active",
            json={"sources": []},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.list_sources(filter="active")

        assert result == {"sources": []}


class TestCreateSession:
    """Tests for create_session method."""

    @responses.activate
    def test_create_session_with_prompt_only(self):
        """create_session should send prompt in request body."""
        responses.post(
            f"{BASE_URL}/sessions",
            json={
                "name": "sessions/1234567",
                "id": "abc123",
                "prompt": "Add tests",
                "state": "QUEUED",
            },
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.create_session(prompt="Add tests")

        assert result["id"] == "abc123"
        assert result["state"] == "QUEUED"

        # Verify request body
        request_body = json.loads(responses.calls[0].request.body)
        assert request_body == {"prompt": "Add tests"}

    @responses.activate
    def test_create_session_with_all_options(self):
        """create_session should include all optional fields."""
        responses.post(
            f"{BASE_URL}/sessions",
            json={"name": "sessions/1234567", "id": "abc123", "state": "QUEUED"},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        client.create_session(
            prompt="Add tests",
            title="Auth tests",
            source="sources/github-myorg-myrepo",
            starting_branch="main",
            require_plan_approval=True,
            automation_mode="AUTO_CREATE_PR",
        )

        request_body = json.loads(responses.calls[0].request.body)
        assert request_body["prompt"] == "Add tests"
        assert request_body["title"] == "Auth tests"
        assert request_body["sourceContext"]["source"] == "sources/github-myorg-myrepo"
        assert request_body["sourceContext"]["githubRepoContext"]["startingBranch"] == "main"
        assert request_body["requirePlanApproval"] is True
        assert request_body["automationMode"] == "AUTO_CREATE_PR"

    @responses.activate
    def test_create_session_with_source_no_branch(self):
        """create_session should handle source without branch."""
        responses.post(
            f"{BASE_URL}/sessions",
            json={"name": "sessions/1234567", "id": "abc123", "state": "QUEUED"},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        client.create_session(prompt="Add tests", source="sources/github-myorg-myrepo")

        request_body = json.loads(responses.calls[0].request.body)
        assert request_body["sourceContext"] == {"source": "sources/github-myorg-myrepo"}
        assert "githubRepoContext" not in request_body["sourceContext"]


class TestListSessions:
    """Tests for list_sessions method."""

    @responses.activate
    def test_list_sessions_returns_sessions(self):
        """list_sessions should return a list of sessions."""
        responses.get(
            f"{BASE_URL}/sessions",
            json={"sessions": [{"id": "sess1", "state": "COMPLETED"}]},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.list_sessions()

        assert result == {"sessions": [{"id": "sess1", "state": "COMPLETED"}]}

    @responses.activate
    def test_list_sessions_with_page_size(self):
        """list_sessions should pass pageSize parameter."""
        responses.get(
            f"{BASE_URL}/sessions?pageSize=10",
            json={"sessions": [], "nextPageToken": "abc"},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.list_sessions(pageSize=10)

        assert result == {"sessions": [], "nextPageToken": "abc"}


class TestGetSession:
    """Tests for get_session method."""

    @responses.activate
    def test_get_session_returns_session(self):
        """get_session should return the session details."""
        responses.get(
            f"{BASE_URL}/sessions/sess1",
            json={
                "name": "sessions/sess1",
                "id": "sess1",
                "state": "COMPLETED",
                "title": "Test session",
            },
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.get_session("sess1")

        assert result["id"] == "sess1"
        assert result["state"] == "COMPLETED"


class TestDeleteSession:
    """Tests for delete_session method."""

    @responses.activate
    def test_delete_session_returns_empty(self):
        """delete_session should return empty dict on success."""
        responses.delete(
            f"{BASE_URL}/sessions/sess1",
            body="",
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.delete_session("sess1")

        assert result == {}

    @responses.activate
    def test_delete_session_not_found(self):
        """delete_session should raise ResourceNotFoundError on 404."""
        responses.delete(
            f"{BASE_URL}/sessions/nonexistent",
            json={"error": "Session not found"},
            status=404,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)

        with pytest.raises(ResourceNotFoundError):
            client.delete_session("nonexistent")


class TestApprovePlan:
    """Tests for approve_plan method."""

    @responses.activate
    def test_approve_plan_returns_success(self):
        """approve_plan should POST to :approvePlan endpoint."""
        responses.post(
            f"{BASE_URL}/sessions/sess1:approvePlan",
            json={},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.approve_plan("sess1")

        assert result == {}

        # Verify empty JSON body was sent
        request_body = json.loads(responses.calls[0].request.body)
        assert request_body == {}


class TestListActivities:
    """Tests for list_activities method."""

    @responses.activate
    def test_list_activities_returns_activities(self):
        """list_activities should return a list of activities."""
        responses.get(
            f"{BASE_URL}/sessions/sess1/activities",
            json={"activities": [{"id": "act1"}]},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.list_activities("sess1")

        assert result == {"activities": [{"id": "act1"}]}


class TestSendMessage:
    """Tests for send_message method."""

    @responses.activate
    def test_send_message_returns_response(self):
        """send_message should POST to :sendMessage with prompt field."""
        responses.post(
            f"{BASE_URL}/sessions/sess1:sendMessage",
            json={},
            status=200,
        )

        client = JulesAPIClient(api_key="test-key", verbose=False)
        result = client.send_message("sess1", "Hello")

        assert result == {}

        # Verify prompt field in request body
        request_body = json.loads(responses.calls[0].request.body)
        assert request_body == {"prompt": "Hello"}
