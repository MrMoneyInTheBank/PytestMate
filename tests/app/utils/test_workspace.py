import os
import tempfile
from typing import Any, Generator, List
import pytest
from app.utils.workspace import in_python_project, get_python_files


@pytest.fixture
def temp_dir() -> Generator[str, Any, None]:
    """Creates a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp:
        yield temp


# Tests for in_python_project function


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
    package_dir: str = os.path.join(temp_dir, "dummy_package")
    os.mkdir(package_dir)

    with open(os.path.join(package_dir, "__init__.py"), "w") as file:
        file.write("# init file")

    assert in_python_project(temp_dir)


def test_no_python_project(temp_dir: str) -> None:
    """Test with an empty directory"""
    assert not in_python_project(temp_dir)


# Tests for get_python_files function


def test_get_python_files(temp_dir: str) -> None:
    """Test get_python_files with nested Python files."""
    package_dir: str = os.path.join(temp_dir, "dummy_package")
    os.makedirs(package_dir)

    for name in ["file1.py", "file2.py", "file3.py"]:
        with open(os.path.join(package_dir, name), "w") as f:
            f.write("# dummy")

    sub1: str = os.path.join(package_dir, "subpackage1")
    os.makedirs(sub1)
    with open(os.path.join(sub1, "file4.py"), "w") as f:
        f.write("# dummy")

    sub2: str = os.path.join(sub1, "subpackage2")
    os.makedirs(sub2)
    with open(os.path.join(sub2, "file5.py"), "w") as f:
        f.write("# dummy")

    result: List[str] = get_python_files(package_dir)

    expected: List[str] = sorted(
        [
            "file1.py",
            "file2.py",
            "file3.py",
            os.path.join("subpackage1", "file4.py"),
            os.path.join("subpackage1", "subpackage2", "file5.py"),
        ]
    )

    assert sorted(result) == expected
