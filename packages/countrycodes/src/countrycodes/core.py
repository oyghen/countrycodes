"""ISO 3166-1 country lookup API."""

__all__ = ("country_name_similarity", "search_countries")


from collections import defaultdict
from difflib import SequenceMatcher
from functools import cache

from countrycodes.country import Countries, Country, list_countries


def search_countries(query: str, *, limit: int | None = None) -> Countries:
    """Return exact matches or fuzzy matches ranked by name similarity.

    Queries match ISO alpha-2, alpha-3, and numeric codes, dial codes, and
    common, official, and short country names. Matching ignores case and
    surrounding or repeated whitespace. If there is no exact match, countries
    are ranked by comparing the query with each full country name; equal
    scores are ordered by alpha-2 code. ``limit`` restricts the number of
    returned countries; it must be positive when provided. An empty query
    returns an empty tuple.
    """
    if limit is not None and limit < 1:
        raise ValueError("limit must be positive")

    normalized_query = _normalize(query)
    if not normalized_query:
        return ()

    countries = list_countries()
    exact_matches = _country_index(countries).get(normalized_query, ())
    if exact_matches:
        matches = exact_matches
    else:
        scored_countries = []
        for country in countries:
            scored_countries.append(
                (_country_name_similarity(normalized_query, country), country)
            )
        matches = tuple(
            country
            for _, country in sorted(
                scored_countries,
                key=lambda match: (
                    -match[0],
                    match[1].alpha2,
                ),
            )
        )

    return matches if limit is None else matches[:limit]


def country_name_similarity(query: str, country: Country) -> float:
    """Return the best full-name similarity score for a query and country."""
    normalized_query = _normalize(query)
    if not normalized_query:
        return 0.0
    return _country_name_similarity(normalized_query, country)


def _normalize(value: str) -> str:
    """Normalize a country query for matching."""
    return " ".join(value.casefold().split())


@cache
def _country_index(countries: Countries) -> dict[str, Countries]:
    """Build the cached index of country codes and names."""
    index: dict[str, list[Country]] = defaultdict(list)
    for country in countries:
        search_terms = (
            country.alpha2,
            country.alpha3,
            country.numeric,
            country.dial_code,
            country.name,
            country.official_name,
            country.common_name,
        )
        for value in search_terms:
            if value is not None:
                index[_normalize(value)].append(country)

    return {key: tuple(matches) for key, matches in index.items()}


def _country_name_similarity(query: str, country: Country) -> float:
    """Return a country's best similarity score across its names."""
    names = (country.name, country.official_name, country.common_name)
    return max(
        (_name_similarity(query, name) for name in names if name is not None),
        default=0.0,
    )


def _name_similarity(query: str, name: str) -> float:
    """Score a query against the complete country name."""
    normalized_name = _normalize(name)
    return SequenceMatcher(None, query, normalized_name).ratio()
