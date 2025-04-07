import os
import shutil
import subprocess
import tempfile
from typing import Any, Generator, List, NoReturn
import pytest
from _pytest.monkeypatch import MonkeyPatch
from pathspec import PathSpec
from app.utils.workspace import (
    in_python_project,
    get_ignore_spec,
    get_python_files,
    create_tests_directory,
    create_test_files,
)


@pytest.fixture
def temp_dir() -> Generator[str, Any, None]:
    """Creates a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp:
        yield temp


# Tests for in_python_project function


def test_pyproject_toml(temp_dir: str) -> None:
    """Test with pyproject.toml file."""
    with open(os.path.join(temp_dir, "pyproject.toml"), "w") as file:
        file.write('[project]\nname = "dummy"')

    assert in_python_project(temp_dir)


def test_setup_py(temp_dir: str) -> None:
    """Test with pyproject.toml file."""
    with open(os.path.join(temp_dir, "setup.py"), "w") as file:
        file.write("from setuptools import setup\nsetup(name='test_project')")

    assert in_python_project(temp_dir)


def test_virtualenv(temp_dir: str) -> None:
    """Test with a virtual environment."""
    os.mkdir(os.path.join(temp_dir, "venv"))
    assert in_python_project(temp_dir)


def test_python_package(temp_dir: str) -> None:
    """Test with a pacakge."""
    package_dir: str = os.path.join(temp_dir, "dummy_package")
    os.mkdir(package_dir)

    with open(os.path.join(package_dir, "__init__.py"), "w") as file:
        file.write("# init file")

    assert in_python_project(temp_dir)


def test_no_python_project(temp_dir: str) -> None:
    """Test with an empty directory."""
    assert not in_python_project(temp_dir)


# Tests for get_python_files function


def create_file(path: str, content: str = "") -> None:
    """Helper function to create a file and write to it."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        file.write(content)


def test_get_python_files_no_git(temp_dir: str) -> None:
    """Test without git awareness."""
    create_file(os.path.join(temp_dir, "main.py"))
    create_file(os.path.join(temp_dir, "helper.py"))
    create_file(os.path.join(temp_dir, "README.md"))

    files: List[str] = get_python_files(temp_dir, use_git=False)
    assert sorted(files) == ["helper.py", "main.py"]


@pytest.mark.skipif(not shutil.which("git"), reason="Git is not installed")
def test_get_python_files_with_git(temp_dir: str):
    """Test with git awareness."""
    subprocess.run(["git", "init"], cwd=temp_dir, check=True)
    create_file(os.path.join(temp_dir, "main.py"))
    create_file(os.path.join(temp_dir, "helper.py"))
    create_file(os.path.join(temp_dir, ".gitignore"), "*.md\n")

    subprocess.run(
        ["git", "config", "user.email", "test@example.com"], cwd=temp_dir, check=True
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"], cwd=temp_dir, check=True
    )
    subprocess.run(["git", "add", "."], cwd=temp_dir, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=temp_dir, check=True)

    files = get_python_files(temp_dir, use_git=True)
    assert sorted(files) == ["helper.py", "main.py"]


def test_get_python_files_not_a_directory():
    """Test if root_dir is not found."""
    with pytest.raises(FileNotFoundError):
        get_python_files("not/a/real/path", use_git=False)


@pytest.mark.skipif(not shutil.which("git"), reason="Git is not installed")
def test_get_python_files_git_not_installed(monkeypatch: MonkeyPatch, temp_dir: str):
    """Test if git not installed on system with -g flag."""
    monkeypatch.setattr(shutil, "which", lambda _: None)
    subprocess.run(["git", "init"], cwd=temp_dir, check=True)
    create_file(os.path.join(temp_dir, ".gitignore"), "*.md\n")

    with pytest.raises(RuntimeError, match="Git is not installed"):
        get_python_files(temp_dir, use_git=True)


def test_get_python_files_missing_git_dir(temp_dir: str):
    """Test if git aware but not inside git repo."""
    create_file(os.path.join(temp_dir, ".gitignore"), "*.md\n")
    with pytest.raises(ModuleNotFoundError, match="not a git repo"):
        get_python_files(temp_dir, use_git=True)


