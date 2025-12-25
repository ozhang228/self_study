import json
import socket

from http_server_types.header import (is_entity_header, is_general_header,
                                      is_request_header)
from http_server_types.response import ResponseBuilder
from utils.http_handlers import get_data, post_data
from utils.parsers import parse_request_line
from utils.send_response import send_response
from utils.socket import recv_line

HOST = "localhost"
PORT = 3000


def main():
    print("Starting server")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(0)

        while True:
            conn, _ = sock.accept()
            print("Connected")

            with conn:
                msg, err_res = recv_line(conn)

                if err_res:
                    print(err_res)
                    return

                # Request Line
                request_line, err_res = parse_request_line(msg)

                if err_res:
                    print(err_res)
                    return

                # Headers
                request_headers = dict[str, str]()
                general_headers = dict[str, str]()
                entity_headers = dict[str, str]()

                while True:
                    msg, err_res = recv_line(conn)

                    if err_res:
                        print(err_res)
                        return

                    if msg == "":
                        break

                    partition_idx = msg.find(":")
                    header = msg[0:partition_idx]
                    # add 1 to skip one whitespace
                    value = msg[partition_idx + 1 : len(msg)]

                    if is_request_header(header):
                        request_headers[header] = value
                    elif is_general_header(header):
                        general_headers[header] = value
                    elif is_entity_header(header):
                        entity_headers[header] = value
                    else:
                        print(f"Invalid header {header} and value {value}")

                # Request Body
                if "Content-Length" in entity_headers:
                    data = conn.recv(int(entity_headers["Content-Length"])).decode()

                    try:
                        body = json.loads(data)
                    except:
                        send_response(
                            conn,
                            ResponseBuilder()
                            .status(500)
                            .message("Was not able to parse request body.")
                            .build(),
                        )
                        return
                else:
                    body: dict = json.loads("{}")

                match request_line["method"]:
                    case "GET":
                        res, err = get_data(request_line["uri"])

                        if err:
                            send_response(conn, err)
                        elif res:
                            send_response(conn, res)
                        else:
                            print("Error occured in get_data function")
                    case "POST":
                        if body or body["content"] == "":
                            send_response(
                                conn,
                                ResponseBuilder()
                                .status(400)
                                .message("POST requests must contain a message")
                                .build(),
                            )
                            return

                        res = post_data(request_line["uri"], body["content"])

                        if res:
                            send_response(conn, res)
                        else:
                            send_response(conn, ResponseBuilder().status(500).build())


if __name__ == "__main__":
    main()
