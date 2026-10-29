"""Tests for the countrycodes library."""

from importlib import metadata
from types import ModuleType

import pytest
from countrycodes import (
    Country,
    CountryNotFoundError,
    find_country,
    get_country,
    list_countries,
)


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

    assert get_country("US") == expected
    assert get_country("usa") == expected
    assert get_country(" 840 ") == expected
    assert get_country("GB").continent == "Europe"
    assert get_country("GB").dial_code == "+44"
    assert get_country("JP").continent == "Asia"
    assert get_country("AQ").continent == "Antarctica"
    assert get_country("AQ").dial_code is None


def test_lookup_by_name_and_whitespace() -> None:
    assert get_country("  united   states  ").alpha2 == "US"
    assert get_country("United States of America").alpha2 == "US"


def test_find_country_returns_none_for_unknown_query() -> None:
    assert find_country("Atlantis") is None


def test_get_country_raises_for_unknown_query() -> None:
    with pytest.raises(CountryNotFoundError, match="Atlantis"):
        get_country("Atlantis")


def test_list_countries_returns_complete_sorted_registry() -> None:
    countries = list_countries()

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
    assert tuple(country.name.casefold() for country in countries) == tuple(
        sorted(country.name.casefold() for country in countries)
    )
    assert len({country.alpha2 for country in countries}) == 249
    assert all(
        country.dial_code is None or country.dial_code.startswith("+")
        for country in countries
    )
