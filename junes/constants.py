"""API constants for Jules REST API."""

# Base URL
BASE_URL = "https://jules.googleapis.com/v1alpha"

# Headers
API_KEY_HEADER = "x-goog-api-key"
CONTENT_TYPE_HEADER = "content-type"

# Endpoints
SOURCES_ENDPOINT = "/sources"
SESSIONS_ENDPOINT = "/sessions"
SESSION_DETAIL_ENDPOINT = "/sessions/{session_id}"
SESSION_DELETE_ENDPOINT = "/sessions/{session_id}"
SESSION_APPROVE_ENDPOINT = "/sessions/{session_id}:approvePlan"
ACTIVITIES_ENDPOINT = "/sessions/{session_id}/activities"
MESSAGES_ENDPOINT = "/sessions/{session_id}:sendMessage"
