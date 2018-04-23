import queue
from time import sleep

from .data import Data
from .player import Player
from .parser import Parser
from . import world


class Game():

    def __init__(self, queue):
        self.queue = queue
        self.loop = True
        self.db = Data("data.db")
        self.parser = Parser()

    def shutdown(self):
        self.loop = False
        self.db.close()
 
    def run(self):
        while self.loop == True:
            self.parsequeue()
            sleep(.1)

    def parsequeue(self):
        # check queue
        try:
            # With False, the queue does not block the program
            # It raises Queue.Empty if empty.
            client, kind, message = self.queue.get(False) 
        except queue.Empty:
            kind = None
        if kind is not None:
            if message == "shutdown":
                self.shutdown()
            elif kind == "connect" and client not in world.clients:
                world.clients.append(client)
                player = Player(self.db, client)
                client.setPlayer(player)
            elif kind == "disconnect" and client in world.clients:
                world.clients.remove(client)
            else:
                self.parser.parse(client.player, message)
            self.queue.task_done()
      
  
