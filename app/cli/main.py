import click
from .process_spells import process_spells

@click.group()
def cli():
    """Spell Book CLI."""
    pass

# Add commands to the CLI
group = cli.add_group('spells')
group.add_command(process_spells)

if __name__ == '__main__':
    cli()
