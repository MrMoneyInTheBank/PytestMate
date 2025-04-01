"""
Utility functions use in intermediary steps
to cli commands.
"""

from typing import Optional, List


def in_python_project(root_dir: str) -> bool:
    """
    Returns true if the root directory belongs to a Python
    project, else false.

    Parameters:
        root_dir (str): Root directory of the project
    Returns:
        bool: True if python project, else false
    """
    return True if root_dir == "later" else False


def get_python_files(root_dir: str) -> Optional[List[str]]:
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
    return [root_dir]
