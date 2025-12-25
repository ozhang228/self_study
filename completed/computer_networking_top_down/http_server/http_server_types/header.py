from typing import Literal, TypeGuard, get_args

GeneralHeader = Literal[
    "Cache-Control",
    "Connection",
    "Date",
    "Pragma",
    "Trailer",
    "Transfer-Encoding",
    "Upgrade",
    "Via",
    "Warning",
]

RequestHeader = Literal[
    "Accept",
    "Accept-Charset",
    "Accept-Encoding",
    "Accept-Language",
    "Authorization",
    "Expect",
    "From",
    "Host",
    "If-Match",
    "If-Modified-Since",
    "If-None-Match",
    "If-Range",
    "If-Unmodified-Since",
    "Max-Forwards",
    "Proxy-Authorization",
    "Range",
    "Referer",
    "TE",
    "User-Agent",
]

EntityHeader = Literal[
    "Allow",
    "Content-Encoding",
    "Content-Language",
    "Content-Length",
    "Content-Location",
    "Content-MD5",
    "Content-Range",
    "Content-Type",
    "Expires",
    "Last-Modified",
]


def is_general_header(header: str) -> TypeGuard[GeneralHeader]:
    """
    Typeguard function for general headers
    Args:
        header: the header string to check

    Returns: true if it is a valid general header

    """
    general_headers = get_args(GeneralHeader)

    if header in general_headers:
        return True
    return False


def is_request_header(header: str) -> TypeGuard[RequestHeader]:
    """
    Typeguard function for Request headers
    Args:
        header: the header string to check

    Returns: true if it is a valid request header

    """
    request_headers = get_args(RequestHeader)

    if header in request_headers:
        return True
    return False


def is_entity_header(header: str) -> TypeGuard[EntityHeader]:
    """
    Typeguard function for entity headers
    Args:
        header: the header string to check

    Returns: true if it is a valid entity header

    """
    entity_headers = get_args(EntityHeader)

    if header in entity_headers:
        return True
    return False
