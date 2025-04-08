"""
PytestMate CLI Interface

This module provides the command-line interface for PytestMate, a tool for managing
Python test infrastructure. It offers commands for initializing test structures,
updating test files, running tests, and generating test reports.

Available Commands:
    init    - Initialize test structure for a Python project
    update  - Update existing test files (Coming Soon)
    test    - Run tests with pytest (Coming Soon)
    report  - Generate test coverage reports (Coming Soon)
    generate - Generate additional test files (Coming Soon)

The CLI is built using Click and provides a user-friendly interface for managing
Python test infrastructure across your project.
"""

import os
import click
from typing import List
from app.utils.workspace import (
    in_python_project,
    get_python_files,
    create_tests_directory,
    create_test_files,
)


@click.group()
def ptm() -> None:
    pass


@click.command()
@click.option(
    "-g",
    "--git",
    type=bool,
    is_flag=True,
    flag_value=True,
    default=False,
    required=False,
    help="Use git for tracking relevant python files.",
)
def init(git: bool) -> None:
    """
    Verify that the command is run within a Python project.

    This command checks whether the current working directory is a valid Python project.
    If the verification succeeds, it prints a confirmation message. Otherwise, it prompts
    the user to run the command inside a Python project.

    Future Enhancements:
    - Scaffold a test directory structure.
    - Generate test file placeholders based on existing source code.

    Returns:
        None
    """
    current_dir = os.getcwd()
    is_python_project = in_python_project(current_dir)

    if is_python_project:
        click.echo("✅ Verfied Python project.")
    else:
        click.echo("❌ Please call pytestmate from within a Python project.")
        return

    click.echo("Found these python files")
    python_files: List[str] = get_python_files(current_dir, git)

    if len(python_files) > 15:
        click.echo(f"Found {len(python_files)} relevant files.")
    else:
        for file in python_files:
            click.echo(file)

    click.echo()

    if click.confirm("Looks good?"):
        create_tests_directory(current_dir)
        create_test_files("tests", python_files)
    else:
        click.echo("Cleaning up.")
    return


@click.command()
def update() -> None:
    """Coming Soon."""
    pass


@click.command()
def test() -> None:
    """Coming Soon."""
    pass


@click.command()
def report() -> None:
    """Coming Soon."""
    pass


@click.command()
def generate() -> None:
    """Coming Soon."""
    pass


ptm.add_command(init)
ptm.add_command(update)
ptm.add_command(test)
ptm.add_command(report)
ptm.add_command(generate)
