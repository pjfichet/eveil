# Copyright (C) 2018 Pierre Jean Fichet
# <pierrejean dot fichet at posteo dot net>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import queue
from time import sleep
from datetime import datetime, timedelta

from .data import Data
from .player import Player
from .parser import Parser
from .map import Map
from .time import Time


class Game():

    def __init__(self, queue):
        self.queue = queue
        self.clients = []
        now = datetime.now()
        # take care to not tick everything at the same time
        self.tick = {
            'delay' : now + timedelta(seconds=1),
            'time' : now + timedelta(seconds=2),
            'character' : now + timedelta(seconds = 3),
            }
        self.db = Data(self.log, "data.db")
        self.parser = Parser(self)
        self.map = Map(self)
        self.time = Time(self)
        self.loop = True

    def run(self):
        while self.loop == True:
            now = datetime.now()
            self._get_queue()
            # tick delays every 5 seconds
            if now >= self.tick['delay']:
                self.tick['delay'] = now + timedelta(seconds=5)
                for client in self.clients:
                    if client.player.character:
                        client.player.character.queue.tick()
            # tick time every 20 seconds
            if now >= self.tick['time']:
                self.tick['time'] = now + timedelta(seconds=20)
                self.time.tick()
            # tick characters every minutes
            if now >= self.tick['character']:
                self.tick['character'] = now + timedelta(seconds=60)
                for client in self.clients:
                    if client.player.character:
                        client.player.character.tick(now)
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
