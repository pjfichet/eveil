import queue

from .game import Game
from .server import ThreadServer
from .objects import chargen

queue = queue.Queue()
game = Game(queue)
server = ThreadServer(queue, '', 5678)
server.setDaemon(True)
server.start()
game.run()
