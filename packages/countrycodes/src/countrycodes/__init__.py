"""Look up ISO 3166-1 country codes."""

__all__ = (
    "__version__",
    "Country",
    "Countries",
    "country_name_similarity",
    "search_countries",
    "list_countries",
)

from importlib import metadata

from countrycodes.core import country_name_similarity, search_countries
from countrycodes.country import Countries, Country, list_countries

__version__ = metadata.version(__name__)
