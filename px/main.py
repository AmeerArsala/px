import typer

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)

@app.command()
def _():
    """Welcome to px!"""
    pass


@app.command()
def init(a: int):
    """Initialize a project"""
    pass


# Start the Typer CLI
if __name__ == "__main__":
    app()
