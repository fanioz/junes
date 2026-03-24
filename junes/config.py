"""Configuration management for Jules CLI."""

import os
import sys
from pathlib import Path

from junes.exceptions import ConfigurationError


class ConfigManager:
    """Manages configuration for the Jules CLI."""

    VALID_FORMATS = {"json", "table", "plain"}

    def __init__(self):
        """Initialize the ConfigManager."""
        self.config_dir = Path.home() / ".junes"
        self.config_file = self.config_dir / "config.toml"

    def init_config(self, api_key: str, format: str = "plain") -> None:
        """
        Initialize the configuration file.

        Args:
            api_key: The API key to store
            format: The output format (json, table, plain)

        Raises:
            ConfigurationError: If format is invalid
        """
        if format not in self.VALID_FORMATS:
            raise ConfigurationError(f"Invalid format: {format}. Must be one of {self.VALID_FORMATS}")

        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Write config file
        config_data = {"api_key": api_key, "format": format}

        try:
            import tomli_w
        except ImportError:
            tomli_w = None

        if tomli_w is not None:
            with open(self.config_file, "wb") as f:
                tomli_w.dump(config_data, f)
        else:
            # Fallback: write simple TOML manually, with escaping
            with open(self.config_file, "w", encoding="utf-8") as f:
                # Escape special characters for TOML basic string format
                escaped_api_key = (
                    api_key.replace("\\", "\\\\")
                    .replace("\"", "\\\"")
                    .replace("\b", "\\b")
                    .replace("\t", "\\t")
                    .replace("\n", "\\n")
                    .replace("\f", "\\f")
                    .replace("\r", "\\r")
                )
                f.write(f'api_key = "{escaped_api_key}"\n')
                f.write(f'format = "{format}"\n')

    def load_config(self) -> dict:
        """
        Load the configuration file.

        Returns:
            dict: Configuration dictionary

        Raises:
            ConfigurationError: If config file not found or invalid
        """
        if not self.config_file.exists():
            raise ConfigurationError("Configuration file not found. Run 'jules config init' first.")

        if sys.version_info >= (3, 11):
            import tomllib
        else:
            try:
                import tomli as tomllib
            except ImportError:
                import tomli as tomllib

        try:
            with open(self.config_file, "rb") as f:
                config = tomllib.load(f)
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

        return config

    def get_api_key(self, cli_arg_key: str = None) -> str:
        """
        Get API key with priority: CLI arg > ENV var > Config file.

        Args:
            cli_arg_key: API key provided via CLI argument

        Returns:
            str: The API key to use

        Raises:
            ConfigurationError: If no API key is available
        """
        # Priority 1: CLI argument
        if cli_arg_key:
            return cli_arg_key

        # Priority 2: Environment variable
        env_key = os.environ.get("JULES_API_KEY")
        if env_key:
            return env_key

        # Priority 3: Config file
        try:
            config = self.load_config()
            if "api_key" in config:
                return config["api_key"]
        except ConfigurationError:
            pass

        raise ConfigurationError(
            "API key not found. Provide via --api-key, JULES_API_KEY env var, or config file."
        )

    def validate_config(self, config: dict) -> bool:
        """
        Validate a configuration dictionary.

        Args:
            config: Configuration dictionary to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(config, dict):
            return False

        # Check required fields
        if "api_key" not in config:
            return False

        # Validate format if present
        if "format" in config:
            if config["format"] not in self.VALID_FORMATS:
                return False

        return True
