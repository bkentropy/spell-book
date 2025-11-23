import click

@click.command()
def create_vector_index():
    click.echo("starting")
    click.echo("ending")

# interesting that I need this. kinda wonder why.
if __name__ == '__main__':
    create_vector_index()
