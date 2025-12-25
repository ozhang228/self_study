from typing import Literal, TypeGuard, get_args

Method = Literal[
    "OPTIONS",
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "TRACE",
]


def is_valid_method(method: str) -> TypeGuard[Method]:
    """
    Typeguard function for method
    Args:
        method: the proposed method

    Returns: true if it is a valid method

    """
    allowed_methods = get_args(Method)

    if method in allowed_methods:
        return True
    return False
