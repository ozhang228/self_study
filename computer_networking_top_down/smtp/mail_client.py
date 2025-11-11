import argparse
import base64
import socket as sock
import ssl
from types import TracebackType
from typing import Type

from google_auth_oauthlib.flow import InstalledAppFlow
from pydantic import BaseModel

MAIL_SERVER_HOSTNAME = "smtp.gmail.com"
MAIL_SERVER_PORT = 465


def print_log(msg: str) -> None:
    """
    Emulates a logging statement
    """

    print(f"[Log]: {msg}")


# TODO: make socket an object that can be stubbed in order to test
class SMTPClient:
    def __init__(
        self, ssl_context: ssl.SSLContext, server_hostname: str, server_port: int
    ) -> None:
        self.ssl_context = ssl_context
        self.server_hostname = server_hostname
        self.server_port = server_port

        self.sock: sock.socket | None = None
        self.ssock: ssl.SSLSocket | None = None

    def __enter__(self) -> "SMTPClient":
        self.sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.ssock = self.ssl_context.wrap_socket(
            sock=self.sock, server_hostname=self.server_hostname
        )
        self.ssock.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.ssock.connect((self.server_hostname, self.server_port))
        recv = self.ssock.recv(1024).decode()

        if recv[:3] != "220":
            raise Exception("220 reply not received from server.")

        self.start_session()

        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType,
    ) -> bool:
        quit_msg = "QUIT\r\n"
        print_log(f"Client: {quit_msg}")
        self.get_ssock().send(quit_msg.encode())
        print_log(f"Server: {self.get_ssock().recv(1024)}")

        self.get_sock().close()
        self.get_ssock().close()

        return False

    def get_sock(self) -> sock.socket:
        if not self.sock:
            raise Exception("Socket not initalized")

        return self.sock

    def get_ssock(self) -> ssl.SSLSocket:
        if not self.ssock:
            raise Exception("SSLSocket not initalized")

        return self.ssock

    def auth_login(self, email: str) -> bool:
        SCOPES = ["https://mail.google.com/"]
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server()

        self.get_ssock().send(
            b"AUTH XOAUTH2 "
            + base64.b64encode(
                f"user={email}\x01auth=Bearer {creds.token}\x01\x01".encode()
            )
            + b"\r\n"
        )
        auth_res = self.get_ssock().recv(1024).decode()

        if auth_res[:3] != "235":
            print_log("OAUTH failed " + auth_res)
            return False
        else:
            print_log(f"Successfully authenticated as {email}")
            return True

    def start_session(self) -> bool:
        helo_cmd = "HELO Alice\r\n"
        self.get_ssock().send(helo_cmd.encode())

        helo_res = self.get_ssock().recv(1024).decode()

        if helo_res[:3] != "250":
            print_log("250 reply not received from server.")
            return False

        return True

    def send_email(self, from_email: str, to_email: str, msg: str) -> bool:
        if not self.auth_login(from_email):
            return False

        mail_from_msg = f"MAIL FROM:<{from_email}>\r\n".encode()
        print_log(f"Client: {mail_from_msg}")
        self.get_ssock().send(mail_from_msg)
        mail_from_res = self.get_ssock().recv(1024)

        if mail_from_res[:3] != b"250":
            print_log(f"MAIL FROM failed with response {mail_from_res}")
            return False
        print_log(f"Server: {mail_from_res}")

        rept_to_msg = f"RCPT TO:<{to_email}>\r\n".encode()
        print_log(f"Client: {rept_to_msg}")
        self.get_ssock().send(rept_to_msg)
        rept_to_res = self.get_ssock().recv(1024)

        if rept_to_res[:3] != b"250":
            print_log(f"RCPT TO failed with response {rept_to_res}")
            return False
        print_log(f"Server: {rept_to_res}")

        data_msg = "DATA\r\n".encode()
        print_log(f"Client: {data_msg}")
        self.get_ssock().send(data_msg)
        data_res = self.get_ssock().recv(1024)

        if data_res[:3] != b"354":
            print_log(f"DATA failed with response {data_res}")
            return False
        print_log(f"Server: {data_res}")

        msg_data = f"{msg}\r\n.\r\n".encode()
        print_log(f"Client: {msg_data}")
        self.get_ssock().send(msg_data)
        msg_res = self.get_ssock().recv(1024)

        if msg_res[:3] != b"250":
            print_log(f"Sending message data failed with response {msg_res}")
        print_log(f"Server: {msg_res}")

        return True


class Arguments(BaseModel):
    src: str
    dst: str


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", type=str)
    parser.add_argument("-d", "--dst", type=str)
    namespace = parser.parse_args()

    args = Arguments(src=namespace.src, dst=namespace.dst)

    # Create socket called clientSocket and establish a TCP connection with mailserver
    ssl_context = ssl.create_default_context()
    with SMTPClient(
        ssl_context=ssl_context,
        server_hostname=MAIL_SERVER_HOSTNAME,
        server_port=MAIL_SERVER_PORT,
    ) as smtp_client:
        while True:
            msg = input("Enter a message or ':Exit' in order to quit:\n")

            if msg == ":Exit":
                break

            smtp_client.send_email(from_email=args.src, to_email=args.dst, msg=msg)


if __name__ == "__main__":
    main()
