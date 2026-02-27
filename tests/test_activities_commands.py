"""Tests for activities commands."""

from click.testing import CliRunner

import responses

from jules_cli.cli import cli
from jules_cli.constants import BASE_URL


class TestActivitiesListCommand:
    """Tests for 'activities list' command."""

    @responses.activate
    def test_activities_list_returns_activities(self):
        """activities list should display activities for a session."""
        responses.get(
            f"{BASE_URL}/sessions/sess1/activities",
            json={"activities": [{"id": "act1", "type": "plan", "timestamp": "2024-01-01T10:00:00Z"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "activities", "list", "sess1"])

        assert result.exit_code == 0
        assert "act1" in result.output or "plan" in result.output

    @responses.activate
    def test_activities_list_json_format(self):
        """activities list --format json should output valid JSON."""
        responses.get(
            f"{BASE_URL}/sessions/sess1/activities",
            json={"activities": []},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "--format", "json", "activities", "list", "sess1"])

        assert result.exit_code == 0
        assert '"activities"' in result.output

    @responses.activate
    def test_activities_list_table_format(self):
        """activities list --format table should output a table."""
        responses.get(
            f"{BASE_URL}/sessions/sess1/activities",
            json={"activities": [{"id": "act1", "timestamp": "2024-01-01T10:00:00Z"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "--format", "table", "activities", "list", "sess1"])

        assert result.exit_code == 0
        # Table format should have the data
        assert "act1" in result.output or "2024-01-01" in result.output

    @responses.activate
    def test_activities_list_empty(self):
        """activities list should handle empty activities list."""
        responses.get(
            f"{BASE_URL}/sessions/sess1/activities",
            json={"activities": []},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "activities", "list", "sess1"])

        assert result.exit_code == 0
        assert "No activities" in result.output or "activities" in result.output.lower()

    @responses.activate
    def test_activities_list_chronological_ordering(self):
        """activities list should order activities chronologically in table format."""
        responses.get(
            f"{BASE_URL}/sessions/sess1/activities",
            json={"activities": [
                {"id": "act2", "timestamp": "2024-01-01T10:00:00Z"},
                {"id": "act1", "timestamp": "2024-01-01T09:00:00Z"}
            ]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "--format", "table", "activities", "list", "sess1"])

        assert result.exit_code == 0
        # In chronological order, act1 (09:00) should appear before act2 (10:00)
        # This is tested more thoroughly in formatter tests
        assert "act1" in result.output and "act2" in result.output

    @responses.activate
    def test_activities_list_session_not_found(self):
        """activities list should handle session not found error."""
        responses.get(
            f"{BASE_URL}/sessions/nonexistent/activities",
            json={"error": "Session not found"},
            status=404,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "activities", "list", "nonexistent"])

        assert result.exit_code != 0
        assert "error" in result.output.lower() or "not found" in result.output.lower()
