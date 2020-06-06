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
import os

from .game import Game
from .server import ThreadServer

queue = queue.Queue()
game = Game(queue)

#cwd = os.getcwd()
#world = os.path.join(cwd, 'world')
for filename in os.listdir('world'):
    if filename.endswith('.py'):
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
