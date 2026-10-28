"""Tests for the countrycodes CLI package."""

import json
import subprocess
from importlib import metadata
from types import ModuleType

import countrycodes
from countrycodes_cli.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_project_name(project_name: str, project_pkg: ModuleType) -> None:
    assert project_pkg.__name__ == project_name


def test_project_version(project_pkg: ModuleType, distribution_name: str) -> None:
    assert project_pkg.__version__ == metadata.version(distribution_name)


def test_library_name() -> None:
    assert countrycodes.__name__ == "countrycodes"


def test_version_command_prints_library_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == f"countrycodes {metadata.version('countrycodes')}"


def test_no_command_prints_ready_message() -> None:
    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "countrycodes" in result.stdout
    assert "ready. See --help for usage." in result.stdout


def test_lookup_command_prints_text() -> None:
    result = runner.invoke(app, ["lookup", "gb"])

    assert result.exit_code == 0
    assert "#" not in result.stdout
    assert "Alpha-2" in result.stdout
    assert "Alpha-3" in result.stdout
    assert "Numeric" in result.stdout
    assert "Continent" in result.stdout
    assert "Country" in result.stdout
    assert "GB" in result.stdout
    assert "GBR" in result.stdout
    assert "826" in result.stdout
    assert "Europe" in result.stdout
    assert "United Kingdom" in result.stdout


def test_lookup_command_prints_json() -> None:
    result = runner.invoke(app, ["lookup", "JP", "--format", "json"])

    assert result.exit_code == 0
    country = json.loads(result.stdout)

    assert country["alpha2"] == "JP"
    assert country["alpha3"] == "JPN"
    assert country["numeric"] == "392"
    assert country["continent"] == "Asia"


def test_unknown_lookup_reports_error() -> None:
    result = runner.invoke(app, ["lookup", "Atlantis"])

    assert result.exit_code == 1
    assert "No country matches 'Atlantis'" in result.output


def test_console_entry_point_lists_countries() -> None:
    result = subprocess.run(
        ["countrycodes", "list", "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
    )
    countries = json.loads(result.stdout)

    assert len(countries) == 249
    assert [country["alpha2"] for country in countries[:3]] == ["AD", "AE", "AF"]
    assert [country["continent"] for country in countries[:3]] == [
        "Europe",
        "Asia",
        "Asia",
    ]
    assert [country["alpha2"] for country in countries] == sorted(
        country["alpha2"] for country in countries
    )


def test_list_text_is_alpha2_sorted_and_numbered() -> None:
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "Alpha-2" in result.stdout
    assert "Alpha-3" in result.stdout
    assert "Numeric" in result.stdout
    assert "Continent" in result.stdout
    assert "Country" in result.stdout
    assert "Europe" in result.stdout
    assert "Andorra" in result.stdout
    assert "Afghanistan" in result.stdout
    assert "Zimbabwe" in result.stdout
    assert (
        result.stdout.index("AD")
        < result.stdout.index("AE")
        < result.stdout.index("AF")
    )
    assert "249" in result.stdout
