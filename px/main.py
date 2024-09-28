import subprocess

import typer

from px.constants import DEFAULT_TEMPLATE, PX_PROJECT_ROOT

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)


@app.command()
def init(template: str = DEFAULT_TEMPLATE):
    """Initialize a project"""
    subprocess.run(f"python3 {PX_PROJECT_ROOT}/px/templates/{template}.py", shell=True)


@app.command()
def pp():
    """Pipelight view"""
    subprocess.run("pipelight", shell=True)


# Start the Typer CLI
if __name__ == "__main__":
    app()
