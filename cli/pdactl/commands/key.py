from typing import Dict, List

import typer
from pydantic import ValidationError

from ..fetching import get, get_full_url, post
from ..models import KeyAddResponse, KeyResponse
from ..printing import print_output

app = typer.Typer()


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
    response: List[Dict] = [post(url, request_body) for i in range(amount)]
    try:
        added_keys: List[KeyAddResponse] = [KeyAddResponse(**r) for r in response]
    except ValidationError:
        if response[0]["detail"] == "Not authenticated":
            print("You are not authenticated. Please provide valid credentials.")
        else:
            print(response[0])
    else:
        print_output(*added_keys)


@app.command()
def remove(identifier: int = typer.Argument(..., help="Identifier of key to remove.")):
    """Remove key(s) from the database"""
    url: str = get_full_url("/administration/remove_key")
    request_body: Dict = {"identifier": identifier}
    response: Dict = post(url, request_body)
    try:
        removed_key: KeyResponse = KeyResponse(**response)
    except ValidationError as e:
        print(e.json())
    else:
        print_output(removed_key)


@app.command()
def ls():
    """List all keys in the database"""
    url: str = get_full_url("/administration/keys")
    response: List[Dict] = get(url)
    try:
        keys: List[KeyResponse] = [KeyResponse(**r) for r in response]
    except ValidationError as e:
        print(e.json())
    else:
        print_output(*keys)
