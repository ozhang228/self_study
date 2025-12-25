# We will need the following module to generate randomized lost packets
import random
import socket as sock
import time

TIMEOUT_SEC = 3
serverSocket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
serverSocket.bind(("", 12000))
serverSocket.settimeout(TIMEOUT_SEC)

prev_seq = 0
while True:
    rand = random.randint(0, 10)
    try:
        message, address = serverSocket.recvfrom(1024)
        # 30% of packets are gone
        if rand < 4:
            print("Message Lost")
            continue

        message = message.upper()
        _, seq_num, packet_time = message.decode().split(" ")
        seq_num = int(seq_num)
        packet_time = float(packet_time)

        if seq_num != prev_seq + 1:
            print(f"Expected {prev_seq + 1} but got {seq_num}")
        print(f"Time Difference: {time.time() - packet_time}")

        prev_seq = seq_num
        serverSocket.sendto(message, address)
    except TimeoutError as _:
        print("Client Died")
