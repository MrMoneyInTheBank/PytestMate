"""
Utility functions used in intermediary steps
to cli commands.
"""

import os
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


def get_python_files(root_dir: str) -> List[str]:
    """
    Returns the relative path of all Python files in a project
    relative to the root directory.

    Parameters:
        root_dir (str): Root directory of the Python project
    Returns:
        list[str] | None: Relative paths of all python files, except tests
    Raises:
        NotFoundError: If a file is not found or a path is broken
    """
    if not os.path.isdir(root_dir):
        raise FileNotFoundError(f"Directory {root_dir} not found")

    python_files: Final[List[str]] = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.relpath(os.path.join(root, file), root_dir))

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

    os.makedirs(os.path.join(root_dir, "tests"), exist_ok=True)
