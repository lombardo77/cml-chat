import socket
import threading as threads
import os
import signal
import sys


# listens for messages from the sever asynchronously
# TODO: somehow make it so that the prompt symbol copies into a new line
# when message is received
def listener():
    while True:
        msg = s.recv(2048).decode("ascii")
        print(f"\r{msg}", flush=True)
        print("> ", end="", flush=True)
        sys.stdin.flush()


# handles C-c by first sending "exit" to sever
def handle_sigint(sig, frame):
    s.send(b"exit")
    os._exit(0)


ip_addr = input("Please enter the host's ip-address: ")

signal.signal(signal.SIGINT, handle_sigint) # handle C-c interrupt

HOST = socket.gethostbyname(ip_addr)  # The server's hostname or IP address
PORT = 19000  # The port used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    t = threads.Thread(target=listener)
    t.start()
    while True:
        k = input("> ")
        s.send(str.encode(k))
        if k == "exit":
            os._exit(0)
