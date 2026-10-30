"""Tests for the countrycodes library."""

from importlib import metadata
from types import ModuleType

from countrycodes import Country, find_country, list_countries


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

    assert find_country("US") == expected
    assert find_country("usa") == expected
    assert find_country(" 840 ") == expected
    assert find_country("GB").continent == "Europe"
    assert find_country("GB").dial_code == "+44"
    assert find_country("+46").alpha2 == "SE"
    assert find_country("JP").continent == "Asia"
    assert find_country("AQ").continent == "Antarctica"
    assert find_country("AQ").dial_code is None


def test_lookup_by_name_and_whitespace() -> None:
    assert find_country("  united   states  ").alpha2 == "US"
    assert find_country("United States of America").alpha2 == "US"


def test_lookup_by_fuzzy_country_name() -> None:
    assert find_country("Untied States").alpha2 == "US"


def test_find_country_returns_none_for_unknown_query() -> None:
    assert find_country("Atlantis") is None


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
