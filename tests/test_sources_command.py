"""Tests for sources command."""

from click.testing import CliRunner
from unittest import mock

import responses

from jules_cli.cli import cli
from jules_cli.constants import BASE_URL


class TestSourcesListCommand:
    """Tests for 'sources list' command."""

    @responses.activate
    def test_sources_list_with_valid_api_key(self):
        """sources list should display sources when API key is valid."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"sources": [{"id": "src1", "name": "Source 1"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sources", "list"])

        assert result.exit_code == 0
        assert "Source 1" in result.output or "src1" in result.output

    @responses.activate
    def test_sources_list_json_format(self):
        """sources list --format json should output valid JSON."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"sources": [{"id": "src1", "name": "Source 1"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "--format", "json", "sources", "list"])

        assert result.exit_code == 0
        assert '"sources"' in result.output
        assert '"src1"' in result.output

    @responses.activate
    def test_sources_list_table_format(self):
        """sources list --format table should output a table."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"sources": [{"id": "src1", "name": "Source 1"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "--format", "table", "sources", "list"])

        assert result.exit_code == 0
        # Table format should have the data
        assert "src1" in result.output or "Source 1" in result.output

    @responses.activate
    def test_sources_list_empty(self):
        """sources list should handle empty sources list."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"sources": []},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sources", "list"])

        assert result.exit_code == 0
        assert "No sources" in result.output or "sources" in result.output.lower()

    @responses.activate
    def test_sources_list_api_error(self):
        """sources list should handle API errors gracefully."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"error": "Unauthorized"},
            status=401,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "invalid-key", "sources", "list"])

        assert result.exit_code != 0
        assert "error" in result.output.lower() or "authentication" in result.output.lower()

    def test_sources_list_with_filters(self):
        """sources list command should work (filters to be implemented later)."""
        # Just test that the basic command structure works
        runner = CliRunner()
        result = runner.invoke(cli, ["sources", "--help"])

        # Should show help for sources commands
        assert result.exit_code == 0
        assert "list" in result.output
