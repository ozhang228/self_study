import socket as sock


def startServer():
    with sock.socket(family=sock.AF_INET, type=sock.SOCK_DGRAM) as socket:
        socket.bind(("localhost", 3000))

        while True:
            msg_len = int.from_bytes(socket.recv(2))
            msg, client_addr = socket.recvfrom(msg_len)

            socket.sendto(msg.decode().upper().encode(), client_addr)


if __name__ == "__main__":
    startServer()
