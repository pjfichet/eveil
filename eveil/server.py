import threading
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class Connection(WebSocket):

    def __init__(self, server, sock, address):
        WebSocket.__init__(self, server, sock, address)
        self.player = None
        self.queue = None

    def handleMessage(self):
        self.queue.put([self, "text", self.data])

    def handleConnected(self):
        self.queue.put([self, "connect", ""])

    def handleClose(self):
        self.queue.put([self, "disconnect", ""])

    def send(self, message):
        self.sendMessage("<div>" + message + "</div>")


class Server(SimpleWebSocketServer):

    def __init__(self, queue, host, port, websocketclass):
        SimpleWebSocketServer.__init__(self, host, port, websocketclass)
        self.queue = queue

    def _constructWebSocket(self, sock, address):
        connection = self.websocketclass(self, sock, address)
        connection.queue = self.queue
        return connection


class ThreadServer(threading.Thread):

    def __init__(self, queue, host, port):
        threading.Thread.__init__(self)
        self.queue = queue
        self.host = host
        self.port = port

    def run(self):
        self.server = Server(self.queue, self.host, self.port, Connection)
        self.server.serveforever()

