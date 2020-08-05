from datetime import datetime
from typing import List, Tuple, Union

from .models import KeyAddResponse, KeyResponse

base_indices = [
    (0, 14),
    (14, 34),
    (34, 48),
    (48, 76),
]

api_key_index = (76, 110)


def print_output(*keys: Union[KeyResponse, KeyAddResponse]):
    print_header_line(keys[0])
    for key in keys:
        print_line(key)


def print_header_line(key: Union[KeyResponse, KeyAddResponse]) -> None:
    line = construct_base_header_line()
    if isinstance(key, KeyAddResponse):
        line += pad("API KEY", api_key_index)
    print(line)


def construct_base_header_line() -> str:
    header_items = [
        "IDENTIFIER",
        "CAN CREATE TOKEN",
        "CREATED BY",
        "CREATION DATE",
    ]
    columns = [pad(value, index) for value, index in zip(header_items, base_indices)]
    line = "".join(columns)
    return line


def print_line(key: Union[KeyResponse, KeyAddResponse]) -> None:
    line = construct_base_line(key)
    if isinstance(key, KeyAddResponse):
        line += pad(key.new_api_key, api_key_index)
    print(line)


def construct_base_line(key: KeyResponse) -> str:
    columns: List[str] = [
        pad(value, index) for (_, value), index in zip(key, base_indices)
    ]
    line = "".join(columns)
    return line


def pad(value: Union[str, int, bool, datetime], position: Tuple[int, int]) -> str:
    if isinstance(value, datetime):
        value = value.ctime()
    elif not isinstance(value, str):
        value = str(value)
    block_len: int = position[1] - position[0]
    spaces: int = block_len - len(value)
    padded_value: str = value + (spaces * " ")
    return padded_value
