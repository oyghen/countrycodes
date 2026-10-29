"""Core ISO 3166-1 country data and lookup API."""

__all__ = (
    "Country",
    "CountryNotFoundError",
    "find_country",
    "get_country",
    "list_countries",
)


import json
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import cache
from importlib.resources import files
from typing import Any


class CountryNotFoundError(LookupError):
    """Raised when a country query does not match the registry."""


@dataclass(frozen=True, slots=True)
class Country:
    """An ISO 3166-1 country or territory with geographic and dialing data."""

    alpha2: str
    alpha3: str
    numeric: str
    continent: str
    name: str
    official_name: str | None = None
    common_name: str | None = None
    dial_code: str | None = None


def list_countries() -> tuple[Country, ...]:
    """Return all countries and territories, sorted by alpha-2 code."""
    countries, _ = _registry()
    return countries


def find_country(query: str) -> Country | None:
    """Return the matching country, or ``None`` if the query is not found.

    Queries match ISO alpha-2, alpha-3, and numeric codes, dial codes, and
    common, official, and short country names. Matching ignores case and
    surrounding or repeated whitespace. If there is no exact match, a
    sufficiently similar country name is matched instead.
    """
    countries, index = _registry()
    matches = index.get(_normalize(query), ())
    unique_matches = tuple(dict.fromkeys(matches))
    if len(unique_matches) > 1:
        raise ValueError(f"Country query is ambiguous: {query!r}")
    if unique_matches:
        return unique_matches[0]
    return _find_fuzzy_country(query, countries)


def get_country(query: str) -> Country:
    """Return the matching country or raise ``CountryNotFoundError``."""
    country = find_country(query)
    if country is None:
        raise CountryNotFoundError(f"No country matches {query!r}")
    return country


def _normalize(value: str) -> str:
    return " ".join(value.casefold().split())


def _find_fuzzy_country(query: str, countries: tuple[Country, ...]) -> Country | None:
    normalized_query = _normalize(query)
    if not normalized_query:
        return None

    best_score = 0.8
    best_matches: set[Country] = set()
    for country in countries:
        names = (country.name, country.official_name, country.common_name)
        score = max(
            (
                SequenceMatcher(None, normalized_query, _normalize(name)).ratio()
                for name in names
                if name is not None
            ),
            default=0.0,
        )
        if score > best_score:
            best_score = score
            best_matches = {country}
        elif score == best_score:
            best_matches.add(country)

    if len(best_matches) > 1:
        raise ValueError(f"Country query is ambiguous: {query!r}")
    return next(iter(best_matches), None)


@cache
def _registry() -> tuple[tuple[Country, ...], dict[str, tuple[Country, ...]]]:
    data_file = files("countrycodes").joinpath("data/iso_3166-1.json")
    with data_file.open(encoding="utf-8") as file:
        records: list[dict[str, Any]] = json.load(file)
    countries = tuple(Country(**record) for record in records)
    countries = tuple(sorted(countries, key=lambda country: country.alpha2))

    index: dict[str, list[Country]] = defaultdict(list)
    for country in countries:
        for value in (
            country.alpha2,
            country.alpha3,
            country.numeric,
            country.dial_code,
            country.name,
            country.official_name,
            country.common_name,
        ):
            if value is not None:
                index[_normalize(value)].append(country)

    return countries, {key: tuple(matches) for key, matches in index.items()}
