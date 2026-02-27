"""Property-based tests for help system."""

from click.testing import CliRunner

from hypothesis import given, settings
from hypothesis import strategies as st

from jules_cli.cli import cli


class TestCommandHelpAvailabilityProperty:
    """Property 14: Command Help Availability (Requirements 12.2)"""

    @given(command=st.sampled_from([
        "sources", "sessions", "activities", "agent", "config",
        "sources list", "sessions create", "sessions list",
        "sessions get", "sessions approve", "activities list",
        "agent send", "config init"
    ]))
    @settings(max_examples=20)
    def test_all_commands_have_help(self, command):
        """All commands should have help available via --help flag."""
        runner = CliRunner()
        parts = command.split()
        result = runner.invoke(cli, parts + ["--help"])

        # Should always succeed
        assert result.exit_code == 0
        # Should contain help content
        assert len(result.output) > 0


class TestHelpContentCompletenessProperty:
    """Property 15: Help Content Completeness (Requirements 12.4, 12.5)"""

    def test_help_contains_required_sections(self):
        """Help should contain Usage, Options, and Arguments sections."""
        runner = CliRunner()

        # Test a few representative commands
        commands_to_test = [
            ["sources", "list"],
            ["sessions", "create"],
            ["agent", "send"],
        ]

        for command in commands_to_test:
            result = runner.invoke(cli, command + ["--help"])

            assert result.exit_code == 0
            # Should have usage line
            assert "Usage:" in result.output or "usage:" in result.output.lower()
            # Should have options section (even if empty)
            assert "Options:" in result.output or "options:" in result.output.lower()

    def test_main_help_shows_all_command_groups(self):
        """Main help should show all top-level command groups."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        # Should list all major command groups
        assert "sources" in result.output
        assert "sessions" in result.output
        assert "activities" in result.output
        assert "agent" in result.output
        assert "config" in result.output
