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

class Remember():
    """Characters don't know each others names. They have to share
    them and remember them. This system allow them to remember names."""

    def __init__(self, game, character):
        self.game = game
        self.name = character.data['name']
        self.character = character
        self.key = "remember:" + self.name
        self.remember = {}
        if self.game.db.has(self.key):
            self._get()
        else:
            self._put()

    def _put(self):
        self.game.db.put(self.key, self.remember)

    def _get(self):
        self.remember = self.game.db.get(self.key)

    def set_remember(self, keyword, string):
        """Remembers/registers a character name."""
        keyword = keyword.replace('/', '')
        for character in self.character.room.characters:
            if character == self.character.data['name']:
                continue
            if keyword in character.data['shortdesc']:
                self.remember[character.data['name']] = string
                self._put()
                de = apostrophe("de", character.data['shortdesc'][0])
                self.character.player.client.send(
                    "<p>{} se souviendra {}{} sous le nom «{}».</p>".format(
                        self.name,
                        de,
                        character.data['shortdesc'],
                        string
                    ))
                return
        self.character.player.client.send("""<p>Le mot clé <i>{}</i> ne correspond
            à personne ici présent.</p>""".format(keyword))

    def get_remember(self, character):
        if self.character.data['name'] == self.name:
            return character.data['name']
        if character.data['name'] in self.remember:
            return self.remember[character.data['name']]
        return character.data['shortdesc']

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

    def rename(self, name):
        "after renaming a character, reset the database entry."
        oldname = self.name
        self.game.db.rem(self.key)
        self.name = name
        self.key = "remember:" + name
        self._put()
        self.game.log(
            "Remember {} renamed {}."
            .format(oldname, self.data['name']))
