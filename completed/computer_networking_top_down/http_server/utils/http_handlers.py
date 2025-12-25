import os
from typing import Optional
from urllib.parse import ParseResult

from definitions import PROJ_ROOT
from http_server_types.response import Response, ResponseBuilder


def get_data_path(uri: ParseResult) -> str:
    if uri.path == "/":
        file_path = f"{PROJ_ROOT}/data{uri.path}data.txt"
    else:
        file_path = f"{PROJ_ROOT}/data{uri.path}/data.txt"
    return file_path


def get_data(uri: ParseResult) -> tuple[Optional[Response], Optional[Response]]:
    file_path = get_data_path(uri)

    if not os.path.exists(file_path):
        return (
            None,
            ResponseBuilder()
            .status(404)
            .message(f"Data does not exist at path {uri.path}")
            .build(),
        )

    with open(file_path, "r") as f:
        content = f.read()

    return ResponseBuilder().status(200).data(content).build(), None


def post_data(uri: ParseResult, data: str) -> Optional[Response]:
    file_path = get_data_path(uri)

    with open(file_path, "w") as f:
        f.write(data)

    return ResponseBuilder().status(200).message(f"Data posted at {file_path}").build()
