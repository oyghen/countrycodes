"""Look up ISO 3166-1 country codes."""

__all__ = (
    "__version__",
    "Country",
    "CountryNotFoundError",
    "find_country",
    "get_country",
    "list_countries",
)

from importlib import metadata

from countrycodes.core import CountryNotFoundError, find_country, get_country
from countrycodes.country import Country, list_countries

__version__ = metadata.version(__name__)
