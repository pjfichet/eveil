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

import threading
from .SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class Connection(WebSocket):

    def __init__(self, server, sock, address):
        WebSocket.__init__(self, server, sock, address)
        self.player = None
        self.queue = None

    def handleMessage(self):
        self.queue.put([self, "text", self.data])

    def handleConnected(self):
        self.queue.put([self, "connect", ""])

    def handleClose(self):
        self.queue.put([self, "disconnect", ""])

    def send(self, message):
        self.sendMessage("<div>" + message + "</div>")


class Server(SimpleWebSocketServer):

    def __init__(self, queue, host, port, websocketclass):
        SimpleWebSocketServer.__init__(self, host, port, websocketclass)
        self.queue = queue

    def _constructWebSocket(self, sock, address):
        connection = self.websocketclass(self, sock, address)
        connection.queue = self.queue
        return connection


class ThreadServer(threading.Thread):

    def __init__(self, queue, host, port):
        threading.Thread.__init__(self)
        self.queue = queue
        self.host = host
        self.port = port

    def run(self):
        self.server = Server(self.queue, self.host, self.port, Connection)
        self.server.serveforever()

