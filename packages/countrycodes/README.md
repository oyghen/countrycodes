<div align="center">

# countrycodes

[![GitHub](https://img.shields.io/badge/GitHub-code-blue)](https://github.com/oyghen/countrycodes/tree/main/packages/countrycodes)
[![PyPI](https://img.shields.io/pypi/v/countrycodes?label=PyPI)](https://pypi.org/project/countrycodes/)
[![License](https://img.shields.io/badge/License-BSD--3--Clause%20%2B%20LGPL--2.1--or--later%20%2B%20CC--BY--4.0-blue)](https://github.com/oyghen/countrycodes/blob/main/packages/countrycodes/LICENSES/iso-codes.NOTICE)
[![CI](https://github.com/oyghen/countrycodes/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/oyghen/countrycodes/actions/workflows/ci.yml)

</div>

`countrycodes` is a dependency-free Python library for looking up all 249
ISO 3166-1 countries and territories, including continent assignments and
international dial codes where available.

## Installation

```console
pip install countrycodes
```

Requires Python 3.11 or newer.

## Usage

```python
import countrycodes as cc

united_states = cc.search_countries("us")[0]
print(united_states.alpha3)  # USA
print(united_states.numeric)  # 840
print(united_states.dial_code)  # +1

united_kingdom = cc.search_countries("United Kingdom")[0]
print(united_kingdom.alpha2)  # GB

typo_tolerant_match = cc.search_countries("Untied States")[0]
print(typo_tolerant_match.alpha2)  # US

print(len(cc.list_countries()))  # 249
```

Lookups accept alpha-2, alpha-3, and numeric codes, dial codes, and display
names. A display name uses `common_name` when available and otherwise `name`.
Matching is case-insensitive and ignores surrounding or repeated whitespace.
If there is no exact match, countries are returned in name similarity order,
even if the similarity is low. The similarity score combines word-level and
full-name matches equally. Exact shared dial codes return every matching
country.
`list_countries` returns records sorted by alpha-2 code.
`search_countries` returns a tuple of matches; use `limit` to cap the result count.
An empty query returns an empty tuple. `dial_code` is the international
country calling code, not a local area code, and is `None` when no code is
available. `country_name_similarity(query, country)` returns the best combined
transposition-aware word and full-name similarity score for the display name
as a value from 0 to 1.

## Data and licenses

The bundled country registry is an adapted subset of ISO 3166-1 data from the
[`iso-codes` project](https://salsa.debian.org/iso-codes-team/iso-codes). Source
country names are retained as provided; their inclusion does not imply
endorsement of any political position. Text output uses each record's common
name when available, falling back to its source name.
Continent assignments are from [GeoNames](https://www.geonames.org/), using
GeoNames' single-continent mapping for each country or territory. The
registry data is licensed under LGPL-2.1-or-later, continent assignments under
CC BY 4.0, and dial codes are derived from GeoNames countryInfo.txt, also
under CC BY 4.0. The library code is under BSD 3-Clause. See the
[data notice](https://github.com/oyghen/countrycodes/blob/main/packages/countrycodes/LICENSES/iso-codes.NOTICE),
[LGPL license text](https://github.com/oyghen/countrycodes/blob/main/packages/countrycodes/LICENSES/iso-codes.LGPL-2.1.txt),
and [BSD license](https://github.com/oyghen/countrycodes/blob/main/packages/countrycodes/LICENSE).
