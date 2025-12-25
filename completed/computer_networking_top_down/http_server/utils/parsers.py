from typing import Optional
from urllib.parse import urlparse

from http_server_types.method import is_valid_method
from http_server_types.request_line import RequestLine
from http_server_types.response import Response, ResponseBuilder


def parse_request_line(
    line: str,
) -> tuple[Optional[RequestLine], Optional[Response]]:
    """

    Args:
        line: request line

    Returns: message denoting which part of the request line is invalid

    """

    parts = line.split(" ")

    if len(parts) != 3:
        return None, (
            ResponseBuilder()
            .status(400)
            .message("Request line must consist of 'METHOD Request-URI HTTP-Version'")
            .build()
        )

    method, uri, http_version = parts

    if not is_valid_method(method):
        return (
            None,
            ResponseBuilder().status(405).message(method).build(),
        )

    # Request-URI can be * | absoluteURI | abs_path | authority
    # server will not support CONNECT / Authority
    uri = urlparse(uri)

    if uri.path == "*" and method != "OPTIONS":
        return (
            None,
            ResponseBuilder()
            .status(400)
            .message("* can only be used with OPTIONS")
            .build(),
        )

    if http_version != "HTTP/1.1":
        return (
            None,
            ResponseBuilder().status(505).message("Only HTTP/1.1 is supported").build(),
        )

    request_line: RequestLine = {"method": method, "uri": uri, "version": http_version}

    return request_line, None
