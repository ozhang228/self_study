import socket as sock


def startClient():
    with sock.socket(family=sock.AF_INET, type=sock.SOCK_STREAM) as socket:
        socket.connect(("localhost", 3000))

        while True:
            msg = input("Enter message to send: ").encode()

            socket.send(len(msg).to_bytes(2))
            socket.send(msg)

            res = socket.recv(len(msg))
            print(res)


if __name__ == "__main__":
    startClient()
