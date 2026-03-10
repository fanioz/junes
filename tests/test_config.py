"""Tests for configuration management."""

import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from junes.config import ConfigManager
from junes.exceptions import ConfigurationError


class TestConfigManager:
    """Tests for ConfigManager class."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary directory for config files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def config_manager(self, temp_config_dir):
        """Create a ConfigManager with a temp config directory."""
        with mock.patch("junes.config.Path.home", return_value=Path(temp_config_dir)):
            return ConfigManager()

    def test_init_config_creates_config_directory(self, config_manager):
        """init_config should create the .junes directory."""
        config_dir = config_manager.config_dir

        # Ensure directory doesn't exist before
        if config_dir.exists():
            config_dir.rmdir()

        config_manager.init_config(api_key="test-key", format="json")

        assert config_dir.exists()
        assert config_dir.is_dir()

    def test_init_config_creates_config_file(self, config_manager):
        """init_config should create the config.toml file."""
        config_manager.init_config(api_key="test-api-key", format="table")

        config_file = config_manager.config_file
        assert config_file.exists()
        assert config_file.is_file()

    def test_init_config_stores_api_key(self, config_manager):
        """init_config should store the API key in the config file."""
        test_key = "my-secret-api-key"
        config_manager.init_config(api_key=test_key, format="json")

        loaded = config_manager.load_config()
        assert loaded["api_key"] == test_key

    def test_init_config_stores_format(self, config_manager):
        """init_config should store the format in the config file."""
        config_manager.init_config(api_key="test-key", format="table")

        loaded = config_manager.load_config()
        assert loaded["format"] == "table"

    def test_load_config_returns_config_dict(self, config_manager):
        """load_config should return a dictionary with config values."""
        config_manager.init_config(api_key="test-key", format="plain")

        config = config_manager.load_config()
        assert isinstance(config, dict)
        assert "api_key" in config
        assert "format" in config

    def test_load_config_raises_error_if_file_missing(self, config_manager):
        """load_config should raise ConfigurationError if config file doesn't exist."""
        # Ensure config file doesn't exist
        config_file = Path.home() / ".junes" / "config.toml"
        if config_file.exists():
            config_file.unlink()

        with pytest.raises(ConfigurationError, match="Configuration file not found"):
            config_manager.load_config()

    def test_get_api_key_from_cli_arg(self, config_manager):
        """get_api_key should return CLI arg API key when provided."""
        cli_key = "cli-provided-key"
        config_manager.init_config(api_key="config-key", format="json")

        # Mock environment to not have JULES_API_KEY
        with mock.patch.dict(os.environ, {}, clear=True):
            result = config_manager.get_api_key(cli_arg_key=cli_key)
            assert result == cli_key

    def test_get_api_key_from_env_var(self, config_manager):
        """get_api_key should return ENV variable API key when CLI arg not provided."""
        env_key = "env-provided-key"
        config_manager.init_config(api_key="config-key", format="json")

        with mock.patch.dict(os.environ, {"JULES_API_KEY": env_key}):
            result = config_manager.get_api_key(cli_arg_key=None)
            assert result == env_key

    def test_get_api_key_from_config(self, config_manager):
        """get_api_key should return config file API key when CLI and ENV not provided."""
        config_key = "config-file-key"
        config_manager.init_config(api_key=config_key, format="json")

        with mock.patch.dict(os.environ, {}, clear=True):
            result = config_manager.get_api_key(cli_arg_key=None)
            assert result == config_key

    def test_get_api_key_priority_order(self, config_manager):
        """get_api_key should follow priority: CLI > ENV > Config."""
        config_key = "config-key"
        env_key = "env-key"
        cli_key = "cli-key"

        config_manager.init_config(api_key=config_key, format="json")

        # CLI should override ENV
        with mock.patch.dict(os.environ, {"JULES_API_KEY": env_key}):
            result = config_manager.get_api_key(cli_arg_key=cli_key)
            assert result == cli_key

    def test_get_api_key_raises_error_when_no_key(self, config_manager):
        """get_api_key should raise ConfigurationError when no API key is available."""
        # Don't initialize config
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ConfigurationError, match="API key not found"):
                config_manager.get_api_key(cli_arg_key=None)

    def test_validate_config_with_valid_config(self, config_manager):
        """validate_config should return True for valid configuration."""
        config = {"api_key": "valid-key", "format": "json"}
        assert config_manager.validate_config(config) is True

    def test_validate_config_with_missing_api_key(self, config_manager):
        """validate_config should return False when api_key is missing."""
        config = {"format": "json"}
        assert config_manager.validate_config(config) is False

    def test_validate_config_with_invalid_format(self, config_manager):
        """validate_config should return False for invalid format."""
        config = {"api_key": "key", "format": "invalid"}
        assert config_manager.validate_config(config) is False
