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
from app import (
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
    Initialize test structure for a Python project.

    This command:
    1. Verifies the current directory is a Python project
    2. Identifies Python source files
    3. Creates test directory structure
    4. Generates test file placeholders

    Parameters:
        git (bool): Whether to use git for file discovery

    Returns:
        None

    Raises:
        click.ClickException: If project validation fails or file operations fail
    """
    try:
        current_dir: str = os.getcwd()
        if not in_python_project(current_dir):
            raise click.ClickException(
                "Please run pytestmate from within a Python project"
            )

        click.echo("✅ Verified Python project")

        python_files: List[str] = get_python_files(current_dir, git)
        if not python_files:
            raise click.ClickException("No Python files found in the project")

        # Display files or count
        if len(python_files) > 15:
            click.echo(f"Found {len(python_files)} Python files")
        else:
            click.echo("Found these Python files:")
            for file in python_files:
                click.echo(f"  {file}")

        if click.confirm("Create test structure?"):
            create_tests_directory(current_dir)
            create_test_files("tests", python_files)
            click.echo("✅ Test structure created successfully")
        else:
            click.echo("Operation cancelled")

    except (FileNotFoundError, PermissionError) as e:
        raise click.ClickException(str(e))


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
