from datetime import datetime
from typing import Dict, List, Tuple, Union


def print_header(add_key: bool = False) -> None:
    header_items: List = [
        ("IDENTIFIER", (0, 14)),
        ("CAN CREATE TOKEN", (14, 34)),
        ("CREATED BY", (34, 48)),
        ("CREATION DATE", (48, 76)),
    ]
    if add_key:
        header_items.append((("API KEY", (76, 110))))
    header = "".join([pad(i, p) for i, p in header_items])
    print(header)


def print_line(key: Dict, add_key: bool = False) -> None:
    identifier: str = pad(key["identifier"], (0, 14))
    can_create_token: str = pad(key["can_create_token"], (14, 34))
    created_by: str = pad(key["created_by"], (34, 48))
    c_time: str = datetime.fromisoformat(key["creation_date"]).ctime()
    creation_date: str = pad(c_time, (48, 76))
    line = "".join([identifier, can_create_token, created_by, creation_date])
    if add_key:
        api_key: str = pad(key["new_api_key"], (76, 110))
        line + api_key
    print(line)


def pad(value: Union[str, int, bool], position: Tuple[int, int]) -> str:
    if not isinstance(value, str):
        value = str(value)
    block_len: int = position[1] - position[0]
    spaces: int = block_len - len(value)
    padded_value: str = value + (spaces * " ")
    return padded_value
