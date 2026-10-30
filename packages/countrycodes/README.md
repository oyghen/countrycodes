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

united_states = cc.find_country("us")
print(united_states.alpha3)  # USA
print(united_states.numeric)  # 840
print(united_states.dial_code)  # +1

united_kingdom = cc.find_country("United Kingdom")
print(united_kingdom.alpha2)  # GB

typo_tolerant_match = cc.find_country("Untied States")
print(typo_tolerant_match.alpha2)  # US

print(len(cc.list_countries()))  # 249
```

Lookups accept alpha-2, alpha-3, and numeric codes, dial codes, and country
names. Matching is case-insensitive and ignores surrounding or repeated
whitespace. If there is no exact match, the country with the most similar
name is returned, even if the similarity is low. Single-word queries are
compared with individual words in country names. Equal best matches and dial
codes shared by multiple countries raise `ValueError`.
`list_countries` returns records sorted by alpha-2 code.
`find_country` returns `None` for an empty query. `dial_code` is the
international country calling code, not a local area code, and is `None` when
no code is available.

## Data and licenses

The bundled country registry is an adapted subset of ISO 3166-1 data from the
[`iso-codes` project](https://salsa.debian.org/iso-codes-team/iso-codes).
Continent assignments are from [GeoNames](https://www.geonames.org/), using
GeoNames' single-continent mapping for each country or territory. The
registry data is licensed under LGPL-2.1-or-later, continent assignments under
CC BY 4.0, and dial codes are derived from GeoNames countryInfo.txt, also
under CC BY 4.0. The library code is under BSD 3-Clause. See the
[data notice](https://github.com/oyghen/countrycodes/blob/main/packages/countrycodes/LICENSES/iso-codes.NOTICE),
[LGPL license text](https://github.com/oyghen/countrycodes/blob/main/packages/countrycodes/LICENSES/iso-codes.LGPL-2.1.txt),
and [BSD license](https://github.com/oyghen/countrycodes/blob/main/packages/countrycodes/LICENSE).
