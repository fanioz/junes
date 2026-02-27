"""Tests for help system and documentation."""

from click.testing import CliRunner

from jules_cli.cli import cli


class TestHelpSystem:
    """Tests for CLI help system."""

    def test_main_help_shows_all_commands(self):
        """Main help should list all available commands."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Commands:" in result.output
        # Check all major commands are listed
        assert "sources" in result.output
        assert "sessions" in result.output
        assert "activities" in result.output
        assert "agent" in result.output
        assert "config" in result.output

    def test_sources_help_available(self):
        """sources command should have help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["sources", "--help"])

        assert result.exit_code == 0
        assert "Manage sources" in result.output or "list" in result.output

    def test_sources_list_help_available(self):
        """sources list subcommand should have help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["sources", "list", "--help"])

        assert result.exit_code == 0
        assert "List" in result.output

    def test_sessions_help_available(self):
        """sessions command should have help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["sessions", "--help"])

        assert result.exit_code == 0
        assert "Manage sessions" in result.output

    def test_sessions_create_help_shows_syntax(self):
        """sessions create help should show SOURCE_ID argument."""
        runner = CliRunner()
        result = runner.invoke(cli, ["sessions", "create", "--help"])

        assert result.exit_code == 0
        assert "SOURCE_ID" in result.output or "source" in result.output.lower()
        assert "Create" in result.output

    def test_sessions_list_help_shows_status_option(self):
        """sessions list help should show --status option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["sessions", "list", "--help"])

        assert result.exit_code == 0
        assert "--status" in result.output or "status" in result.output.lower()

    def test_sessions_get_help_shows_syntax(self):
        """sessions get help should show SESSION_ID argument."""
        runner = CliRunner()
        result = runner.invoke(cli, ["sessions", "get", "--help"])

        assert result.exit_code == 0
        assert "SESSION_ID" in result.output or "session" in result.output.lower()

    def test_sessions_approve_help_shows_syntax(self):
        """sessions approve help should show SESSION_ID argument."""
        runner = CliRunner()
        result = runner.invoke(cli, ["sessions", "approve", "--help"])

        assert result.exit_code == 0
        assert "SESSION_ID" in result.output or "session" in result.output.lower()
        assert "Approve" in result.output

    def test_activities_help_available(self):
        """activities command should have help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["activities", "--help"])

        assert result.exit_code == 0
        assert "Manage activities" in result.output or "list" in result.output

    def test_activities_list_help_shows_syntax(self):
        """activities list help should show SESSION_ID argument."""
        runner = CliRunner()
        result = runner.invoke(cli, ["activities", "list", "--help"])

        assert result.exit_code == 0
        assert "SESSION_ID" in result.output or "session" in result.output.lower()

    def test_agent_help_available(self):
        """agent command should have help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["agent", "--help"])

        assert result.exit_code == 0
        assert "Interact" in result.output or "send" in result.output

    def test_agent_send_help_shows_syntax(self):
        """agent send help should show SESSION_ID and MESSAGE arguments."""
        runner = CliRunner()
        result = runner.invoke(cli, ["agent", "send", "--help"])

        assert result.exit_code == 0
        assert "SESSION_ID" in result.output or "session" in result.output.lower()
        assert "MESSAGE" in result.output or "message" in result.output.lower()

    def test_config_help_available(self):
        """config command should have help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "--help"])

        assert result.exit_code == 0
        assert "Manage configuration" in result.output or "init" in result.output

    def test_config_init_help_shows_prompts(self):
        """config init help should show the prompts."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "init", "--help"])

        assert result.exit_code == 0
        assert "Initialize" in result.output

    def test_help_shows_global_options(self):
        """Help should show all global options."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "--api-key" in result.output or "api-key" in result.output.lower()
        assert "--format" in result.output or "format" in result.output.lower()
        assert "--verbose" in result.output or "verbose" in result.output.lower()
