import click
from .process_spells import process_spells
from .create_vector_index import create_vector_index

@click.group()
def cli():
    """Spell Book CLI."""
    pass

# Add commands to the CLI
group = cli.add_group('spells')
group.add_command(process_spells)
group.add_command(create_vector_index)

if __name__ == '__main__':
    cli()
