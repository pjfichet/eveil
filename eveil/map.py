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
from .message import pose, expose_format, info
from datetime import datetime, timedelta

class Map():
    """The Map class implements a graph: rooms are nodes, and links
    are edges. Rooms and links instances should be created from a Map
    object, using the new_room and new_link methods."""

    def __init__(self, game):
        self.game = game
        self.rooms = []
        self.links = []
        self.linklists = []


    def new_room(self, region, uid):
        room = Room(self.game, region, uid)
        self.rooms.append(room)
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
        # pose_leave and pose_enter define the characters'
        # automated poses when they leave a room and
        # enter another.
        # self.pose_move = None
        # self.pose_leave = None
        # self.pose_enter = None
        self.door = None

    def move(self, character):
        self.leave(character)
        character.queue.add(self.enter, character)

    def leave(self, character):
        pose(character, "/Il se dirige vers {}."
            .format(self.target.shortdesc))

    def enter(self, character):
        pose(character, "/Il quitte les environs en rejoignant {}."
                .format(self.target.shortdesc))
        self.source.del_character(character)
        self.target.send_longdesc(character)
        self.target.add_character(character)
        character.set_room(self.target)
        pose(character, "/Il arrive par ici depuis {}."
                .format(self.source.shortdesc))

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
    NEVER = datetime(2000, 1, 1)
    RPDELTA = timedelta(minutes=15)

    def __init__(self, game, region, uid):
        self.game = game
        self.region = region
        self.uid = region + '_' + uid
        if self.game.db.has('room', self.uid):
            self.data = self.game.db.get('room', self.uid)
            self.container = Container(self.game, self.data['container'])
        else:
            self.data = {
                'container': self.game.db.uid()
            }
            self.container = Container(self.game, self.data['container'])
            self.container.set_volume(10000)
            self.game.db.put('room', self.uid, self.data)
        self.shortdesc = None
        self.longdesc = None
        self.links = []
        self.sources = []
        self.targets = []
        self.characters = []
        self.next_rp = Room.NEVER

    def short(self, text):
        """Sets the short description (title)."""
        self.shortdesc = text

    def long(self, text, dictionary={}):
        """Sets the long description."""
        self.longdesc = Template(
                "<h3>{{room.shortdesc}}</h3>"
                + text
                #+ "<p>{{list_char}}</p>",
                + "<p>{{list_item}}</p><p>{{list_char}}</p>",
                dictionary)

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
        # Give a chance to players to have RP, even if they're not
        # exposing yet.
        if len(self.characters) > 1:
            self.next_rp = datetime.now() + Room.RPDELTA

    def del_character(self, character):
        """Removes a character form the rom."""
        self.characters.remove(character)
        if len(self.characters) < 2:
            # A character alone is not having RP.
            self.next_rp = Room.NEVER

    def send_longdesc(self, character):
        """ Send the long description to a character."""
        list_char = ", ".join(
                [expose_format(char, character, char.data['pose'])
                for char in self.characters])
        if list_char:
            list_char += "."

        list_item = ""
        if self.container.items:
            list_item = ", ".join([item.data['roomdesc']
                                   for item in self.container.items])
            list_item = list_item.capitalize() + "."
        character.player.client.send(self.longdesc.render({
                    "character": character,
                    "room": self,
                    "list_char": list_char,
                    "list_item": list_item,
                }))

    def move(self, character, word):
        """ Move a character to an adjacent room. """
        for link in self.targets:
            if word in link.target.shortdesc:
                link.move(character)
                return
        info(character.player, "Aller où?")

    def rp(self):
        """ Update the RP status of the room."""
        if len(self.characters) > 1:
            self.next_rp = datetime.now() + Room.RPDELTA

    def has_rp(self, now):
        """ Check if the room is RP active."""
        # self.del_character() takes care a lonely character
        # won't have RP.
        return bool(self.next_rp >= now)
