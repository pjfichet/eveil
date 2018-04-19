import queue
from time import sleep

from .data import Data
from .player import Player
from .parser import Parser

class Game():

    def __init__(self, queue):
        self.clients = []
        self.queue = queue
        self.loop = True
        self.db = Data("data.db")
        self.parser = Parser()

    def run(self):
        while self.loop == True:
            self.tick()
            sleep(.1)

    def tick(self):
        # check queue
        client, kind, message = self.queue.get() 
        if message == "shutdown":
            self.shutdown()
        elif kind == "connect" and client not in self.clients:
            self.clients.append(client)
            player = Player(self.db, client)
            client.setPlayer(player)
        elif kind == "disconnect" and client in self.clients:
            self.clients.remove(client)
        else:
            self.parser.parse(client.player, message)
        self.queue.task_done()
    
    def handleMessage(self, client, message):
        client.sendMessage(message)
   
    def shutdown(self):
        self.loop = False
        self.db.close()
   
