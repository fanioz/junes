"""Tests for sessions commands."""

from click.testing import CliRunner

import responses

from jules_cli.cli import cli
from jules_cli.constants import BASE_URL


class TestSessionsCreateCommand:
    """Tests for 'sessions create' command."""

    @responses.activate
    def test_sessions_create_with_source_id(self):
        """sessions create should create a new session."""
        responses.post(
            f"{BASE_URL}/sessions",
            json={"session": {"id": "sess1", "source_id": "src1", "status": "active"}},
            status=201,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "create", "src1"])

        assert result.exit_code == 0
        assert "sess1" in result.output

    @responses.activate
    def test_sessions_create_with_parameters(self):
        """sessions create should pass additional parameters."""
        responses.post(
            f"{BASE_URL}/sessions",
            json={"session": {"id": "sess1"}},
            status=201,
        )

        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "create", "src1",
            "-p", "param1=value1"
        ])

        assert result.exit_code == 0

    @responses.activate
    def test_sessions_create_api_error(self):
        """sessions create should handle API errors."""
        responses.post(
            f"{BASE_URL}/sessions",
            json={"error": "Invalid source"},
            status=404,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "create", "invalid"])

        assert result.exit_code != 0
        assert "error" in result.output.lower()


class TestSessionsListCommand:
    """Tests for 'sessions list' command."""

    @responses.activate
    def test_sessions_list_returns_sessions(self):
        """sessions list should display sessions."""
        responses.get(
            f"{BASE_URL}/sessions",
            json={"sessions": [{"id": "sess1", "status": "active"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "list"])

        assert result.exit_code == 0
        assert "sess1" in result.output or "active" in result.output

    @responses.activate
    def test_sessions_list_with_status_filter(self):
        """sessions list --status should filter by status."""
        responses.get(
            f"{BASE_URL}/sessions?status=active",
            json={"sessions": [{"id": "sess1", "status": "active"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "list", "--status", "active"])

        assert result.exit_code == 0

    @responses.activate
    def test_sessions_list_json_format(self):
        """sessions list --format json should output JSON."""
        responses.get(
            f"{BASE_URL}/sessions",
            json={"sessions": []},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "--format", "json", "sessions", "list"])

        assert result.exit_code == 0
        assert '"sessions"' in result.output


class TestSessionsGetCommand:
    """Tests for 'sessions get' command."""

    @responses.activate
    def test_sessions_get_returns_details(self):
        """sessions get should display session details."""
        responses.get(
            f"{BASE_URL}/sessions/sess1",
            json={"session": {"id": "sess1", "status": "active"}},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "get", "sess1"])

        assert result.exit_code == 0
        assert "sess1" in result.output

    @responses.activate
    def test_sessions_get_not_found(self):
        """sessions get should handle 404 errors."""
        responses.get(
            f"{BASE_URL}/sessions/nonexistent",
            json={"error": "Session not found"},
            status=404,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "get", "nonexistent"])

        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "error" in result.output.lower()


class TestSessionsApproveCommand:
    """Tests for 'sessions approve' command."""

    @responses.activate
    def test_sessions_approve_succeeds(self):
        """sessions approve should approve the plan."""
        responses.post(
            f"{BASE_URL}/sessions/sess1/approve",
            json={"success": True},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "approve", "sess1"])

        assert result.exit_code == 0
        assert "approved" in result.output.lower() or "sess1" in result.output

    @responses.activate
    def test_sessions_approve_no_pending_plan(self):
        """sessions approve should handle no pending plan scenario."""
        responses.post(
            f"{BASE_URL}/sessions/sess1/approve",
            json={"error": "No pending plan"},
            status=400,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "approve", "sess1"])

        assert result.exit_code != 0
