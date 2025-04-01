import click


@click.group()
def ptm() -> None:
    pass


@click.command()
def init() -> None:
    pass


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
