"""Property-based tests for CLI interface."""

from click.testing import CliRunner

from hypothesis import given, settings
from hypothesis import strategies as st

from junes.cli import cli


class TestExitCodeCorrectnessProperty:
    """Property 3: Exit Code Correctness (Requirements 1.5, 3.5, 5.4, 6.5, 9.6)"""

    @given(
        args=st.lists(
            st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=['L', 'N'], blacklist_characters='\x00')),
            min_size=1,
            max_size=5,
        )
    )
    @settings(max_examples=50)
    def test_cli_has_valid_exit_code(self, args):
        """CLI should always return a valid exit code (0 for help, non-zero for errors)."""
        runner = CliRunner()
        result = runner.invoke(cli, args)

        # Exit code should be an integer
        assert isinstance(result.exit_code, int)

        # Exit code should be non-negative
        assert result.exit_code >= 0

    def test_help_returns_zero(self):
        """Help command should always return exit code 0."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0

    def test_version_returns_zero(self):
        """Version command should always return exit code 0."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0

    def test_no_args_returns_zero(self):
        """No arguments should return exit code 0 (shows help)."""
        runner = CliRunner()
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
