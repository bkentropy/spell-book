import click
from app.services.embedding import EmbeddingClient
from app.database import spells

@click.command()
def process_spells():
    """Process spells in the database."""
    click.echo("starting")
    embedding_client = EmbeddingClient()
    # resp = embedding_client.get_embedding("test")
    embedding_client.embed_all_spell_descriptions(spells)
    click.echo("ending")

if __name__ == '__main__':
    process_spells()
