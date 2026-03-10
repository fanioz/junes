"""API client for Jules REST API."""

import logging
import re
from typing import Optional

from jules_cli.constants import (
    API_KEY_HEADER,
    BASE_URL,
    CONTENT_TYPE_HEADER,
    ACTIVITIES_ENDPOINT,
    MESSAGES_ENDPOINT,
    SESSION_APPROVE_ENDPOINT,
    SESSION_DELETE_ENDPOINT,
    SESSION_DETAIL_ENDPOINT,
    SESSIONS_ENDPOINT,
    SOURCES_ENDPOINT,
)
from jules_cli.exceptions import (
    AuthenticationError,
    NetworkError,
    RateLimitError,
    ResourceNotFoundError,
    ServerError,
)


# Configure logging
logger = logging.getLogger(__name__)


def _redact_api_key(text: str, api_key: str) -> str:
    """Redact API key from text for logging."""
    if not api_key:
        return text
    # Show first 4 and last 4 characters, mask the rest
    if len(api_key) <= 8:
        return re.sub(re.escape(api_key), "***", text)
    masked_key = f"{api_key[:4]}...{api_key[-4:]}"
    return re.sub(re.escape(api_key), masked_key, text)


class JulesAPIClient:
    """Client for interacting with the Jules API.

    Note: The `requests` library is lazily imported in `_make_request` to improve
    CLI startup time for commands that don't make API calls (e.g., `--help`).
    """

    def __init__(self, api_key: str, base_url: str = BASE_URL, verbose: bool = False):
        """
        Initialize the API client.

        Args:
            api_key: The API key for authentication
            base_url: The base URL of the API (default: from constants)
            verbose: Enable verbose logging
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.verbose = verbose

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json: JSON body for POST requests

        Returns:
            dict: Parsed JSON response

        Raises:
            AuthenticationError: If authentication fails (401)
            ResourceNotFoundError: If resource not found (404)
            RateLimitError: If rate limit exceeded (429)
            ServerError: If server returns an error (5xx)
            NetworkError: If network error occurs
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            API_KEY_HEADER: self.api_key,
            CONTENT_TYPE_HEADER: "application/json",
        }

        if self.verbose:
            safe_url = _redact_api_key(url, self.api_key)
            safe_headers = {k: _redact_api_key(v, self.api_key) for k, v in headers.items()}
            logger.debug(f"Request: {method} {safe_url}")
            logger.debug(f"Headers: {safe_headers}")
            if json:
                logger.debug(f"Body: {json}")

        import requests  # Lazy import to improve CLI startup time
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
            )

            if self.verbose:
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response body: {response.text[:500]}")

            # Handle error status codes
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed. Check your API key.")
            elif response.status_code == 404:
                raise ResourceNotFoundError(response.json().get("error", "Resource not found"))
            elif response.status_code == 429:
                raise RateLimitError(response.json().get("error", "Rate limit exceeded"))
            elif response.status_code >= 500:
                raise ServerError(response.json().get("error", f"Server error: {response.status_code}"))

            # Return parsed JSON for successful responses
            response.raise_for_status()

            # Handle empty responses (e.g., DELETE, sendMessage, approvePlan)
            if not response.text or not response.text.strip():
                return {}

            return response.json()

        except requests.exceptions.Timeout as e:
            raise NetworkError(f"Request timed out: {e}")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection failed: {e}")
        except (AuthenticationError, ResourceNotFoundError, RateLimitError, ServerError, NetworkError):
            raise
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {e}")

    def list_sources(self, **params) -> dict:
        """
        List available sources.

        Returns:
            dict: List of sources

        Raises:
            JulesAPIError: If the API request fails
        """
        return self._make_request("GET", SOURCES_ENDPOINT, params=params)

    def create_session(
        self,
        prompt: str,
        title: Optional[str] = None,
        source: Optional[str] = None,
        starting_branch: Optional[str] = None,
        require_plan_approval: Optional[bool] = None,
        automation_mode: Optional[str] = None,
    ) -> dict:
        """
        Create a new session.

        Args:
            prompt: The task description for Jules to execute (required)
            title: Optional title for the session
            source: Source resource name (e.g. "sources/github-myorg-myrepo")
            starting_branch: Starting branch name (e.g. "main")
            require_plan_approval: If True, plans require explicit approval
            automation_mode: Automation mode (e.g. "AUTO_CREATE_PR")

        Returns:
            dict: Created session details

        Raises:
            JulesAPIError: If the API request fails
        """
        data = {"prompt": prompt}

        if title is not None:
            data["title"] = title

        if source is not None:
            source_context = {"source": source}
            if starting_branch is not None:
                source_context["githubRepoContext"] = {
                    "startingBranch": starting_branch
                }
            data["sourceContext"] = source_context

        if require_plan_approval is not None:
            data["requirePlanApproval"] = require_plan_approval

        if automation_mode is not None:
            data["automationMode"] = automation_mode

        return self._make_request("POST", SESSIONS_ENDPOINT, json=data)

    def list_sessions(self, **params) -> dict:
        """
        List sessions.

        Args:
            **params: Query parameters (pageSize, pageToken)

        Returns:
            dict: List of sessions

        Raises:
            JulesAPIError: If the API request fails
        """
        return self._make_request("GET", SESSIONS_ENDPOINT, params=params)

    def get_session(self, session_id: str) -> dict:
        """
        Get session details.

        Args:
            session_id: The session ID

        Returns:
            dict: Session details

        Raises:
            JulesAPIError: If the API request fails
        """
        endpoint = SESSION_DETAIL_ENDPOINT.format(session_id=session_id)
        return self._make_request("GET", endpoint)

    def delete_session(self, session_id: str) -> dict:
        """
        Delete a session.

        Args:
            session_id: The session ID

        Returns:
            dict: Empty response on success

        Raises:
            JulesAPIError: If the API request fails
        """
        endpoint = SESSION_DELETE_ENDPOINT.format(session_id=session_id)
        return self._make_request("DELETE", endpoint)

    def approve_plan(self, session_id: str) -> dict:
        """
        Approve a pending plan.

        Args:
            session_id: The session ID

        Returns:
            dict: Approval response

        Raises:
            JulesAPIError: If the API request fails
        """
        endpoint = SESSION_APPROVE_ENDPOINT.format(session_id=session_id)
        return self._make_request("POST", endpoint, json={})

    def list_activities(self, session_id: str) -> dict:
        """
        List activities for a session.

        Args:
            session_id: The session ID

        Returns:
            dict: List of activities

        Raises:
            JulesAPIError: If the API request fails
        """
        endpoint = ACTIVITIES_ENDPOINT.format(session_id=session_id)
        return self._make_request("GET", endpoint)

    def send_message(self, session_id: str, message: str) -> dict:
        """
        Send a message to a session.

        Args:
            session_id: The session ID
            message: The message to send

        Returns:
            dict: SendMessageResponse (empty on success)

        Raises:
            JulesAPIError: If the API request fails
        """
        endpoint = MESSAGES_ENDPOINT.format(session_id=session_id)
        return self._make_request("POST", endpoint, json={"prompt": message})
