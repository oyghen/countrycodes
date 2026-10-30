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
) -> None:
    """Look up a country by name, ISO code, or dial code."""
    countries = (
        tuple(
            country
            for country in cc.list_countries()
            if country.dial_code == query.strip()
        )
        if query.strip().startswith("+")
        else ()
    )
    is_dial_code_lookup = bool(countries)

    if not countries:
        country = cc.find_country(query)
        if country is None:
            typer.echo(f"No country matches {query!r}", err=True)
            raise typer.Exit(1)
        countries = (country,)

    if output_format == "json":
        result = (
            [asdict(country) for country in countries]
            if is_dial_code_lookup
            else asdict(countries[0])
        )
        typer.echo(json.dumps(result, ensure_ascii=False))
    else:
        table = Table(
            "Alpha-2",
            "Alpha-3",
            "Numeric",
            "Dial Code",
            "Continent",
            "Country",
            show_lines=False,
        )
        for country in countries:
            table.add_row(
                country.alpha2,
                country.alpha3,
                country.numeric,
                country.dial_code or "",
                country.continent,
                country.name,
            )
        Console().print(table)


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
