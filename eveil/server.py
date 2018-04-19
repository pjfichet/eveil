import threading
import queue
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

queue = queue.Queue()

class Server(WebSocket):

    def handleMessage(self):
        #self.sendMessage(self.data)
        queue.put([self, "text", self.data])

    def handleConnected(self):
        queue.put([self, "connect", ""])

    def handleClose(self):
        queue.put([self, "disconnect", ""])

    def setPlayer(self, player):
        self.player = player

    def setState(self, state):
        # Do not use self.state since it would conflict
        # with the class WebSocket.
        self.status = state

    def getState(self):
        return self.status


class ThreadServer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        self.server = SimpleWebSocketServer('', 5678, Server)
        self.server.serveforever()

