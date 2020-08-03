from configparser import ConfigParser
from typing import Dict, List, Optional

import typer

from .config import ensure_config, write_config
from .fetching import get, get_full_url, post
from .printing import print_header, print_line

app = typer.Typer()


@app.command()
def setup(url: str = typer.Option(..., "-u", "--url", prompt=True)):
    """Setup pdactl to interact with backend server"""
    if url:
        config("core.url", url)
    typer.echo(
        'Now export your api key as an evironment variable by typing the following into your shell: \n export PDA_API_KEY="<YOUR_API_KEY>"'
    )


@app.command()
def config(
    key: str = typer.Argument(..., help="Config option to get or set."),
    value: Optional[str] = typer.Argument(
        False, help="Value to set the config option to."
    ),
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


@app.command()
def add(
    can_create_token: bool = typer.Option(
        False,
        "-c",
        "--can-create-token",
        help="Gives key the power to create new keys.",
    ),
    amount: int = typer.Argument(1, help="Amount of keys to create."),
):
    """Generate new key(s) and store their hash in the database"""
    url: str = get_full_url("/administration/add_key")
    request_body: Dict = {"can_create_tokens": can_create_token}
    new_keys: List[Dict] = [post(url, request_body) for i in range(amount)]
    print_header(add_key=True)
    for new_key in new_keys:
        print_line(new_key, add_key=True)


@app.command()
def remove(identifier: int = typer.Argument(..., help="Identifier of key to remove.")):
    """Remove key(s) from the database"""
    url: str = get_full_url("/administration/remove_key")
    request_body: Dict = {"identifier": identifier}
    doc: Dict = post(url, request_body)
    print_header()
    print_line(doc)


@app.command()
def ls():
    """List all keys in the database"""
    url: str = get_full_url("/administration/keys")
    keys: List[Dict] = get(url)
    print_header()
    for key in keys:
        print_line(key)


if __name__ == "__main__":
    app()
