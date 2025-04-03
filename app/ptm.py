import os
import click
from app.utils.workspace import in_python_project


@click.group()
def ptm() -> None:
    pass


@click.command()
def init() -> None:
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
