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

"""
Database format:

The keys are of the form <prefix>:<suffix>.

<prefix> defines the kind of object (player, character, room...)

<suffix> identifies the object, and must be unique for that object.
<suffix> is either a human choosen name (player, character, or room
name), either a randomly generated uid.

We use a simple uid generator, and record each used uid in the
uid:<uid> key of the database.

KEY                         DATA
game:time                   {minute, hour, day, month, ...}
game:init                   datetime
uid:<uid>                   1
player:<name>               {uid, pseudo, password, email, ...}
character:<name>            {uid, pseudo, password, email, ...}
remember:<character_uid>    {name: remembered name, ...}
room:<name>                 uid
container:<uid>             {...}
"""

import shelve
import random
from datetime import datetime

class Data:
    """
    Implements a simple database.
    """

    PREFIX = ('game', 'player', 'character', 'remember', 'room', 'container')

    def __init__(self, game, filename):
        """
        Open the file containing the data.
        """
        self.game = game
        self.filename = filename
        self.db = shelve.open(self.filename)
        if self.has('game', 'init'):
            init = self.get('game', 'init')
            self.game.log("Opening {} created on {}".format(self.filename, init))
        else:
            self.game.log("Creating {}".format(self.filename))
            self.put('game', 'init', datetime.now())


    def _check_prefix(self, prefix):
        """Check the prefix matches one of the accepted prefixes."""
        if prefix not in Data.PREFIX:
            self.game.log("Invalid data prefix {}.".format(prefix))
            return False
        return True

    def _smallid(self):
        """Generates a smallid. There are 57^6 = 34.296.447.249
        possibilities.
        """
        alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        return ''.join(random.choice(alphabet) for x in range(6))

    def uid(self):
        """Gets a unique id, by generating a smallid and checking it
        is indeed unique. The uid is recorded, to be sure we don't use
        it again accidently.
        """
        uid = self._smallid()
        i = 1
        while 'uid:' + uid in self.db:
            # could eventually be a long loop if
            # the smallid generator is not random enough.
            uid = self._smallid()
            i = i + 1
        if i > 1:
            # logs to alert on the lack of randomness.
            self.game.log("Uid generated in {} rounds.".format(i))
        self.db['uid:' + uid] = 1
        return uid

    def has(self, prefix, suffix):
        """ Check if the key is present in the db.
        """
        key = prefix + ':' + suffix
        if key in self.db:
            return True
        return False

    def new(self, prefix, data):
        if not self._check_prefix(prefix):
            return None
        uid = self.uid()
        self.db[prefix + ':' + uid] = data
        return uid

    def put(self, prefix, suffix, data):
        """Record a data. It needs an existing uid.
        """
        if not self._check_prefix(prefix):
            return False
        self.db[prefix + ':' + suffix] = data
        return True

    def get(self, prefix, suffix):
        """Fetch data for a given suffix (uid or name).
        """
        if not self._check_prefix(prefix):
            return None
        try:
            return self.db[prefix + ':' + suffix]
        except KeyError:
            return None

    def rem(self, prefix, suffix):
        """ Delete an entry. This deletes all data relative to a name.
        The uid is lost, and meaningless after that operation.
        """
        if not self._check_prefix(prefix):
            return False
        key = prefix + ':' + suffix
        if key in self.db:
            del self.db[prefix + ':' + suffix]
        key = 'uid:' + suffix
        if key in self.db:
            del self.db['uid:' + suffix]
        return True

    def close(self):
        """Close the database."""
        self.game.log("Closing {}.".format(self.filename))
        self.db.close()

    def serialize(self, function):
        """Apply a function to all the entries of the database."""
        for key in self.db:
            function(key)
