import click
from app.database import spells
from pymongo.operations import SearchIndexModel
import time

@click.command()
def create_vector_index():
    click.echo("Creating vector index...")
    # Define your vector search index model with customizable fields, dimensions, and similarity
    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "desc_embedding",
                    "numDimensions": 384,
                    "similarity": "cosine",
                }
            ]
        },
        name="spell_desc_index",
        type="vectorSearch"
    )

    # Create the search index and poll for readiness
    try:
        result = spells.create_search_index(model=search_index_model)
        click.echo("New search index named " + result + " is building.")

        click.echo("Polling to check if the index is ready. This may take up to a minute.")
        def predicate(index):
            return index.get("queryable") is True

        while True:
            indices = list(spells.list_search_indexes(result))
            if len(indices) and predicate(indices[0]):
                break
            time.sleep(5)
        click.echo(result + " is ready for querying.")

    except Exception as e:
        click.echo(f"An error occurred: {e}")

    finally:
        click.echo("Vector index created.")

# interesting that I need this. kinda wonder why.
if __name__ == '__main__':
    create_vector_index()
