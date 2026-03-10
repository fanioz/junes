"""Tests for sessions commands."""

from click.testing import CliRunner

import responses

from junes.cli import cli
from junes.constants import BASE_URL


class TestSessionsCreateCommand:
    """Tests for 'sessions create' command."""

    @responses.activate
    def test_sessions_create_with_prompt(self):
        """sessions create should create a new session with --prompt."""
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

        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "create",
            "--prompt", "Add tests",
        ])

        assert result.exit_code == 0
        assert "abc123" in result.output

    @responses.activate
    def test_sessions_create_with_all_options(self):
        """sessions create should pass all options."""
        responses.post(
            f"{BASE_URL}/sessions",
            json={"name": "sessions/1234567", "id": "abc123", "state": "QUEUED"},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "create",
            "--prompt", "Add tests",
            "--title", "Auth tests",
            "--source", "sources/github-myorg-myrepo",
            "--branch", "main",
            "--require-approval",
            "--auto-pr",
        ])

        assert result.exit_code == 0

    @responses.activate
    def test_sessions_create_requires_prompt(self):
        """sessions create should fail without --prompt."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "create",
        ])

        assert result.exit_code != 0
        assert "prompt" in result.output.lower() or "required" in result.output.lower() or "missing" in result.output.lower()

    @responses.activate
    def test_sessions_create_api_error(self):
        """sessions create should handle API errors."""
        responses.post(
            f"{BASE_URL}/sessions",
            json={"error": "Invalid source"},
            status=404,
        )

        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "create",
            "--prompt", "Add tests",
        ])

        assert result.exit_code != 0
        assert "error" in result.output.lower()


class TestSessionsListCommand:
    """Tests for 'sessions list' command."""

    @responses.activate
    def test_sessions_list_returns_sessions(self):
        """sessions list should display sessions."""
        responses.get(
            f"{BASE_URL}/sessions",
            json={"sessions": [{"id": "sess1", "state": "COMPLETED", "title": "Test"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "list"])

        assert result.exit_code == 0
        assert "sess1" in result.output or "COMPLETED" in result.output

    @responses.activate
    def test_sessions_list_with_page_size(self):
        """sessions list --page-size should pass pageSize."""
        responses.get(
            f"{BASE_URL}/sessions?pageSize=10",
            json={"sessions": [{"id": "sess1", "state": "COMPLETED"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "list",
            "--page-size", "10",
        ])

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
            json={
                "name": "sessions/sess1",
                "id": "sess1",
                "state": "COMPLETED",
                "title": "Test session",
            },
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


class TestSessionsDeleteCommand:
    """Tests for 'sessions delete' command."""

    @responses.activate
    def test_sessions_delete_with_confirmation(self):
        """sessions delete should delete the session after confirmation."""
        responses.delete(
            f"{BASE_URL}/sessions/sess1",
            body="",
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "delete", "sess1",
        ], input="y\n")

        assert result.exit_code == 0
        assert "deleted" in result.output.lower()

    @responses.activate
    def test_sessions_delete_with_yes_flag(self):
        """sessions delete --yes should skip confirmation."""
        responses.delete(
            f"{BASE_URL}/sessions/sess1",
            body="",
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "delete", "sess1", "--yes",
        ])

        assert result.exit_code == 0
        assert "deleted" in result.output.lower()

    def test_sessions_delete_abort(self):
        """sessions delete should abort when user declines."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "delete", "sess1",
        ], input="n\n")

        assert result.exit_code != 0

    @responses.activate
    def test_sessions_delete_not_found(self):
        """sessions delete should handle 404 errors."""
        responses.delete(
            f"{BASE_URL}/sessions/nonexistent",
            json={"error": "Session not found"},
            status=404,
        )

        runner = CliRunner()
        result = runner.invoke(cli, [
            "--api-key", "test-key",
            "sessions", "delete", "nonexistent", "--yes",
        ])

        assert result.exit_code != 0
        assert "error" in result.output.lower()


class TestSessionsApproveCommand:
    """Tests for 'sessions approve' command."""

    @responses.activate
    def test_sessions_approve_succeeds(self):
        """sessions approve should approve the plan."""
        responses.post(
            f"{BASE_URL}/sessions/sess1:approvePlan",
            json={},
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
            f"{BASE_URL}/sessions/sess1:approvePlan",
            json={"error": "No pending plan"},
            status=400,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sessions", "approve", "sess1"])

        assert result.exit_code != 0
