#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "purekit",
#   "typer",
# ]
# ///

import re
import subprocess
import tomllib
from enum import StrEnum, auto
from pathlib import Path
from typing import Annotated, Any

import purekit as pk  # type: ignore
import typer  # type: ignore

LIB_NAME = "countrycodes"
CLI_NAME = "countrycodes-cli"

ROOT = Path(__file__).resolve().parent
ROOT_PYPROJECT = ROOT / "pyproject.toml"
LIB_PYPROJECT = ROOT / "packages" / LIB_NAME / "pyproject.toml"
CLI_PYPROJECT = ROOT / "packages" / CLI_NAME / "pyproject.toml"


class BumpType(StrEnum):
    """Define the supported version bump types."""

    major = auto()
    minor = auto()
    patch = auto()
    stable = auto()
    alpha = auto()
    beta = auto()
    rc = auto()
    post = auto()
    dev = auto()


def main(
    bump_types: Annotated[
        list[BumpType], typer.Option("--bump", help="Specify bump type.")
    ],
) -> None:
    """Bump versions for a lockstep release.

    Examples:
        uv run version.py --bump minor
        uv run version.py --bump minor --bump rc
        uv run version.py --bump rc
        uv run version.py --bump stable
    """
    ensure_clean_worktree()
    bump_versions(bump_types)
    bumped_version = project_version(ROOT_PYPROJECT)
    check_versions(bumped_version)
    update_dependency_pin(bumped_version)
    refresh_lockfile()
    commit_bump(bumped_version)
    tag_commit(bumped_version)
    typer.echo(pk.text.headline(typer.style("if successful", fg=typer.colors.YELLOW)))
    typer.echo("git push && git push --tags")


def ensure_clean_worktree() -> None:
    """Prevent release automation from including unrelated changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if result.stdout.strip():
        raise RuntimeError("Version bumps require a clean Git working tree")


def bump_versions(bumps: list[BumpType]) -> None:
    """Bump the workspace root and package versions in one sequence."""
    run(*uv_version_args(bumps))
    run(*uv_version_args(bumps, package=LIB_NAME))
    run(*uv_version_args(bumps, package=CLI_NAME))


def uv_version_args(bumps: list[BumpType], package: str | None = None) -> list[str]:
    """Return uv version command arguments in bump order."""
    args = ["uv", "version", "--frozen"]

    for bump in bumps:
        args.extend(["--bump", bump.value])

    if package is not None:
        args.extend(["--package", package])

    return args


def project_version(path: Path) -> str:
    """Return the project version from a pyproject.toml file."""
    data: dict[str, Any] = tomllib.loads(path.read_text(encoding="utf-8"))
    version = data["project"]["version"]
    if not isinstance(version, str):
        raise TypeError(f"Project version in {path} must be a string")
    return version


def check_versions(version: str) -> None:
    """Verify that package versions match the workspace version."""
    lib_version = project_version(LIB_PYPROJECT)
    cli_version = project_version(CLI_PYPROJECT)

    if lib_version != version or cli_version != version:
        raise RuntimeError(
            f"Version mismatch: root={version}, lib={lib_version}, cli={cli_version}"
        )


def update_dependency_pin(version: str) -> None:
    """Update the CLI package's exact dependency pin on the library."""
    cli_text = CLI_PYPROJECT.read_text(encoding="utf-8")
    updated = replace_exact_pin(cli_text, LIB_NAME, version)

    if updated != cli_text:
        CLI_PYPROJECT.write_text(updated, encoding="utf-8")


def replace_exact_pin(text: str, package: str, version: str) -> str:
    """Return text with an exact dependency pin replaced."""
    pattern = rf"({re.escape(package)}==)([^\s,;\"']+)"
    updated, count = re.subn(pattern, rf"\g<1>{version}", text, count=1)

    if count != 1:
        raise RuntimeError(f"Could not find exact pin for {package} in {CLI_PYPROJECT}")

    return updated


def refresh_lockfile() -> None:
    """Regenerate the uv lockfile."""
    run("uv", "lock")


def commit_bump(version: str) -> None:
    """Stage changed version files and commit the release bump."""
    prefix = typer.style("Created commit", fg=typer.colors.GREEN, bold=True)
    message = f"chore(release): bump version to v{version}"

    files = (ROOT_PYPROJECT, LIB_PYPROJECT, CLI_PYPROJECT, ROOT / "uv.lock")
    for file_name in files:
        run("git", "add", str(file_name))

    run("git", "commit", "-m", message)
    typer.echo(f"{prefix} {message}")


def tag_commit(version: str) -> None:
    """Create an annotated release tag for the version."""
    prefix = typer.style("Created tag", fg=typer.colors.GREEN, bold=True)
    tag = f"v{version}"

    run("git", "tag", "-a", tag, "-m", tag)
    typer.echo(f"{prefix} {tag}")


def run(*args: str) -> None:
    """Run a command in the repository root."""
    subprocess.run(args, check=True, cwd=ROOT)


if __name__ == "__main__":
    typer.run(main)
