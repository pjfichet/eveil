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


# This submodule implements a directed graph.
# The path algorithm comes from: https://www.python.org/doc/essays/graphs/
# Some other ideas come from:
# https://triangleinequality.wordpress.com/2013/08/21/graphs-as-objects-in-python/

from .template import Template
from .item import Container

class Map():
    """The Map class implements a graph: rooms are nodes, and links
    are edges. Rooms and links instances should be created from a Map
    object, using the new_room and new_link methods."""

    def __init__(self, game):
        self.game = game
        self.rooms = []
        self.links = []
        self.linklists = []

    def new_room(self):
        room = Room(self.game)
        self.rooms.append(room)
        room.id = self.rooms.index(room)
        return room

    def new_link(self, source, target):
        # First, our link is a simple list
        link =  [source, target]
        if link in self.linklists:
            self.game.log("There is yet a link from room {} to room {}."
                .format(source.shortdesc, target.shortdesc)
                )
            return
        self.linklists.append(link)
        # Now, we create a true Link instance
        link = Link(source, target)
        self.links.append(link)
        source.add_link(link)
        return link
 
    def path(self, source, target, path=[]):
        """ Returns the shortest path from source to target.
        Comes from: https://www.python.org/doc/essays/graphs/
        """
        path = path + [source]
        if source == target:
            return path
        if source not in self.rooms:
            return None
        shortest = None
        for room in source.get_targets():
            if room not in path:
                newpath = self.path(room, target, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                            shortest = newpath
        return shortest


class Link():
    """ An unidirectional link between two rooms."""
    def __init__(self, source, target):
        self.rooms = [source, target]
        self.source = source
        self.target = target
        # dynadesc: a multi-purpose short description
        # of the form: by climbing up the ridge.
        # used as follow:
        # - by $dynadesc, /n can go to $room.
        # - /n leaves toward $room by $dynadesc.
        # - $dynadesc, /n arrives from.
        self.dynadesc = None # "en montant le chemin"
        self.door = None

    def move(self, character):
        self.source.characters.remove(character)
        self.source.send_all("<p>En {}, {} s'en va vers {}.</p>"
                .format(self.dynadesc, character.name,
                    self.target.shortdesc)
                )
        self.target.send_all("<p>En {}, {} arrive depuis {}.</p>"
                .format(self.dynadesc, character.name,
                    self.source.shortdesc)
                )
        character.player.client.send(
                "<p>En {}, {} quitte {} pour rejoindre {}.</p>"
                .format(self.dynadesc, character.name,
                    self.source.shortdesc, self.target.shortdesc)
                )
        character.room = self.target
        self.target.characters.append(character)
        self.target.send_longdesc(character)


class Door():
    """A door."""
    def __init__(self):
        self.is_opened = True
        self.can_close = False
        self.is_closed = False
        self.can_lock = False
        self.is_locked = False
        self.key = None


class Room():
    top_template = Template(
    """<h3>{{room.shortdesc|capitalize}}</h3>""",
    {'capitalize': str.capitalize}
    )

    bottom_template = Template(
"""<ul>
{% for item in room.container.items %}
    <li>{{item.roomdesc}}</li>
{% endfor %}
</ul>
<p>
{% for link in room.targets %}
    En {{link.dynadesc}}, {{character.name}} peut rejoindre {{link.target.shortdesc}}.
{% endfor %}
</p>""")

    def __init__(self, game):
        self.game = game
        self.id = None
        self.shortdesc = None
        self.longdesc = None
        self.links = []
        self.sources = []
        self.targets = []
        self.characters = []
        self.container = Container(self.game)
        self.container.max_volume = 10000

    def add_link(self, link):
        if self in link.rooms and link not in self.links:
            self.links.append(link)
            if link.source == self:
                self.targets.append(link)
            else:
                self.sources.append(link)
    
    def get_sources(self):
        """ Return the list of rooms from which one can come here."""
        return [link.source for link in self.links]

    def get_targets(self):
        """ Return the list of rooms one can go from here."""
        return [link.target for link in self.targets]

    def get_target_link(self, target):
        """ Return the link leading to the target room."""
        for link in self.targets:
            if link.target == target:
                return link

    def get_source_link(self, source):
        """ Return the link by which one can come from source room."""
        for link in self.sources:
            if link.source == source:
                return link

    def add_character(self, character):
        """ add a character to the room."""
        self.characters.append(character)

    def send_longdesc(self, character):
        """ Send the long description to a character."""
        character.player.client.send(Room.top_template.render({
                "room": self,
                }))
        character.player.client.send(self.longdesc.render({
                    "character": character,
                    "room": self,
                }))            
        character.player.client.send(Room.bottom_template.render({
                    "character": character,
                    "room": self,
                }))

    def send_all(self, message):
        """ Send a message to all characters in the room. """
        for character in self.characters:
            character.player.client.send(message)

    def move(self, character, word):
        """ Move a character to an adjacent room. """
        for link in self.targets:
            if word in link.target.shortdesc:
                link.move(character)
                return
        character.player.client.send("<p><code>Aller où?</code></p>")

