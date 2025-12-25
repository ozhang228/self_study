import socket
from typing import Optional

from http_server_types.response import Response, ResponseBuilder


def recv_line(conn: socket.socket) -> tuple[str, Optional[Response]]:
    """

    Args:
        sock: TCP socket

    Returns: one line of the message, error as a response if any errors occurred

    """
    try:
        msg = []
        while True:
            nxt_byte = conn.recv(1)

            if nxt_byte == b"\r":
                _ = conn.recv(1)
                break
            elif nxt_byte == b"\n":
                break

            msg.append(nxt_byte)

        return b"".join(msg).decode(), None
    except Exception as e:
        return (
            "",
            ResponseBuilder().status(500).message(str(e)).build(),
        )
