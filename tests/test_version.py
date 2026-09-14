"""Unit tests for the __version__ fallback."""

import importlib
from importlib.metadata import PackageNotFoundError
from unittest.mock import patch

import espn_sports_api


def test_version_falls_back_when_package_not_installed():
    try:
        with patch("importlib.metadata.version", side_effect=PackageNotFoundError):
            importlib.reload(espn_sports_api)
        assert espn_sports_api.__version__ == "0.4.2"
    finally:
        importlib.reload(espn_sports_api)
