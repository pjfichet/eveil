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

from datetime import datetime, timedelta

from .parser import State
from .grammar import Grammar
from .delay import Queue
from .remember import Remember
from .message import pose, info

def check_character_name(player, name):
    """Check if a name is valid."""
    if len(name) < 4:
        info(player,
             "Le nom du personnage doit contenir au moins quatre lettres.")
        return False
    if player.game.db.has('character', name):
        info(player,
             "Il existe déjà un personnage nommé {}."
             .format(name))
        return False
    return True



SHADOW = "Ombre"

class Character():
    """A character. Characters are created by the player, from the
    Player class. Their name must be unique. To a character are
    attached several objects, defining capabilities."""

    def __init__(self, game, player, name):
        self.game = game
        self.player = player
        # Fetch or create player datas
        if self.game.db.has('character', name):
            self.data = self.game.db.get('character', name)
            self.data['login_dt'] = datetime.now()
        else:
            self.data = {
                'uid' : self.game.db.uid(),
                'name' : name,
                'lastname' : 'Ombre',
                'gender' : Grammar.GENDERS.index("neutre"),
                'shortdesc' : "l'ombre d'un personnage",
                'longdesc' : "Une ombre informe, vaguement visible.",
                'pose' : 'est ici',
                'roomuid' : self.game.map.rooms[0].uid,
                'login_dt' : datetime.now(),
                'logout_dt' : None,
                'play_time' : timedelta(seconds=0),
                'state' : State.CHARGEN,
            }
        self.game.db.put('character', self.data['name'], self.data)
        # Instanciate character components
        self.remember = Remember(self.game, self)
        self.queue = Queue(5) # 10 second interval
        self.grammar = Grammar(
            Grammar.NUMBERS.index("singulier"),
            Grammar.GENDERS.index("neutre"),
            )
        self.grammar.agree(
            Grammar.NUMBERS.index("singulier"),
            self.data['gender']
        )
        # put the character in grid
        for room in self.game.map.rooms:
            if room.uid == self.data['roomuid']:
                self.room = room
                break
        self.room.send_longdesc(self)
        self.room.add_character(self)
        pose(self, "/Il déambule par ici")
        self.game.log(
            "Character {} enters the game in room {}."
            .format(self.data['name'], self.data['roomuid']))

    def logout(self):
        """ Removes a character from the grid at logout."""
        self.data['logout_dt'] = datetime.now()
        play_time = self.data['logout_dt'] - self.data['login_dt']
        self.data['play_time'] = self.data['play_time'] + play_time
        self.game.db.put('character', self.data['name'], self.data)
        pose(self, "/Il se déconnecte.")
        self.game.log(
            "Character {} leaves the game from room {}."
            .format(self.data['name'], self.room.uid))
        if self in self.room.characters:
            # should be always true
            self.room.characters.remove(self)

    def set_name(self, name):
        """ Name or rename a character. This is also when the character is
        actually recorded in the database."""
        name = name.capitalize()
        if not check_character_name(self.player, name):
            return
        oldname = self.data['name']
        self.game.db.rem('character', oldname)
        self.data['name'] = name
        self.game.db.put('character', self.data['name'], self.data)
        self.game.log(
            "Character {} renamed {}."
            .format(oldname, self.data['name']))
        info(self.player,
            "Votre personnage se nomme {}."
            .format(self.data['name']))

    def set_gender(self, gender):
        """ Define the gender of the character """
        if gender not in Grammar.GENDERS:
            # parser.py takes care of this yet.
            return
        self.data['gender'] = Grammar.GENDERS.index(gender)
        self.grammar.agree(
            Grammar.NUMBERS.index("singulier"),
            self.data['gender'])
        self.game.db.put('character', self.data['name'], self.data)
        self.game.log("{} is of gender {} ({}).".format(
            self.data['name'],
            self.data['gender'],
            self.grammar.gender
            ))
        info(self.player, "{} est {} {}.".format(
            self.grammar.il.capitalize(),
            self.grammar.un,
            self.grammar.homme
            ))

    def set_shortdesc(self, shortdesc):
        """ Define the short description of the character."""
        if shortdesc[-1] in ('.', '?', '!'):
            shortdesc = shortdesc[:-1]
        shortdesc = shortdesc.lower()
        self.data['shortdesc'] = shortdesc
        self.game.db.put('character', self.data['name'], self.data)
        info(self.player, "{} est {}.".format(
            self.data['name'],
            self.data['shortdesc']
            ))

    def set_longdesc(self, longdesc):
        """ Define the long description of the character."""
        self.data['longdesc'] = longdesc
        self.game.db.put('character', self.data['name'], self.data)
        info(self.player, self.data['longdesc'])

    def set_room(self, room):
        self.room = room
        self.data['roomuid'] = room.uid
        self.game.db.put('character', self.data['name'], self.data)

    def tick(self, now):
        """ tick all objects. """
        self.queue.tick(now)
