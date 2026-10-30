"""Tests for the countrycodes library."""

from importlib import metadata
from types import ModuleType

import countrycodes as cc
import pytest


def test_project_name(project_name: str, project_pkg: ModuleType) -> None:
    assert project_pkg.__name__ == project_name


def test_project_version(project_name: str, project_pkg: ModuleType) -> None:
    assert project_pkg.__version__ == metadata.version(project_name)


def test_lookup_by_each_code_format() -> None:
    expected = cc.Country(
        alpha2="US",
        alpha3="USA",
        numeric="840",
        continent="North America",
        name="United States",
        official_name="United States of America",
        dial_code="+1",
    )

    assert cc.search_countries("US") == (expected,)
    assert cc.search_countries("usa") == (expected,)
    assert cc.search_countries(" 840 ") == (expected,)
    assert cc.search_countries("GB")[0].continent == "Europe"
    assert cc.search_countries("GB")[0].dial_code == "+44"
    assert cc.search_countries("+46")[0].alpha2 == "SE"
    assert cc.search_countries("JP")[0].continent == "Asia"
    assert cc.search_countries("AQ")[0].continent == "Antarctica"
    assert cc.search_countries("AQ")[0].dial_code is None


def test_lookup_by_name_and_whitespace() -> None:
    assert cc.search_countries("  united   states  ")[0].alpha2 == "US"
    assert cc.search_countries("United States of America")[0].alpha2 == "US"


def test_lookup_by_fuzzy_country_name() -> None:
    matches = cc.search_countries("Untied States")

    assert len(matches) == 249
    assert matches[0].alpha2 == "US"


def test_fuzzy_lookup_combines_word_and_full_name_scores() -> None:
    matches = cc.search_countries("Untied")

    assert matches[0].alpha2 == "US"
    united_states = cc.search_countries("US")[0]
    assert cc.country_name_similarity("Untied", united_states) == pytest.approx(
        (5 / 6 + 5 / 13) / 2
    )


def test_fuzzy_similarity_prefers_transposed_word_over_partial_overlap() -> None:
    united_states = cc.search_countries("US")[0]
    niger = cc.search_countries("NE")[0]

    assert cc.country_name_similarity("Untied", united_states) > (
        cc.country_name_similarity("Untied", niger)
    )
    assert cc.search_countries("Untied")[0].alpha2 == "US"


def test_fuzzy_lookup_matches_multiword_typos() -> None:
    assert cc.search_countries("Untied States")[0].alpha2 == "US"


def test_single_word_query_returns_names_containing_the_word() -> None:
    matches = cc.search_countries("United", limit=3)

    assert tuple(country.alpha2 for country in matches) == ("US", "GB", "AE")


def test_fuzzy_similarity_uses_displayed_name_not_official_name() -> None:
    mexico = cc.search_countries("MX")[0]
    tanzania = cc.search_countries("TZ")[0]

    assert cc.country_name_similarity("United", mexico) < cc.country_name_similarity(
        "United", tanzania
    )


def test_fuzzy_lookup_orders_equal_scores_by_alpha2_code() -> None:
    tied_codes = {"BZ", "BR", "ZM"}
    matches = cc.search_countries("zzzzzzzz")
    matched_codes = [
        country.alpha2 for country in matches if country.alpha2 in tied_codes
    ]

    assert matched_codes == sorted(tied_codes)


def test_search_countries_returns_empty_tuple_for_empty_query() -> None:
    assert cc.search_countries("") == ()


def test_search_countries_limits_ranked_matches() -> None:
    matches = cc.search_countries("Untied States", limit=3)

    assert len(matches) == 3
    assert matches[0].alpha2 == "US"


def test_country_name_similarity_returns_combined_score() -> None:
    united_states = cc.search_countries("US")[0]

    assert cc.country_name_similarity("Untied", united_states) == pytest.approx(
        (5 / 6 + 5 / 13) / 2
    )
    assert cc.country_name_similarity("", united_states) == 0.0


def test_search_countries_rejects_non_positive_limit() -> None:
    with pytest.raises(ValueError, match="limit must be positive"):
        cc.search_countries("US", limit=0)


def test_search_countries_returns_all_exact_dial_code_matches() -> None:
    matches = cc.search_countries("+1")

    assert len(matches) > 1
    assert {country.dial_code for country in matches} == {"+1"}


def test_list_countries_returns_complete_sorted_registry() -> None:
    countries = cc.list_countries()

    assert cc.list_countries() is countries
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
