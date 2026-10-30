"""Tests for the countrycodes library."""

from importlib import metadata
from types import ModuleType

import pytest
from countrycodes import Country, list_countries, search_countries


def test_project_name(project_name: str, project_pkg: ModuleType) -> None:
    assert project_pkg.__name__ == project_name


def test_project_version(project_name: str, project_pkg: ModuleType) -> None:
    assert project_pkg.__version__ == metadata.version(project_name)


def test_lookup_by_each_code_format() -> None:
    expected = Country(
        alpha2="US",
        alpha3="USA",
        numeric="840",
        continent="North America",
        name="United States",
        official_name="United States of America",
        dial_code="+1",
    )

    assert search_countries("US") == (expected,)
    assert search_countries("usa") == (expected,)
    assert search_countries(" 840 ") == (expected,)
    assert search_countries("GB")[0].continent == "Europe"
    assert search_countries("GB")[0].dial_code == "+44"
    assert search_countries("+46")[0].alpha2 == "SE"
    assert search_countries("JP")[0].continent == "Asia"
    assert search_countries("AQ")[0].continent == "Antarctica"
    assert search_countries("AQ")[0].dial_code is None


def test_lookup_by_name_and_whitespace() -> None:
    assert search_countries("  united   states  ")[0].alpha2 == "US"
    assert search_countries("United States of America")[0].alpha2 == "US"


def test_lookup_by_fuzzy_country_name() -> None:
    matches = search_countries("Untied States")

    assert len(matches) == 249
    assert matches[0].alpha2 == "US"


def test_fuzzy_lookup_matches_single_word_typos_within_country_name() -> None:
    assert search_countries("Untied")[0].alpha2 == "US"


def test_fuzzy_lookup_matches_partial_country_name() -> None:
    assert search_countries("United")[0].alpha2 == "US"


def test_search_countries_returns_empty_tuple_for_empty_query() -> None:
    assert search_countries("") == ()


def test_search_countries_limits_ranked_matches() -> None:
    matches = search_countries("Untied States", limit=3)

    assert len(matches) == 3
    assert matches[0].alpha2 == "US"


def test_search_countries_rejects_non_positive_limit() -> None:
    with pytest.raises(ValueError, match="limit must be positive"):
        search_countries("US", limit=0)


def test_search_countries_returns_all_exact_dial_code_matches() -> None:
    matches = search_countries("+1")

    assert len(matches) > 1
    assert {country.dial_code for country in matches} == {"+1"}


def test_list_countries_returns_complete_sorted_registry() -> None:
    countries = list_countries()

    assert list_countries() is countries
    assert len(countries) == 249
    assert {country.continent for country in countries} == {
        "Africa",
        "Antarctica",
        "Asia",
        "Europe",
        "North America",
        "Oceania",
        "South America",
    }
    assert tuple(country.alpha2 for country in countries) == tuple(
        sorted(country.alpha2 for country in countries)
    )
    assert len({country.alpha2 for country in countries}) == 249
    assert all(
        country.dial_code is None or country.dial_code.startswith("+")
        for country in countries
    )
