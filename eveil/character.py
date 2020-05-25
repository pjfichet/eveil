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

from .grammar import Grammar
from .grammar import apostrophe

SHADOW = "l'ombre d'un personnage"

class Character():
    SKILLS = ["artisan", "chasseur", "druide", "guerrier", "barde"]
    TALENTS = ["agileté", "constitution", "force", "intelligence", "sagesse"]

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.id = None
        self.key = None
        self.name = SHADOW
        self.lastname = None
        self.gender = None
        self.longdesc = None
        self.shortdesc = None
        self.skill = None
        self.talent = None
        self.remember = {}
        self.room = self.game.map.rooms[0]
        self.roomid = self.room.id
        self.grammar = Grammar(
                Grammar.NUMBERS.index("singulier"),
                Grammar.GENDERS.index("neutre"),
                )

    def _get(self):
        """ With the character name, extract datas from the db."""
        self.id = self.game.db.get("character:" + self.name)
        if self.id:
            self.key = "character:" + str(self.id)
            data = self.game.db.get(self.key)
            self.lastname = data["lastname"]
            self.gender = data["gender"]
            self.roomid = data["roomid"]
            self.longdesc = data["longdesc"]
            self.shortdesc = data["shortdesc"]
            self.skill = data["skill"]
            self.talent = data["talent"]
            self.remember = data["remember"]
            self.grammar.agree(Grammar.NUMBERS.index("singulier"), self.gender)
            return True
        else:
            return  False

    def _put(self):
        """ Record the datas of the character in the db."""
        self.key = "character:" + str(self.id)
        self.game.db.put(
            self.key,
            {"name": self.name, "lastname": self.lastname,
            "gender": self.gender, "roomid": self.room.id, 
            "longdesc": self.longdesc, "shortdesc": self.shortdesc,
            "skill": self.skill, "talent": self.talent,
            "remember": self.remember
            })

    def _new(self):
        """ Record a new character in the db."""
        self.id = self.game.db.new("character")
        self.game.db.put("character:" + self.name, self.id)
        self._put()
        self.player.record_character()

    def create(self):
        """ If the character has data in the db, fetch them,
        and in all case, put the character in game."""
        if self.name is not SHADOW:
            self._get()
            self.game.characters.append(self)
        self.game.log("Character {} enters the game in room {}."
                .format(self.name, self.room.id)
                )
        self.room.send_longdesc(self)
        self.room.add_character(self)
        #if self.name is not SHADOW:
        self.room.send_all("<p>{} arrive ici.</p>".format(self.name.capitalize()))

    def set_name(self, name):
        """ Name or rename a character. This is also when the character is
        actually recorded in the database."""
        name = name.capitalize()
        if self.name is not SHADOW:
            self.name = name
            self._put()
        else:
            self.name = name
            self._new()
        self.player.client.send("<p>Votre personnage se nomme {}.</p>".format(
            self.name
            ))
        self.game.log("Character {} created.".format(self.name))

    def set_gender(self, gender):
        """ Define the gender of the character """
        if gender not in Grammar.GENDERS:
            # parser.py takes care of this yet.
            return
        self.gender = Grammar.GENDERS.index(gender)
        self.grammar.agree(Grammar.NUMBERS.index("singulier"), self.gender)
        if self.name is not SHADOW:
            self.game.log("{} is of gender {} ({}).".format(
                self.name,
                self.gender,
                self.grammar.gender
                ))
            self._put()
        self.player.client.send("<p>{} est {} {}.</p>".format(
                self.grammar.il.capitalize(),
                self.grammar.un,
                self.grammar.homme
                ))

    def set_shortdesc(self, shortdesc):
        """ Define the short description of the character."""
        self.shortdesc = shortdesc
        self.player.client.send("</p>{} est {}.</p>".format(
            self.name,
            self.shortdesc
            ))
        self._put()

    def set_longdesc(self, longdesc):
        """ Define the long description of the character."""
        self.longdesc = longdesc
        self.player.client.send("<p>{}</p>".format(self.longdesc))
        self._put()

    def set_skill(self, skill):
        """ Define the skill of the character. """
        self.skill = Character.SKILLS.index(skill)
        self.player.client.send(
                "<p>C'est {} {}.".format(
                    self.grammar.un,
                    Character.SKILLS[self.skill])
                )
        self._put()

    def set_talent(self, talent):
        """ Define the talent of the character. """
        self.talent = Character.TALENTS.index(talent)
        self.player.client.send(
                "<p>{} est doté d'une {} étonnante.".format(
                    self.grammar.il.capitalize(),
                    Character.TALENTS[self.talent])
                )
        self._put()

    def set_remember(self, keyword, string):
        """Remembers/register a character name."""
        keyword = keyword.replace('/', '')
        for character in self.room.characters:
            if character == self.name:
                continue
            if keyword in character.shortdesc:
                self.remember[character.name] = string
                self._put()
                de = apostrophe("de", character.shortdesc[0])
                self.player.client.send(
                    "<p>{} se souviendra {}{} sous le nom «{}».</p>".format(
                        self.name,
                        de,
                        character.shortdesc,
                        string
                    ))
                return
        self.player.client.send("""<p>Le mot clé <i>{}</i> ne correspond
            à personne ici présent.</p>""".format(keyword))

    def get_remember(self, character):
        if character.name == self.name:
            return character.name
        if character.name in self.remember:
            return self.remember[character.name]
        return character.shortdesc

    def list_remember(self):
        table = "<table><tr><th>nom</th><th>description</th></tr>"
        for name in self.remember:
            id_ = self.game.db.get("character:" + name)
            if id_:
                key = "character:" + str(id_)
                data = self.game.db.get(key)
                table += "<tr><td>{}</td><td>{}</td></tr>".format(
                    self.remember[name],
                    data["shortdesc"]
                ) 
        table += "</table>"
        self.player.client.send(table)
