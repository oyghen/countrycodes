<div align="center">

# countrycodes-cli

[![GitHub](https://img.shields.io/badge/GitHub-code-blue)](https://github.com/oyghen/countrycodes/tree/main/packages/countrycodes-cli)
[![PyPI](https://img.shields.io/pypi/v/countrycodes-cli?label=PyPI)](https://pypi.org/project/countrycodes-cli/)
[![License](https://img.shields.io/badge/License-BSD--3--Clause-blue)](https://github.com/oyghen/countrycodes/blob/main/packages/countrycodes-cli/LICENSE)
[![CI](https://github.com/oyghen/countrycodes/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/oyghen/countrycodes/actions/workflows/ci.yml)

</div>

Command-line interface for the [`countrycodes`](https://pypi.org/project/countrycodes/)
ISO 3166-1 lookup library.

## Installation

Install as a command-line tool with [uv](https://docs.astral.sh/uv/):

```console
uv tool install countrycodes-cli
```

Or install into the active Python environment:

```console
python -m pip install countrycodes-cli
```

Requires Python 3.11 or newer. The library dependency is installed automatically.

## Usage

Look up a country by code or name:

```console
countrycodes lookup US
countrycodes lookup "United Kingdom"
countrycodes lookup +1
```

Lookups are displayed as a table by default. Choose JSON output or list all
countries:

```console
countrycodes lookup GBR --format json
countrycodes list
countrycodes list --format json
```

Dial-code lookups display every country or territory sharing that code. In
JSON, dial-code lookups return an array; lookups by country name or ISO code
return a single record. The default list is rendered as a table sorted by
alpha-2 code, with a row number, and JSON list output is an unnumbered array.
Country records include the international dial code when available.

See all options with:

```console
countrycodes --help
```

## License

The CLI code is licensed under BSD 3-Clause. The separately distributed
`countrycodes` library includes ISO registry data under LGPL-2.1-or-later and
continent assignments from GeoNames under CC BY 4.0; installing the CLI
installs that library as a dependency.
