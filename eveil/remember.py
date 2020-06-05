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

from .grammar import apostrophe
from .message import info

class Remember():
    """Characters don't know each others names. They have to share
    them and remember them. This system allow them to remember names."""

    def __init__(self, game, character):
        self.game = game
        self.character = character
        self.uid = self.character.data['uid']
        if self.game.db.has('remember', self.uid):
            self.data = self.game.db.get('remember', self.uid)
        else:
            self.data = {}
            self.game.db.put('remember', self.uid, self.data)

    def set_remember(self, keyword, string):
        """Remembers/registers a character name."""
        keyword = keyword.replace('/', '')
        keyword = keyword.lower()
        for character in self.character.room.characters:
            if character == self.character:
                continue
            if keyword in self.get_remember(character).lower():
                # Since we remember characters by their name,
                # when they change name the information becomes
                # useless. That's a design choice: characters changing
                # name should'nt be remembered.
                self.data[character.data['name']] = string
                self.game.db.put('remember', self.uid, self.data)
                article = apostrophe("de", character.data['shortdesc'][0])
                info(self.character.player,
                    "{} se souviendra {}{} sous le nom de « {} ».".format(
                        self.character.data['name'],
                        article,
                        character.data['shortdesc'],
                        string
                    ))
                return
        info(self.character.player,
            "<p>Le mot clé <i>{}</i> ne correspond à personne ici présent.</p>"
            .format(keyword))

    def get_remember(self, character):
        "Get the string by which a character is remembered."
        if character.data['name'] == self.character.data['name']:
            return character.data['name']
        if character.data['name'] in self.data:
            return self.data[character.data['name']]
        return character.data['shortdesc']

    def list_remember(self):
        "List the remembered names and strings."
        table = "<table><tr><th>nom</th><th>description</th></tr>"
        for name in self.data:
            data = self.game.db.get("character:" + name)
            if data:
                table += "<tr><td>{}</td><td>{}</td></tr>".format(
                    self.data[name],
                    data["shortdesc"]
                )
        table += "</table>"
        info(self.character.player, table)

