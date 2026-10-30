"""Command-line interface for country code lookups."""

import json
from dataclasses import asdict
from typing import Annotated, Literal

import countrycodes as cc
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
) -> None:
    pkg_name = cc.__name__
    pkg_version = typer.style(cc.__version__, fg=typer.colors.CYAN)

    if version:
        typer.echo(f"{pkg_name} {pkg_version}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        typer.echo(f"{pkg_name} {pkg_version} ready. See --help for usage.")
        raise typer.Exit()


@app.command()
def lookup(
    query: Annotated[str, typer.Argument(help="Country name, ISO code, or dial code.")],
    output_format: Annotated[
        Literal["text", "json"],
        typer.Option("--format", help="Output format."),
    ] = "text",
    limit: Annotated[
        int,
        typer.Option("--limit", min=1, help="Maximum number of matches to show."),
    ] = 5,
) -> None:
    """Look up a country by name, ISO code, or dial code."""
    countries: tuple[cc.Country, ...] = (
        tuple(
            country
            for country in cc.list_countries()
            if country.dial_code == query.strip()
        )
        if query.strip().startswith("+")
        else ()
    )
    is_dial_code_lookup = bool(countries)
    has_more_matches = False
    is_fuzzy_lookup = False
    normalized_query = _normalize_query(query)

    if is_dial_code_lookup:
        has_more_matches = len(countries) > limit
        countries = countries[:limit]
    else:
        matches = cc.search_countries(query, limit=limit + 1)
        if not matches:
            typer.echo(f"No country matches {query!r}", err=True)
            raise typer.Exit(1)
        has_more_matches = len(matches) > limit
        countries = matches[:limit]
        first_country = countries[0]
        is_fuzzy_lookup = normalized_query not in {
            _normalize_query(value)
            for value in (
                first_country.alpha2,
                first_country.alpha3,
                first_country.numeric,
                first_country.dial_code,
                first_country.name,
                first_country.official_name,
                first_country.common_name,
            )
            if value is not None
        }

    if not countries:
        typer.echo(f"No country matches {query!r}", err=True)
        raise typer.Exit(1)

    if output_format == "json":
        first_country = next(iter(countries), None)
        result = (
            [asdict(country) for country in countries]
            if first_country is None or len(countries) > 1
            else asdict(first_country)
        )
        typer.echo(json.dumps(result, ensure_ascii=False))
    else:
        table = Table(show_lines=False)
        table.add_column("Alpha-2")
        table.add_column("Alpha-3")
        table.add_column("Numeric")
        table.add_column("Dial Code")
        table.add_column("Continent")
        table.add_column("Country")
        if is_fuzzy_lookup:
            table.add_column("Similarity", justify="right", min_width=10, no_wrap=True)
        for country in countries:
            row = (
                country.alpha2,
                country.alpha3,
                country.numeric,
                country.dial_code or "",
                country.continent,
                country.name,
            )
            if is_fuzzy_lookup:
                score = cc.country_name_similarity(query, country)
                row += (f"{score:.0%}",)
            table.add_row(*row)
        Console().print(table)
        if has_more_matches:
            Console().print(f"[dim]Showing only the top {limit} matches.[/dim]")


def _normalize_query(value: str) -> str:
    """Normalize text using the same whitespace and case rules as the library."""
    return " ".join(value.casefold().split())


@app.command(name="list")
def list_countries(
    output_format: Annotated[
        Literal["text", "json"],
        typer.Option("--format", help="Output format."),
    ] = "text",
) -> None:
    """List all countries and territories."""
    countries = cc.list_countries()
    if output_format == "json":
        typer.echo(
            json.dumps(
                [asdict(country) for country in countries],
                ensure_ascii=False,
            )
        )
    else:
        table = Table(
            "#",
            "Alpha-2",
            "Alpha-3",
            "Numeric",
            "Dial Code",
            "Continent",
            "Country",
            show_lines=False,
        )
        for index, country in enumerate(countries, start=1):
            table.add_row(
                str(index),
                country.alpha2,
                country.alpha3,
                country.numeric,
                country.dial_code or "",
                country.continent,
                country.name,
            )
        Console().print(table)