@pytest.mark.skipif(not shutil.which("git"), reason="Git is not installed")
def test_get_python_files_missing_gitignore(temp_dir: str):
    """Test if git aware but gitignore doesn't exist."""
    subprocess.run(["git", "init"], cwd=temp_dir, check=True)
    with pytest.raises(FileNotFoundError, match="does not have a gitignore"):
        get_python_files(temp_dir, use_git=True)


@pytest.mark.skipif(not shutil.which("git"), reason="Git is not installed")
def test_get_python_files_subprocess_error(monkeypatch: MonkeyPatch, temp_dir: str):
    """Test for subprocess error in git aware case."""
    subprocess.run(["git", "init"], cwd=temp_dir, check=True)
    create_file(os.path.join(temp_dir, ".gitignore"), "*.md\n")

    def mock_check_output(*_args: Any, **_kwargs: Any) -> NoReturn:
        _ = _kwargs
        _ = _args
        raise subprocess.CalledProcessError(1, "git")

    monkeypatch.setattr(subprocess, "check_output", mock_check_output)

    with pytest.raises(RuntimeError, match="Could not filter files using git"):
        get_python_files(temp_dir, use_git=True)


def test_get_ignore_spec_uses_gitignore(temp_dir: str):
    """Test gitignore pathspec."""
    create_file(os.path.join(temp_dir, ".gitignore"), "*.py\n")
    spec = get_ignore_spec(temp_dir)
    assert isinstance(spec, PathSpec)
    assert spec.match_file("main.py") is True


def test_get_ignore_spec_uses_template(temp_dir: str):
    """Test default pathspec."""
    spec = get_ignore_spec(temp_dir)
    assert isinstance(spec, PathSpec)
    assert spec.match_file("__pycache__/foo.pyc")
    assert not spec.match_file("main.py")


# Tests for create_tests_directory function


def test_create_tests_directory(temp_dir: str) -> None:
    """Test create_tests_directory"""

    create_tests_directory(temp_dir)
    assert os.path.isdir(os.path.join(temp_dir, "tests"))


def test_root_dir_does_not_exist(monkeypatch: MonkeyPatch):
    """Test if root_dir does not exist."""
    monkeypatch.setattr(os.path, "exists", lambda _: False)

    with pytest.raises(FileNotFoundError, match="not found"):
        create_tests_directory("/fake/path")


def test_root_dir_not_writable(monkeypatch: MonkeyPatch):
    """Test if root_dir is not writeable."""
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    monkeypatch.setattr(os, "access", lambda *_: False)

    with pytest.raises(PermissionError, match="not writable"):
        create_tests_directory("/fake/path")


def test_root_dir_not_a_directory(monkeypatch: MonkeyPatch):
    """Test if root_dir is not a directory"""
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    monkeypatch.setattr(os, "access", lambda *_: True)
    monkeypatch.setattr(os.path, "isdir", lambda _: False)

    with pytest.raises(FileNotFoundError, match="not found"):
        create_tests_directory("/fake/path")


# Tests for create_test_files function


def test_tests_dir_not_exist(temp_dir: str) -> None:
    """Test if tests directory does not exist."""
    with pytest.raises(FileNotFoundError, match="not found"):
        create_test_files(os.path.join(temp_dir, "tests"), [])


def test_tests_dir_not_writable(monkeypatch: MonkeyPatch) -> None:
    """Test if tests directory is not writable."""
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    monkeypatch.setattr(os, "access", lambda *_: False)

    with pytest.raises(PermissionError, match="not writable"):
        create_test_files("tests/", [])


def test_create_test_files(temp_dir: str) -> None:
    """Test if test files were created correctly."""
    create_file(os.path.join(temp_dir, "main.py"))
    create_file(os.path.join(temp_dir, "helper.py"))
    create_file(os.path.join(temp_dir, "app/another_helper.py"))
    create_file(os.path.join(temp_dir, "__init__.py"))

    create_tests_directory(temp_dir)
    create_test_files(
        os.path.join(temp_dir, "tests"),
        ["main.py", "helper.py", "app/another_helper.py"],
    )

    created_test_files: List[str] = []
    for root, _, files in os.walk(os.path.join(temp_dir, "tests")):
        for file in files:
            relpath = os.path.relpath(os.path.join(root, file), temp_dir)
            created_test_files.append(relpath)

    expected_files = sorted(
        [
            "tests/test_main.py",
            "tests/test_helper.py",
            "tests/app/test_another_helper.py",
        ]
    )
    assert sorted(created_test_files) == expected_files
