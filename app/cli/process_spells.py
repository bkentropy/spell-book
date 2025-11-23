import click
from app.services.embedding import EmbeddingClient

@click.command()
def process_spells():
    """Process spells in the database."""
    click.echo("starting")
    embedding_client = EmbeddingClient()
    resp = embedding_client.get_embedding("test")
    click.echo(resp)

    click.echo("ending")

if __name__ == '__main__':
    process_spells()
