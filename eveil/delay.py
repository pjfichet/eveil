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

### From https://stackoverflow.com/questions/10154568

from datetime import datetime, timedelta

class QueuedFunction():
    """A function stored for later usage."""

    def __init__(self, function, *args):
        self.function = function
        self.args = args

    def execute(self):
        self.function(*self.args)

class Queue():
    """Store a queue of commands, execute them after a delay."""

    def __init__(self, seconds):
        self.queue = []
        self.pause = False

    def tick(self):
        if self.pause:
            return
        if self.queue:
            function = self.queue.pop(0)
            function.execute()

    def add(self, function, *args):
        fn = QueuedFunction(function, *args)
        self.queue.append(fn)

    def stop(self):
        self.queue = []

    def pause(self):
        if self.pause:
            self.pause = False
        else:
            self.pause = True
