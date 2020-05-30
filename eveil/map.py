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
from .expose import expose_all

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

        expose_all(character, "En {}, /{} se dirige vers {}."
                .format(self.dynadesc, character.name,
                    self.target.shortdesc)
                )
        character.queue.add(self.leave, character)

    def leave(self, character):
        expose_all(character, "/{} quitte {} pour rejoindre {}."
                .format(character.name,
                    self.source.shortdesc, self.target.shortdesc)
                )
        self.source.characters.remove(character)
        self.target.characters.append(character)
        character.room = self.target
        self.target.send_longdesc(character)
        expose_all(character, "En {}, /{} arrive depuis {}."
                .format(self.dynadesc, character.name,
                    self.source.shortdesc)
                )

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
"""<p>
{% for link in room.targets %}
    En {{link.dynadesc}}, {{character.name}} peut rejoindre {{link.target.shortdesc}}.
{% endfor %}
</p>
<p>{{list_char}} {{list_item}}</p>
""")

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
        list_item = "" 
        if self.container.items:
            list_item = "Il y a aussi "
            for i, item in self.container.items:
                if i:
                    list_item += ", " + item.roomdesc
                else:
                    list_item = item.roomdesc.capitalize()
            list_item += "."
        list_char = ""
        if self.characters:
            i = 0
            for char in self.characters:
                name = character.get_remember(char)
                if i:
                    list_char += ", " + name + " " + char.action
                else:
                    list_char = name + " " + char.action
                    i = 1
            list_char += "."
        character.player.client.send(Room.bottom_template.render({
                    "character": character,
                    "room": self,
                    "list_item": list_item,
                    "list_char": list_char,
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

