import socket as sock


def startServer():
    with sock.socket(family=sock.AF_INET, type=sock.SOCK_STREAM) as socket:
        socket.bind(("localhost", 3000))
        socket.listen()

        while True:
            conn, ret_addr = socket.accept()

            with conn:
                while True:
                    msg_len = int.from_bytes(conn.recv(2))
                    if not msg_len:
                        break
                    msg = conn.recv(msg_len)
                    conn.sendall(msg.decode().upper().encode())


if __name__ == "__main__":
    startServer()
