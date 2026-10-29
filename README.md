# CountryCodes

CountryCodes is a Python workspace with two separately published packages for
ISO 3166-1 country and territory lookups:

- [`countrycodes`](packages/countrycodes/README.md): dependency-free lookup
  library with the bundled registry, continent assignments, and international
  dial codes.
- [`countrycodes-cli`](packages/countrycodes-cli/README.md): command-line
  interface built on the library.

The packages support Python 3.11 and newer. See the package READMEs for
installation, usage, and package-specific licensing details.

## Development

Install the workspace packages and development tools with
[uv](https://docs.astral.sh/uv/):

```console
uv sync --dev --all-packages
```

Run tests and quality checks from VS Code:

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).
2. Select **Tasks: Run Task**.
3. Choose **CountryCodes: Checks** to run pre-commit (including Ruff lint and
formatting), followed by the test suite.

The **pre-commit all** and **pytest** tasks can also be run separately.

## Releases

Prepare a lockstep release with:

```console
uv run version.py --bump patch
```

Run this from a clean working tree. The script updates versions, refreshes the
lockfile, commits the release changes, and creates a `v<version>` tag. Push the
commit and tag to trigger the release workflow, which builds, smoke-tests, and
publishes both packages to PyPI.

## Licensing

The library code and CLI are BSD 3-Clause licensed. The bundled ISO registry
data is LGPL-2.1-or-later, and the continent assignments are CC BY 4.0. See
the [library README](packages/countrycodes/README.md) and
[license files](packages/countrycodes/LICENSES/) for details.
