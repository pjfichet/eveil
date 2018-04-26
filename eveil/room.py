from step import Template

class Exit():

    def __init__(db, toroom):
        self.toroom = toroom
        self.shortdesc = None
        self.longdesc = None
        self.is_opened = True
        self.can_close = False
        self.is_closed = False
        self.can_lock = False
        self.is_locked = False
        self.key = None


class Room():

    def __init__(self, game):
        self.game = game
        self.game.rooms.append(self)
        # get the index of the room in the list of rooms
        self.id = self.game.rooms.index(self)
        self.area = None
        # short and long description must be a Template instance.
        self.shortdesc = None
        self.longdesc = None
        self.exits = []
        self.characters = []
        self.things = []

    def add_character(self, character):
        self.characters.append(character)

    def del_character(self, character):
        self.characters.remove(character)

    def add_thing(self, thing):
        self.things.append(thing)

    def del_thing(self, thing):
        self.things.remove(thing)

    def add_exit(self, exit):
        self.exits.append(exit)

    def get_shortdesc(self, character):
        character.player.client.send(self.shortdesc.expand(
            {"character" : character}
            ))

    def get_longdesc(self, character):
        self.get_shortdesc(character)
        character.player.client.send(self.longdesc.expand(
            {"character": character}
            ))


