"""ISO 3166-1 country lookup API."""

__all__ = ("search_countries",)


from collections import defaultdict
from difflib import SequenceMatcher
from functools import cache

from countrycodes.country import Countries, Country, list_countries


def search_countries(query: str, *, limit: int | None = None) -> Countries:
    """Return exact matches or fuzzy matches ranked by name similarity.

    Queries match ISO alpha-2, alpha-3, and numeric codes, dial codes, and
    common, official, and short country names. Matching ignores case and
    surrounding or repeated whitespace. If there is no exact match, countries
    are ranked by name similarity, comparing single-word queries with
    individual name words. ``limit`` restricts the number of returned
    countries; it must be positive when provided. An empty query returns an
    empty tuple.
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
            names = (country.name, country.official_name, country.common_name)
            score = max(
                (
                    _name_similarity(normalized_query, name)
                    for name in names
                    if name is not None
                ),
                default=(0.0, 0.0),
            )
            scored_countries.append((score, country))
        matches = tuple(
            country
            for _, country in sorted(
                scored_countries,
                key=lambda match: match[0],
                reverse=True,
            )
        )

    return matches if limit is None else matches[:limit]


def _normalize(value: str) -> str:
    """Normalize a country query for matching."""
    return " ".join(value.casefold().split())


def _name_similarity(query: str, name: str) -> tuple[float, float]:
    """Score a query against a full name and its words, preferring word matches."""
    normalized_name = _normalize(name)
    full_name_score = SequenceMatcher(None, query, normalized_name).ratio()
    if " " in query:
        return full_name_score, full_name_score

    word_score = max(
        (
            SequenceMatcher(None, query, word).ratio()
            for word in normalized_name.split()
        ),
        default=full_name_score,
    )
    return word_score, full_name_score


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
