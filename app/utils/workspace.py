"""
Utility functions used in intermediary steps
to cli commands.
"""

import os
import shutil
import subprocess
from pathspec import PathSpec
from importlib.resources import files as package_files
from typing import Final, List, Set


def in_python_project(root_dir: str) -> bool:
    """
    Returns true if the root directory belongs to a Python
    project, else false.

    Parameters:
        root_dir (str): Root directory of the project
    Returns:
        bool: True if python project, else false
    """
    key_files: Final[Set[str]] = {
        "pyproject.toml",
        "setup.py",
        "requirements.txt",
        "Pipfile",
        "tox.ini",
        "poetry.lock",
        "uv.lock",
        ".python-version",
    }
    key_dirs: Final[Set[str]] = {"venv", ".venv", "env"}

    if any(os.path.isfile(os.path.join(root_dir, file)) for file in key_files):
        return True

    if any(os.path.isdir(os.path.join(root_dir, directory)) for directory in key_dirs):
        return True

    for _, _, files in os.walk(root_dir):
        if any(file.endswith(".py") for file in files):
            return True

    return False


def get_ignore_spec(root_dir: str) -> PathSpec:
    """
    Returns a PathSpec object for filtering files based on ignore patterns.

    This function first checks if a `.gitignore` file exists in the provided
    root directory. If it does, it uses that file to construct the PathSpec.
    If not, it falls back to a bundled default Python `.gitignore` template
    stored within the package at `app.templates/python.gitignore`.

    Parameters:
        root_dir (str): The root directory of the project.

    Returns:
        PathSpec: A PathSpec object constructed using `gitwildmatch` rules,
        which can be used to match files against ignore patterns.
    """
    gitignore_path: str = os.path.join(root_dir, ".gitignore")

    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as file:
            return PathSpec.from_lines(pattern_factory="gitwildmatch", lines=file)
    else:
        template_path = package_files("app.templates").joinpath("python.gitignore")
        with template_path.open("r") as file:
            return PathSpec.from_lines(pattern_factory="gitwildmatch", lines=file)


def get_python_files(root_dir: str, use_git: bool) -> List[str]:
    """
    Returns the relative path of all Python files in a project
    relative to the root directory.

    Parameters:
        root_dir (str): Root directory of the Python project
        use_git (bool): Flag indicating whether or not use git for filtering files
    Returns:
        list[str] | None: Relative paths of all python files, except tests
    Raises:
        NotFoundError: If a file is not found or a path is broken
        RuntimeError: If a shell/subprocess command fails to execute
    """
    if not os.path.isdir(root_dir):
        raise FileNotFoundError(f"Directory {root_dir} not found")

    if use_git:
        if not shutil.which("git"):
            raise RuntimeError("Git is not installed on the system.")
        if not os.path.exists(os.path.join(root_dir, ".git")):
            raise ModuleNotFoundError(f"{root_dir} is not a git repo.")
        if not os.path.exists(os.path.join(root_dir, ".gitignore")):
            raise FileNotFoundError(
                f"Directory {root_dir} is a git repo but does not have a gitignore config."
            )

        try:
            git_py_files: str = subprocess.check_output(
                ["git", "-C", root_dir, "ls-files", "*.py"],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            return git_py_files.strip().splitlines()
        except subprocess.CalledProcessError as error:
            raise RuntimeError("Could not filter files using git") from error

    spec: PathSpec = get_ignore_spec(root_dir)
    python_files: List[str] = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), root_dir)
            if file.endswith(".py") and not spec.match_file(rel_path):
                python_files.append(rel_path)

    return python_files


def create_tests_directory(root_dir: str) -> None:
    """
    Creates a tests directory in the root directory if it doesn't exist.

    Parameters:
        root_dir (str): Root directory of the project
    Returns:
        None
    Raises:
        NotFoundError: If the root directory is not found
        PermissionError: If the root directory is not writable
        OSError: If the root directory is not a directory
    """
    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"Directory {root_dir} not found")
    if not os.access(root_dir, os.W_OK):
        raise PermissionError(f"Directory {root_dir} is not writable")
    if not os.path.isdir(root_dir):
        raise FileNotFoundError(f"Directory {root_dir} not found")

    test_dir = os.path.join(root_dir, "tests")
    os.makedirs(test_dir, exist_ok=True)


def create_test_files(tests_dir: str, python_files: List[str]) -> None:
    """
    Creates test files in the tests directory mirroring the structure
    of the provided Python files. Each Python file will have a corresponding
    test file in the tests directory with the same relative path structure.

    Parameters:
        tests_dir (str): Path to the tests directory
        python_files (List[str]): List of relative paths to Python files from project root
    Returns:
        None
    Raises:
        FileNotFoundError: If the tests directory is not found
        PermissionError: If the tests directory is not writable
    """
    if not os.path.exists(tests_dir):
        raise FileNotFoundError(f"Directory {tests_dir} not found")
    if not os.access(tests_dir, os.W_OK):
        raise PermissionError(f"Directory {tests_dir} is not writable")

    for python_file in python_files:
        test_file = python_file
        if test_file == "__init__.py":
            continue
        if test_file.startswith("test_"):
            continue

        if not test_file.startswith("test_"):
            dirname = os.path.dirname(test_file)
            basename = os.path.basename(test_file)
            test_file = os.path.join(dirname, f"test_{basename}")

        test_dir = os.path.dirname(os.path.join(tests_dir, test_file))
        os.makedirs(test_dir, exist_ok=True)

        test_file_path = os.path.join(tests_dir, test_file)
        if not os.path.exists(test_file_path):
            with open(test_file_path, "w") as f:
                f.write("import pytest\n\n")
