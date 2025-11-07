import base64
import socket as sock
import ssl
from types import TracebackType
from typing import Type

from google_auth_oauthlib.flow import InstalledAppFlow

MSG = "\r\n I love computer networks!"
END_MSG = "\r\n.\r\n"


MAIL_SERVER_HOSTNAME = "smtp.gmail.com"
MAIL_SERVER_PORT = 465


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

    def auth_login(self, email: str, token: str) -> None:
        SCOPES = ["https://mail.gmail.com/"]
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        print(creds.token)

        # self.get_ssock().send((base64.b64encode("AUTH XOAUTH2 1".encode()) + b"\r\n"))
        # print(self.get_ssock().recv(1024).decode())

        pass

    def start_session(self) -> str:
        helo_cmd = "HELO Alice\r\n"
        self.get_ssock().send(helo_cmd.encode())

        helo_res = self.get_ssock().recv(1024).decode()

        print(helo_res)
        if helo_res[:3] != "250":
            raise Exception("250 reply not received from server.")

        self.auth_login("hi", "hi")

        return helo_res

    def send_email(self, from_email: str, to_email: str) -> str:
        # self.get_ssock().send(f"MAIL FROM:{from_email}\r\n".encode())
        # print(self.get_ssock().recv(1024))

        return ""


def main():
    # Create socket called clientSocket and establish a TCP connection with mailserver
    ssl_context = ssl.create_default_context()
    with SMTPClient(
        ssl_context=ssl_context,
        server_hostname=MAIL_SERVER_HOSTNAME,
        server_port=MAIL_SERVER_PORT,
    ) as smtp_client:
        smtp_client.send_email(
            from_email="tracyyguo15@gmail.com", to_email="oscarzhang228@gmail.com"
        )
        pass

    # Send MAIL FROM command and print server response.
    # Fill in start
    # Fill in end
    # Send RCPT TO command and print server response.
    # Fill in start
    # Fill in end
    # Send DATA command and print server response.
    # Fill in start
    # Fill in end
    # Send message data.
    # Fill in start
    # Fill in end
    # Message ends with a single period.
    # Fill in start
    # Fill in end
    # Send QUIT command and get server response.
    # Fill in start
    # Fill in end
    pass


if __name__ == "__main__":
    main()
