from configparser import ConfigParser
from typing import Optional

import typer

from .commands import key
from .config import ensure_config, write_config

app = typer.Typer()
app.add_typer(key.app, name="key")


@app.command()
def setup(url: str = typer.Option(..., "-u", "--url", prompt=True)):
    """Setup pdactl to interact with backend server"""
    if url:
        config("core.url", url)
    typer.echo(
        'Now export your api key as an evironment variable: export PDA_API_KEY="<YOUR_API_KEY>"'
    )


@app.command()
def config(
    key: str = typer.Argument(..., help="Config option to get or set."),
    value: Optional[str] = typer.Argument(False, help="Value of config option."),
):
    """Get and set configuration options"""
    top_key, sub_key = key.split(".")
    config: ConfigParser = ensure_config()
    if value:
        if top_key not in config.sections():
            config[top_key] = {}
        else:
            config[top_key][sub_key] = value
    else:
        try:
            typer.echo(config[top_key][sub_key])
        except KeyError as e:
            typer.echo(
                f"No configuration option available under this key: {e}", err=True
            )
    write_config(config)


if __name__ == "__main__":
    app()
