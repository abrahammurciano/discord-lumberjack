"""
.. include:: ../README.md
"""
import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    import toml

    __version__ = (
        toml.load("pyproject.toml")
        .get("tool", {})
        .get("post-install", {})
        .get("version", "unknown")
        + "-dev"
    )

from . import handlers
from . import message_creators
