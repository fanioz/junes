"""Tests for agent commands."""

from click.testing import CliRunner

import responses

from jules_cli.cli import cli
from jules_cli.constants import BASE_URL


class TestAgentSendCommand:
    """Tests for 'agent send' command."""

    @responses.activate
    def test_agent_send_with_message_argument(self):
        """agent send should send a message provided as argument."""
        responses.post(
            f"{BASE_URL}/sessions/sess1/messages",
            json={"response": {"content": "Hello back!"}},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "agent", "send", "sess1", "Hello"])

        assert result.exit_code == 0
        assert "Hello back!" in result.output or "Hello" in result.output

    @responses.activate
    def test_agent_send_with_stdin(self):
        """agent send should read message from stdin when no argument."""
        responses.post(
            f"{BASE_URL}/sessions/sess1/messages",
            json={"response": {"content": "Response from stdin"}},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "agent", "send", "sess1"], input="Message from stdin")

        assert result.exit_code == 0
        assert "Response from stdin" in result.output or "stdin" in result.output

    @responses.activate
    def test_agent_send_json_format(self):
        """agent send --format json should output valid JSON."""
        responses.post(
            f"{BASE_URL}/sessions/sess1/messages",
            json={"response": {"content": "Response"}},
            status=200,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "--format", "json", "agent", "send", "sess1", "Hello"])

        assert result.exit_code == 0
        assert '"response"' in result.output

    @responses.activate
    def test_agent_send_error_handling(self):
        """agent send should handle API errors gracefully."""
        responses.post(
            f"{BASE_URL}/sessions/sess1/messages",
            json={"error": "Session not found"},
            status=404,
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["--api-key", "test-key", "agent", "send", "sess1", "Hello"])

        assert result.exit_code != 0
        assert "error" in result.output.lower() or "not found" in result.output.lower()
