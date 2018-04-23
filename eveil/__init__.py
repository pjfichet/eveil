from .server import ThreadServer
from .game import Game
from .objects import chargen

server = ThreadServer()
server.setDaemon(True)
server.start()
game = Game(server.queue)
game.run()
