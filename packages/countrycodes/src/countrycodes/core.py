"""ISO 3166-1 country lookup API."""

__all__ = ("country_name_similarity", "search_countries")


from collections import defaultdict
from functools import cache

from countrycodes.country import Countries, Country, list_countries


def search_countries(query: str, *, limit: int | None = None) -> Countries:
    """Return exact matches or fuzzy matches ranked by name similarity.

    Queries match ISO alpha-2, alpha-3, and numeric codes, dial codes, and
    common, official, and short country names. Matching ignores case and
    surrounding or repeated whitespace. If there is no exact match, countries
    are ranked using the displayed country name's combined word-level and
    full-name similarity score; equal scores are ordered by alpha-2 code.
    ``limit`` restricts the number of returned countries; it must be positive
    when provided. An empty query returns an empty tuple.
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
    """Return the combined word-level and full-name similarity score."""
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
    """Return combined word and full-name similarity for the displayed name."""
    word_score, full_name_score = _name_similarity(query, country.name)
    return (word_score + full_name_score) / 2


def _name_similarity(query: str, name: str) -> tuple[float, float]:
    """Return word-level and full-name similarity scores."""
    normalized_name = _normalize(name)
    full_name_score = _edit_similarity(query, normalized_name)
    if " " in query:
        return full_name_score, full_name_score

    word_score = max(
        (_edit_similarity(query, word) for word in normalized_name.split()),
        default=full_name_score,
    )
    return word_score, full_name_score


def _edit_similarity(left: str, right: str) -> float:
    """Return normalized edit similarity, counting adjacent transpositions."""
    if not left or not right:
        return float(left == right)

    distances = [list(range(len(right) + 1)) for _ in range(len(left) + 1)]
    for left_index in range(len(left) + 1):
        distances[left_index][0] = left_index
    for right_index in range(len(right) + 1):
        distances[0][right_index] = right_index

    for left_index in range(1, len(left) + 1):
        for right_index in range(1, len(right) + 1):
            cost = left[left_index - 1] != right[right_index - 1]
            distances[left_index][right_index] = min(
                distances[left_index - 1][right_index] + 1,
                distances[left_index][right_index - 1] + 1,
                distances[left_index - 1][right_index - 1] + cost,
            )
            if (
                left_index > 1
                and right_index > 1
                and left[left_index - 1] == right[right_index - 2]
                and left[left_index - 2] == right[right_index - 1]
            ):
                distances[left_index][right_index] = min(
                    distances[left_index][right_index],
                    distances[left_index - 2][right_index - 2] + 1,
                )

    distance = distances[-1][-1]
    return 1 - distance / max(len(left), len(right))
