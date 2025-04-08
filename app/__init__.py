"""
PytestMate - Python Test Infrastructure Manager

This package provides tools for managing Python test infrastructure, including
test file generation, test running, and test reporting. It exports utility
functions from the workspace module for managing Python project structures
and test files.
"""

from typing import List
from .utils import (
    in_python_project,
    get_ignore_spec,
    get_python_files,
    create_tests_directory,
    create_test_files,
)

__all__: List[str] = [
    "in_python_project",
    "get_ignore_spec",
    "get_python_files",
    "create_tests_directory",
    "create_test_files",
]
