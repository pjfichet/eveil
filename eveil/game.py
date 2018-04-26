import queue
from time import sleep
from datetime import datetime

from .data import Data
from .player import Player
from .parser import Parser
from .utils import log
from . import world


class Game():

    def __init__(self, queue):
        self.queue = queue
        self.db = Data("data.db")
        self.parser = Parser(self)
        self.loop = True

    def run(self):
        while self.loop == True:
            self._get_queue()
            sleep(.1)

    def _get_queue(self):
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
                client.player = player
                world.clients.append(client)
            elif kind == "disconnect":
                if client.player is not None:
                    client.player.logout()
                world.clients.remove(client)
            self.queue.task_done()

    def shutdown(self):
        log("Recording datas before shutdown.")
        self.loop = False
        for client in world.clients:
            if client.player is not None:
                client.player.logout()
            world.clients.remove(client)
            client.send("<h4>Au revoir.</h4>")
            client.close()
        log("Shutting down.")
