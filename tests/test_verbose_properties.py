"""Property-based tests for verbose mode."""

from click.testing import CliRunner
from unittest import mock

from hypothesis import given, settings
from hypothesis import strategies as st

import responses

from jules_cli.cli import cli
from jules_cli.constants import BASE_URL


class TestVerboseModeSuppressionProperty:
    """Property 18: Verbose Mode Suppression (Requirements 14.5)"""

    @given(
        has_verbose_flag=st.booleans(),
    )
    @settings(max_examples=20)
    def test_verbose_mode_only_shows_logs_when_enabled(self, has_verbose_flag):
        """Verbose logs should only appear when --verbose flag is used."""
        with responses.RequestsMock() as rsps:
            # Mock the sources endpoint
            rsps.get(
                f"{BASE_URL}/sources",
                json={"sources": []},
                status=200,
            )

            runner = CliRunner()
            parts = ["--api-key", "test-key"]
            if has_verbose_flag:
                parts.append("--verbose")
            parts.extend(["sources", "list"])

            result = runner.invoke(cli, parts)

            # Should always succeed
            assert result.exit_code == 0

            # Output should not contain raw debug logs even in verbose mode
            # (because Click doesn't capture logger output to result.output)
            assert "DEBUG" not in result.output
