import os
import tempfile
from typing import Any, Generator
import pytest
from app.utils.workspace import in_python_project


@pytest.fixture
def temp_dir() -> Generator[str, Any, None]:
    """Creates a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp:
        yield temp


def test_pyproject_toml(temp_dir: str) -> None:
    """Test with pyproject.toml file"""
    with open(os.path.join(temp_dir, "pyproject.toml"), "w") as file:
        file.write('[project]\nname = "dummy"')

    assert in_python_project(temp_dir)


def test_setup_py(temp_dir: str) -> None:
    """Test with pyproject.toml file"""
    with open(os.path.join(temp_dir, "setup.py"), "w") as file:
        file.write("from setuptools import setup\nsetup(name='test_project')")

    assert in_python_project(temp_dir)


def test_virtualenv(temp_dir: str) -> None:
    """Test with a virtual environment"""
    os.mkdir(os.path.join(temp_dir, "venv"))
    assert in_python_project(temp_dir)


def test_python_package(temp_dir: str) -> None:
    """Test with a pacakge"""
    package_dir = os.path.join(temp_dir, "dummy_package")
    os.mkdir(package_dir)

    with open(os.path.join(package_dir, "__init__.py"), "w") as file:
        file.write("# init file")

    assert in_python_project(temp_dir)


def test_no_python_project(temp_dir: str) -> None:
    """Test with an empty directory"""
    assert not in_python_project(temp_dir)
