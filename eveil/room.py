class Exit():

    exits = []

    def __init__(self, game, room_a, room_b, name):
        self.game = game
        self.room_a = room_a
        self.room_b = room_b
        self.name = name
        self.is_opened = True
        self.can_close = False
        self.is_closed = False
        self.can_lock = False
        self.is_locked = False
        self.is_bidirectional = True
        self.key = None

    def get_rooms(self, room):
        # return current room first, other in second
        if room == self.room_a:
            return self.room_a, self.room_b
        else:
            return self.room_b, self.room_a

    def move(self, character):
        from_room, to_room = self.get_rooms(character.room)
        from_room.send(
            "<p>{} s'en va via {}.</p>".format(
            character.name, self.name
            ))
        from_room.characters.remove(character)
        character.room = to_room
        to_room.characters.append(character)
        to_room.send(
            "<p>{} s'en vient via {}.</p>".format(
            character.name, self.name
            ))
        to_room.get_longdesc(character)


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
        # Objects in the room
        self.exits = {}
        self.characters = []
        self.things = []

    def add_character(self, character):
        self.characters.append(character)

    def add_exit(self, room, keyword):
        # Search if a matching exit exists yet
        for exit in Exit.exits:
            if exit.room_a == self:
                if exit.room_b == room:
                    self.exits[keyword] = exit
            elif exit.room_b == self:
                if Exit.room_a == room:
                    self.exits[keyword] = exit
        # If no matching exit is found, create one
        if keyword not in self.exits:
            self.exits[keyword] = Exit(self.game, self, room, keyword)

    def get_shortdesc(self, character):
        character.player.client.send(self.shortdesc.render(
            {"character" : character}
            ))

    def get_longdesc(self, character):
        self.get_shortdesc(character)
        character.player.client.send(self.longdesc.render(
            {"character": character}
            ))

    def send(self, message):
        for character in self.characters:
            character.player.client.send(message)

    def move(self, character, keyword):
        if keyword in self.exits:
            self.exits[keyword].move(character)
        else:
            character.player.client.send(
                "<p><code>Il n'y a pas d'issue nommée {}.</code></p>".format(keyword)
                )

