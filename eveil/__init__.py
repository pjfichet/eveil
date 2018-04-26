import queue
import os

from .game import Game
from .server import ThreadServer

queue = queue.Queue()
game = Game(queue)

#cwd = os.getcwd()
#world = os.path.join(cwd, 'world')
for filename in os.listdir('world'):
    filepath = os.path.join('world', filename)
    if os.path.isfile(filepath):
        game.log("Charging {}".format(filepath))
        exec(
            compile(open(filepath, "rb").read(), filepath, 'exec')
            )


server = ThreadServer(queue, '', 5678)
server.setDaemon(True)
server.start()
game.run()
