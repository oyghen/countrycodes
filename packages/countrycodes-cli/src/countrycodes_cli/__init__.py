"""Command-line application for the countrycodes library."""

__all__ = ["__version__"]

from importlib import metadata

__version__ = metadata.version(__name__)
