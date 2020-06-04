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

from datetime import datetime

from .parser import State
from .grammar import Grammar
from .delay import Queue
from .remember import Remember
from .expose import pose, info

def check_character_name(player, name):
    """Check if a name is valid."""
    if len(name) < 4:
        info(player,
             "Le nom du personnage doit contenir au moins quatre lettres.")
        return False
    if player.game.db.get('character:' + name):
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
        self.key = 'character:' + name
        # Fetch or create player datas
        if not self._get():
            self.data = {
                'name' : name
                'lastname' : 'Ombre',
                'gender' : Grammar.GENDERS.index("neutre"),
                'shortdesc' : "l'ombre d'un personnage",
                'longdesc' : "Une ombre informe, vaguement visible.",
                'pose' : 'est ici',
                'roomid' : 0,
                'login_dt' : None,
                'logout_dt' : None,
                'play_time' : None,
                'state' : State.CHARGEN,
            }
        self.data['login_dt'] = datetime.now()
        self._put()
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
            if room.id == self.data['roomid']:
                self.room = room
                break
        self.room.send_longdesc(self)
        self.room.add_character(self)
        pose(self, "/Il déambule par ici")
        self.game.log("Character {} enters the game in room {}.")


    def _get(self):
        """ With the character name, extract datas from the db."""
        self.data = self.game.db.get(self.key)
        return bool(self.data)

    def _put(self):
        """ Record the datas of the character in the db."""
        self.game.db.put(self.key, self.data)

    def logout(self):
        """ Removes a character from the grid at logout."""
        self.data['logout_dt'] = datetime.now()
        self.data['play_time'] = self.data['logout_dt'] - self.data['login_dt']
        self._put()
        pose(self, "/Il se déconnecte.")
        self.game.log(
            "Character {} leaves the game from room {}."
            .format(self.data['name'], self.room.id))
        if self in self.room.characters:
            # should be always true
            self.room.characters.remove(self)
        if self in self.game.characters:
            self.game.characters.remove(self)

    def set_name(self, name):
        """ Name or rename a character. This is also when the character is
        actually recorded in the database."""
        name = name.capitalize()
        if not check_character_name(self.player, name):
            return
        self.remember.rename(name)
        oldname = self.data['name']
        self.game.db.rem(self.key)
        self.data['name'] = name
        self.key = 'character:' + self.data['name']
        self._put()
        self.game.log(
            "Character {} renamed {}."
            .format(oldname, self.data['name']))
        self.player.client.send(
            "<p>Votre personnage se nomme {}.</p>"
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
        self._put()
        self.game.log("{} is of gender {} ({}).".format(
            self.data['name'],
            self.data['gender'],
            self.grammar.gender
            ))
        self.player.client.send("<p>{} est {} {}.</p>".format(
            self.grammar.il.capitalize(),
            self.grammar.un,
            self.grammar.homme
            ))

    def set_shortdesc(self, shortdesc):
        """ Define the short description of the character."""
        self.data['shortdesc'] = shortdesc
        self._put()
        self.player.client.send("</p>{} est {}.</p>".format(
            self.data['name'],
            self.data['shortdesc']
            ))

    def set_longdesc(self, longdesc):
        """ Define the long description of the character."""
        self.data['longdesc'] = longdesc
        self._put()
        self.player.client.send("<p>{}</p>".format(self.data['longdesc']))

    def tick(self, now):
        """ tick all objects. """
        self.queue.tick(now)
