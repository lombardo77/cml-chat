from textual.app import App
from textual.message import Message
from textual.widgets import Static, Header, Footer, Input, Label
import socket
import threading as threads
import time
import os


class Chat(Static):
    sock = None

    class Inmsg(Message):
        def __init__(self, msg):
            self.msg = msg
            super().__init__()

    def on_mount(self):
        self.mount(Label("chat"))
        conn = threads.Thread(target=self.conn_server)
        conn.daemon = True
        conn.start()
        lis = threads.Thread(target=self.lis_server)
        lis.daemon = True
        lis.start()

    def conn_server(self):
        HOST = socket.gethostbyname("127.0.0.1")
        PORT = 19000
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            self.sock = s
            while True:
                pass

    # listens for messages from the sever asynchronously
    def lis_server(self):
        time.sleep(3)
        while True:
            msg = self.sock.recv(2048).decode("ascii")
            self.post_message(self.Inmsg(msg))


class Myapp(App):
    def on_mount(self):
        self.mount(Input(placeholder="message", id="input"))
        self.mount(Chat(id="chat"))

    def on_input_submitted(self, event: Input.Submitted):
        chat = self.query_one("#chat", Chat)
        self.mount(Label("<me> " + event.value))
        chat.sock.send(str.encode(event.value))
        event.value = ""

    def on_chat_inmsg(self, event: Chat.Inmsg):
        self.mount(Label(event.msg))


if __name__ == "__main__":
    Myapp().run()
