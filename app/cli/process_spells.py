import click

@click.command()
def process_spells():
    """Process spells in the database."""
    click.echo("starting")
    click.echo("ending")

if __name__ == '__main__':
    process_spells()
