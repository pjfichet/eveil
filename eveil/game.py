import queue
from time import sleep
from datetime import datetime

from .data import Data
from .player import Player
from .parser import Parser


class Game():

    def __init__(self, queue):
        self.queue = queue
        self.clients = []
        self.players = []
        self.characters = []
        self.rooms = []
        self.db = Data(self, "data.db")
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
                player = Player(self, client)
                client.player = player
                self.clients.append(client)
            elif kind == "disconnect":
                if client.player is not None:
                    client.player.logout()
                self.clients.remove(client)
            self.queue.task_done()

    def log(self, message):
        print("{}: {}".format(datetime.now(), message))

    def shutdown(self):
        self.log("Recording datas before shutdown.")
        self.loop = False
        for client in self.clients:
            if client.player is not None:
                client.player.logout()
            self.clients.remove(client)
            client.send("<h4>Au revoir.</h4>")
            client.close()
        self.log("Shutting down.")
