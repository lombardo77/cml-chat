from textual.app import App
from textual import on
from textual.message import Message
from textual.widgets import Static, Header, Footer, Input, Label
import socket
import threading as threads
import time


class Chat(Static):
    sock = None

    def __init__(self, ip_addr, *args, **kwargs):
        self.ip_addr = ip_addr
        super().__init__(*args, **kwargs)

    class Inmsg(Message):
        def __init__(self, msg):
            self.msg = msg
            super().__init__()

    def on_mount(self):
        conn = threads.Thread(target=self.conn_server)
        conn.daemon = True
        conn.start()
        lis = threads.Thread(target=self.lis_server)
        lis.daemon = True
        lis.start()

    def conn_server(self):
        HOST = socket.gethostbyname(self.ip_addr)
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
    CSS = """
    .me {
        border: ascii blue;
    }

    .others {
        border: ascii white;
    }
    """

    def on_mount(self):
        self.mount(Input(placeholder="Host IP", id="ip-addr"))
        # self.mount(Input(placeholder="Access Key", id="key"))

    @on(Input.Submitted, "#input")
    def msg_submitted(self):
        chat = self.query_one("#chat", Chat)
        input = self.query_one("#input", Input)
        self.mount(Label("<me> " + input.value, classes="me"))
        chat.sock.send(str.encode(input.value))
        input.value = ""

    def on_chat_inmsg(self, event: Chat.Inmsg):
        self.mount(Label(event.msg, classes="others"))

    @on(Input.Submitted, "#ip-addr")
    def ipaddr_submitted(self):
        ip_addr_item = self.query_one("#ip-addr", Input)
        ip_addr = ip_addr_item.value
        ip_addr_item.remove()
        self.mount(Input(placeholder="message", id="input"))
        self.mount(Chat(ip_addr, id="chat"))


    @on(Input.Submitted, "#ip-addr")
    def key_submitted(self):
        pass


if __name__ == "__main__":
    Myapp().run()
