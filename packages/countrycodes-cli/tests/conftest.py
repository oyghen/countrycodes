import importlib
import tomllib
from pathlib import Path
from types import ModuleType

import pytest


@pytest.fixture(scope="module")
def project_pkg(project_name: str) -> ModuleType:
    return importlib.import_module(project_name)


@pytest.fixture(scope="module")
def project_name() -> str:
    project_root = Path(__file__).parent.parent.resolve()
    pyproject_toml = project_root / "pyproject.toml"

    with pyproject_toml.open("rb") as toml_file:
        data = tomllib.load(toml_file)

    return data["project"]["name"].replace("-", "_")


@pytest.fixture(scope="module")
def distribution_name() -> str:
    project_root = Path(__file__).parent.parent.resolve()
    pyproject_toml = project_root / "pyproject.toml"

    with pyproject_toml.open("rb") as toml_file:
        data = tomllib.load(toml_file)

    return data["project"]["name"]
