import socket as sock
import time
from abc import ABC, abstractmethod
from typing import override

target_host = "127.0.0.1"
target_port = 12000
send_num = 10

ReturnAddress = str


class AbstractSocketDao(ABC):
    @abstractmethod
    def __init__(
        self, address_family: sock.AddressFamily, sock_kind: sock.SocketKind
    ) -> None: ...

    @abstractmethod
    def set_timeout(self, timeout_sec: float) -> None: ...

    @abstractmethod
    def sent_to(self, message: str, host: str, port: int) -> None: ...

    @abstractmethod
    def recv_from(self, num_bytes: int) -> tuple[bytes, ReturnAddress]: ...


class SocketDao(AbstractSocketDao):
    def __init__(
        self, address_family: sock.AddressFamily, sock_kind: sock.SocketKind
    ) -> None:
        self.socket = sock.socket(address_family, sock_kind)

    @override
    def set_timeout(self, timeout_sec: float) -> None:
        self.socket.settimeout(timeout_sec)

    @override
    def sent_to(self, message: str, host: str, port: int) -> None:
        self.socket.sendto(message.encode(), (host, port))

    @override
    def recv_from(self, num_bytes: int) -> tuple[bytes, ReturnAddress]:
        return self.socket.recvfrom(num_bytes)


if __name__ == "__main__":
    client_sock = SocketDao(sock.AF_INET, sock.SOCK_DGRAM)
    client_sock.set_timeout(1)

    min_rtt = float("inf")
    max_rtt = float("-inf")
    avg_rtt = 0
    num_packets_recv = 0

    for seq_num in range(1, 11):
        start_time = time.time()
        message = f"Ping {seq_num} {start_time}"
        client_sock.sent_to(message, target_host, target_port)

        print(f"===Packet {seq_num}===")
        try:
            res, addr = client_sock.recv_from(1024)
            rtt = time.time() - start_time
            min_rtt = min(min_rtt, rtt)
            max_rtt = max(max_rtt, rtt)
            avg_rtt = ((avg_rtt * num_packets_recv) + rtt) / (num_packets_recv + 1)
            num_packets_recv += 1

            print(f"Response: {res}")
            print(f"Min, Max, Avg RTT: {min_rtt} {max_rtt} {avg_rtt}")
        except Exception as _:
            print("Request timed out")

        packet_loss_rate = (
            1 - (num_packets_recv / seq_num) if num_packets_recv / seq_num > 0 else 1
        )
        print(f"Packet Loss Rate: {packet_loss_rate:.2%}")
