"""Property-based tests for configuration management."""

import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from jules_cli.config import ConfigManager
from jules_cli.exceptions import ConfigurationError


class TestAPIKeyPriorityProperty:
    """Property 1: API Key Priority Order (Requirements 1.1, 1.2, 1.3, 1.4)"""

    @given(
        cli_key=st.text(min_size=1, alphabet=st.characters(whitelist_categories=['L', 'N', 'P'], blacklist_characters='\x00')).filter(lambda x: x.strip()),
        env_key=st.text(min_size=1, alphabet=st.characters(whitelist_categories=['L', 'N', 'P'], blacklist_characters='\x00')).filter(lambda x: x.strip()),
        config_key=st.text(min_size=1, alphabet=st.characters(whitelist_categories=['L', 'N', 'P'], blacklist_characters='\x00')).filter(lambda x: x.strip()),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_cli_arg_overrides_env_and_config(self, cli_key, env_key, config_key):
        """CLI argument should always be returned when provided, regardless of ENV and config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                config_manager = ConfigManager()
                config_manager.init_config(api_key=config_key, format="json")

            with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                    config_manager = ConfigManager()

                with mock.patch.dict(os.environ, {"JULES_API_KEY": env_key}):
                    result = config_manager.get_api_key(cli_arg_key=cli_key)
                    assert result == cli_key

    @given(
        env_key=st.text(min_size=1, alphabet=st.characters(whitelist_categories=['L', 'N', 'P'], blacklist_characters='\x00')).filter(lambda x: x.strip()),
        config_key=st.text(min_size=1, alphabet=st.characters(whitelist_categories=['L', 'N', 'P'], blacklist_characters='\x00')).filter(lambda x: x.strip()),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_env_overrides_config_when_no_cli(self, env_key, config_key):
        """ENV variable should be returned when CLI arg not provided, overriding config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                config_manager = ConfigManager()
                config_manager.init_config(api_key=config_key, format="json")

            with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                    config_manager = ConfigManager()

                with mock.patch.dict(os.environ, {"JULES_API_KEY": env_key}):
                    result = config_manager.get_api_key(cli_arg_key=None)
                    assert result == env_key


class TestConfigPersistenceProperty:
    """Property 12: Configuration Persistence (Requirements 11.3, 11.4)"""

    @given(
        api_key=st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=['L', 'N', 'P'], blacklist_characters='\x00')).filter(lambda x: x.strip()),
        format=st.sampled_from(["json", "table", "plain"]),
    )
    @settings(max_examples=100)
    def test_config_persists_across_instances(self, api_key, format):
        """Configuration written by one ConfigManager instance should be readable by another."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # First instance writes config
            with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                cm1 = ConfigManager()
                cm1.init_config(api_key=api_key, format=format)

            # Second instance reads config
            with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                cm2 = ConfigManager()
                loaded = cm2.load_config()

                assert loaded["api_key"] == api_key
                assert loaded["format"] == format


class TestConfigValidationProperty:
    """Property 13: Configuration Validation (Requirements 11.5, 11.6)"""

    def test_valid_config_always_passes_validation(self):
        """Any configuration with required fields and valid values should pass validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                cm = ConfigManager()
                assert cm.validate_config({"api_key": "key", "format": "json"}) is True
                assert cm.validate_config({"api_key": "key", "format": "table"}) is True
                assert cm.validate_config({"api_key": "key", "format": "plain"}) is True
                assert cm.validate_config({"api_key": "key"}) is True  # format is optional

    def test_invalid_config_always_fails_validation(self):
        """Configurations missing required fields or with invalid values should fail validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch("jules_cli.config.Path.home", return_value=Path(tmpdir)):
                cm = ConfigManager()
                # Missing api_key
                assert cm.validate_config({"format": "json"}) is False
                # Invalid format
                assert cm.validate_config({"api_key": "key", "format": "invalid"}) is False
                # Not a dict
                assert cm.validate_config(None) is False
                assert cm.validate_config("string") is False
                assert cm.validate_config([]) is False
