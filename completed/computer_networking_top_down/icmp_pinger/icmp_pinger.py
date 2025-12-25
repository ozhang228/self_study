import os
import select
import socket as socket
import struct
import sys
import time
from typing import Literal

# import binascii

TYPE_ICMP_ECHO_REQUEST = 8


def create_checksum(data: bytes) -> int:
    csum = 0
    count_to = (len(data) // 2) * 2
    count = 0

    while count < count_to:
        # Combine two adjacent bytes into one 16-bit number
        this_val = data[count + 1] * 256 + data[count]
        csum += this_val
        csum &= 0xFFFFFFFF
        count += 2

    if count_to < len(data):
        csum += data[-1]
        csum &= 0xFFFFFFFF

    # Add high 16 bits to low 16 bits
    csum = (csum >> 16) + (csum & 0xFFFF)
    csum += csum >> 16

    # One's complement
    answer = ~csum & 0xFFFF

    # Swap bytes
    answer = answer >> 8 | (answer << 8 & 0xFF00)

    return answer


RTT = float
TIMEOUT_MSG = "Request timed out."


def receiveOnePing(
    mySocket: socket.socket, ID: int, timeout: float, destAddr: str
) -> RTT | Literal["Request timed out."]:
    timeLeft = timeout

    while True:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = time.time() - startedSelect

        if whatReady[0] == []:
            return TIMEOUT_MSG

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fetch the ICMP header from the IP packet
        # ICMP starts after byte 20
        icmp_header = recPacket[20:28]
        icmp_type, code, chksum, packet_id, seq = struct.unpack("bbHHh", icmp_header)

        if icmp_type == 0 and packet_id == ID:
            # Extract timestamp that we sent
            time_sent = struct.unpack("d", recPacket[28:36])[0]

            rtt = (timeReceived - time_sent) * 1000
            return rtt

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return TIMEOUT_MSG


def sendOnePing(mySocket: socket.socket, destAddr: str, ID: int) -> None:
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0

    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", TYPE_ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header.
    myChecksum = create_checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == "darwin":
        # Convert 16-bit integers from host to network byte order
        myChecksum = socket.htons(myChecksum) & 0xFFFF
    else:
        myChecksum = socket.htons(myChecksum)

    header = struct.pack("bbHHh", TYPE_ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def doOnePing(destAddr: str, timeout: float) -> RTT | Literal["Request timed out."]:
    icmp = socket.getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details: http://sockraw.org/papers/sock_raw
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)

    ping_res = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()

    return ping_res


def ping(host: str, timeout: int = 1) -> None:
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = socket.gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")

    min_rtt = float("inf")
    max_rtt = float("-inf")
    num_packets = 0
    avg_rtt = 0

    # Send ping requests to a server separated by approximately one second
    while True:
        rtt = doOnePing(dest, timeout)

        if rtt == "Request timed out.":
            print(rtt)
            break

        num_packets += 1

        min_rtt = min(min_rtt, rtt)
        max_rtt = max(max_rtt, rtt)

        # Incremental mean theorem
        avg_rtt += (rtt - avg_rtt) / num_packets

        print(
            f"Min: {min_rtt:.3f} | Max: {max_rtt:.3f} | Avg: {avg_rtt:.3f} | Current: {rtt:.3f}"
        )

        time.sleep(1)


ping("127.0.0.1")
