"""Module for parsing maze configuration files."""

import sys
from typing import Any, Optional


class ConfigParser:
    """Parses and provides access to maze configuration parameters.

    Reads configuration from a file with key=value pairs, supporting
    comments (lines starting with #) and blank lines.
    """

    def __init__(self, filepath: str):
        """Initialize the parser and load configuration from file.

        Args:
            filepath: Path to the configuration file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
        """
        self.filepath = filepath
        self.config: dict[str, str] = {}
        self.parse()

    def parse(self) -> None:
        """Parse the configuration file and populate the config dictionary.

        Ignores blank lines and lines starting with '#' (comments).

        Raises:
            FileNotFoundError: If the configuration file cannot be opened.
        """
        try:
            with open(self.filepath, "r") as file:
                for line in file:
                    if line.startswith("#"):
                        continue
                    if not line:
                        continue
                    if "=" in line:
                        par = line.split("=", 1)
                        self.config[par[0].strip()] = par[1].strip()
                    else:
                        raise ValueError()

        except FileNotFoundError:
            print(f"Error: Config file '{self.filepath}' not found!")
            raise
        except ValueError:
            print(f"Error: Invalid format in {self.filepath},\
                   expected format 'Key = Value'")
            raise

    def get(self, key: str, default: Optional[Any] = None) -> str | None:
        """Get a configuration value as a string.

        Args:
            key: The configuration key to retrieve.
            default: Default value if key not found (default: None).

        Returns:
            The configuration value or the default value if not found.
        """
        return self.config.get(key, default)

    def get_int(self, key: str) -> int:
        """Get a configuration value as an integer.

        Args:
            key: The configuration key to retrieve.

        Returns:
            The integer value of the configuration parameter.

        Raises:
            KeyError: If the key is not found in configuration.
            ValueError: If the value cannot be converted to an integer.
        """
        value = self.config.get(key)
        if value is None or int(value) < 0:
            raise KeyError(f"Missing key: {key}")
        return int(value)

    def get_bool(self, key: str) -> bool:
        """Get a configuration value as a boolean.

        Args:
            key: The configuration key to retrieve.

        Returns:
            True if value is 'true' (case-insensitive), False otherwise.

        Raises:
            KeyError: If the key is not found in configuration.
        """
        value = self.config.get(key)
        if value:
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
        else:
            raise KeyError(f"Missing key: {key}")
        return False

    def get_tuple(self, key: str) -> tuple[int, int]:
        """Get a configuration value as a tuple of two integers.

        Args:
            key: The configuration key to retrieve (expects format: 'x,y').

        Returns:
            A tuple of two integers parsed from comma-separated values.

        Raises:
            KeyError: If the key is not found in configuration.
            ValueError: If the value cannot be parsed as two integers.
        """
        try:
            value = self.config.get(key)
            if value is None:
                raise KeyError(f"Missing key: {key}")
            parts = value.split(",")
            return (int(parts[0].strip()), int(parts[1].strip()))
        except IndexError:
            print("Config File Error: list index out of range")
            sys.exit(1)
