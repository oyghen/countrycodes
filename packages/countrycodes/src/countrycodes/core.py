"""ISO 3166-1 country lookup API."""

__all__ = ("find_country",)


from collections import defaultdict
from difflib import SequenceMatcher
from functools import cache

from countrycodes.country import Countries, Country, list_countries


def find_country(query: str) -> Country | None:
    """Return the matching country, or ``None`` if the query is not found.

    Queries match ISO alpha-2, alpha-3, and numeric codes, dial codes, and
    common, official, and short country names. Matching ignores case and
    surrounding or repeated whitespace. If there is no exact match, a
    sufficiently similar country name is matched instead.
    """
    countries = list_countries()
    index = _country_index(countries)
    matches = index.get(_normalize(query), ())
    unique_matches = tuple(dict.fromkeys(matches))
    if len(unique_matches) > 1:
        raise ValueError(f"Country query is ambiguous: {query!r}")
    if unique_matches:
        return unique_matches[0]
    return _find_fuzzy_country(query, countries)


def _normalize(value: str) -> str:
    """Normalize a country query for matching."""
    return " ".join(value.casefold().split())


def _find_fuzzy_country(query: str, countries: Countries) -> Country | None:
    """Return the closest matching country name, if any."""
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
