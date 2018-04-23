import threading
import queue
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

queue = queue.Queue()

class Connection(WebSocket):

    def handleMessage(self):
        self.queue.put([self, "text", self.data])

    def handleConnected(self):
        self.queue.put([self, "connect", ""])

    def handleClose(self):
        self.queue.put([self, "disconnect", ""])

    def setplayer(self, player):
        self.player = player

    def setqueue(self, queue):
        self.queue = queue

class Server(SimpleWebSocketServer):

    def __init__(self, queue, host, port, websocketclass):
        SimpleWebSocketServer.__init__(self, host, port, websocketclass)
        self.queue = queue

    def _constructWebSocket(self, sock, address):
        connection = self.websocketclass(self, sock, address)
        connection.setqueue(self.queue)
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

