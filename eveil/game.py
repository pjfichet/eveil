import queue
from time import sleep

from .data import Data
from .player import Player
from .parser import Parser
from . import world


class Game():

    def __init__(self, queue):
        self.queue = queue
        self.db = Data("data.db")
        self.parser = Parser(self)
        self.loop = True

    def shutdown(self):
        self.loop = False
        self.db.close()

    def run(self):
        while self.loop == True:
            self.parsequeue()
            sleep(.1)

    def parsequeue(self):
        try:
            # With False, the queue does not block the program.
            # It raises Queue.Empty if empty.
            client, kind, message = self.queue.get(False) 
        except queue.Empty:
            kind = None
        if kind is not None:
            if kind == "text":
                self.parser.parse(client.player, message)
            if kind == "connect":
                player = Player(self.db, client)
                client.setplayer(player)
                world.clients.append(client)
            elif kind == "disconnect":
                client.player.logout()
                world.clients.remove(client)
            self.queue.task_done()

    def shutdown(self):
        self.loop = False
