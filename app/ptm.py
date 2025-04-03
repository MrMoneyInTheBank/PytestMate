import os
import click
from app.utils.workspace import in_python_project


@click.group()
def ptm() -> None:
    pass


@click.command()
def init() -> None:
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


@click.command()
def update() -> None:
    pass


@click.command()
def test() -> None:
    pass


@click.command()
def report() -> None:
    pass


@click.command()
def generate() -> None:
    pass


ptm.add_command(init)
ptm.add_command(update)
ptm.add_command(test)
ptm.add_command(report)
ptm.add_command(generate)
