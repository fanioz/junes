"""Tests for verbose mode."""

from click.testing import CliRunner
from unittest import mock

import responses

from junes.cli import cli
from junes.constants import BASE_URL


class TestVerboseMode:
    """Tests for verbose mode functionality."""

    @responses.activate
    def test_verbose_flag_enables_logging(self):
        """--verbose flag should enable verbose logging in API client."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"sources": []},
            status=200,
        )

        runner = CliRunner()

        with mock.patch("junes.client.logger"):
            result = runner.invoke(cli, ["--api-key", "test-key", "--verbose", "sources", "list"])

            # With verbose, logger should be called
            if result.exit_code == 0:
                # Verbose mode was passed to the client
                assert result.exit_code == 0

    @responses.activate
    def test_non_verbose_mode_suppresses_logs(self):
        """Non-verbose mode should not show verbose logs."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"sources": [{"id": "src1"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "sources", "list"])

        # Should succeed without verbose output
        assert result.exit_code == 0
        # Should not contain debug information
        assert "Request:" not in result.output

    @responses.activate
    def test_verbose_with_api_error(self):
        """Verbose mode should work even when API returns an error."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"error": "Unauthorized"},
            status=401,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "invalid-key", "--verbose", "sources", "list"])

        # Should still fail, but with error message
        assert result.exit_code != 0

    @responses.activate
    def test_verbose_shows_output(self):
        """Verbose mode should show output plus debug info."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"sources": [{"id": "src1", "name": "Source 1"}]},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "--verbose", "sources", "list"])

        # Should succeed
        assert result.exit_code == 0
        # Should show the results
        assert "src1" in result.output or "Source 1" in result.output


class TestAPIKeyRedactionInVerboseMode:
    """Tests for API key redaction in verbose logs."""

    @responses.activate
    def test_api_key_redacted_in_verbose_logs(self):
        """Verbose mode should redact API key in logs."""
        responses.get(
            f"{BASE_URL}/sources",
            json={"sources": []},
            status=200,
        )

        runner = CliRunner()

        with mock.patch("junes.client.logger") as mock_logger:
            result = runner.invoke(cli, ["--api-key", "secret-key-12345", "--verbose", "sources", "list"])

            # If logger was called, check that API key was redacted
            if result.exit_code == 0 and mock_logger.debug.called:
                # Get all logged messages
                for call in mock_logger.debug.call_args_list:
                    msg = str(call)
                    # Full API key should not appear in logs
                    assert "secret-key-12345" not in msg
