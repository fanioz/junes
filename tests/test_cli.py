"""Tests for CLI interface."""

from click.testing import CliRunner

from junes.cli import cli


class TestCLIGroup:
    """Tests for main CLI group."""

    def test_cli_exists(self):
        """CLI group should be defined and callable."""
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert "Usage:" in result.output or "junes" in result.output

    def test_version_flag(self):
        """--version flag should display version information."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "2.0.0" in result.output

    def test_help_flag(self):
        """--help flag should display help information."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Options:" in result.output
        assert "Commands:" in result.output

    def test_no_args_shows_help(self):
        """No arguments should show help with available commands."""
        runner = CliRunner()
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
        assert "Usage:" in result.output


class TestGlobalOptions:
    """Tests for global CLI options."""

    def test_api_key_option(self):
        """--api-key option should be available."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert "--api-key" in result.output

    def test_format_option(self):
        """--format option should be available."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert "--format" in result.output

    def test_verbose_option(self):
        """--verbose option should be available."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert "--verbose" in result.output

    def test_invalid_format_value(self):
        """Invalid format value should show error."""
        runner = CliRunner()
        # This will be tested when we have actual commands
        # For now, just verify the option exists
        result = runner.invoke(cli, ["--help"])
        assert "json" in result.output.lower() or "table" in result.output.lower()


class TestMissingAPIKey:
    """Tests for missing API key handling."""

    def test_error_without_api_key(self):
        """Commands should fail gracefully when no API key is provided."""
        runner = CliRunner()

        # Clear environment and config file
        import os
        from junes.config import ConfigManager
        env = os.environ.copy()
        env.pop("JULES_API_KEY", None)
        
        # Ensure no config file exists for the test
        config_manager = ConfigManager()
        if os.path.exists(config_manager.config_file):
            os.remove(config_manager.config_file)

        result = runner.invoke(cli, ["sources", "list"], env=env)
        # Should fail with error message about API key
        assert result.exit_code != 0
        assert "API key" in result.output or "not found" in result.output


class TestContextObject:
    """Tests for Click context object."""

    def test_context_passes_api_key(self):
        """Context should pass API key to commands."""
        # This will be tested when we implement actual commands
        pass

    def test_context_passes_format(self):
        """Context should pass format preference to commands."""
        # This will be tested when we implement actual commands
        pass

    def test_context_passes_verbose(self):
        """Context should pass verbose flag to commands."""
        # This will be tested when we implement actual commands
        pass
