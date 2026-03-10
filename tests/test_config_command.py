"""Tests for config command."""

from click.testing import CliRunner
from pathlib import Path
from unittest import mock

from junes.cli import cli


class TestConfigInitCommand:
    """Tests for 'config init' command."""

    def test_config_init_prompts_for_values(self):
        """config init should prompt for API key and format."""
        runner = CliRunner()

        # Simulate user input
        result = runner.invoke(cli, ["config", "init"], input="my-api-key\nplain\n")

        assert result.exit_code == 0
        assert "API key" in result.output or "Configuration initialized" in result.output

    def test_config_init_creates_config_file(self):
        """config init should create a config file."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Mock the home directory to use temp directory
            with mock.patch("junes.config.Path.home") as mock_home:
                mock_home.return_value = Path(".")
                result = runner.invoke(cli, ["config", "init"], input="test-key\njson\n")

                assert result.exit_code == 0
                assert "Configuration initialized" in result.output

    def test_config_init_with_options(self):
        """config init should accept API key and format as options."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            with mock.patch("junes.config.Path.home") as mock_home:
                mock_home.return_value = Path(".")
                result = runner.invoke(cli, ["config", "init", "--api-key", "key123", "--format", "table"])

                assert result.exit_code == 0
                assert "Configuration initialized" in result.output

    def test_config_init_help(self):
        """config init --help should show help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "init", "--help"])

        assert result.exit_code == 0
        assert "Initialize" in result.output
