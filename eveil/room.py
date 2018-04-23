from step import Template

from . import world


class Exit():

    def __init__(db, toroom):
        self.toroom = toroom
        self.shortdesc = None
        self.longdesc = None
        self.isopened = True
        self.closable = False
        self.isclosed = False
        self.lockable = False
        self.islocked = False
        self.key = None


class Room():

    def __init__(self):
        world.rooms.append(self)
        # get the index of the room in the list of rooms
        self.id = world.rooms.index(self)
        self.area = None
        self.shortdesc = None
        self.longdesc = None
        self.exits = []
        self.characters = []
        self.things = []

    def addcharacter(self, character):
        self.characters.append(character)

    def delcharacter(self, character):
        self.characters.remove(character)

    def addthing(self, thing):
        self.things.append(obj)

    def delthing(self, thing):
        self.things.remove(obj)

    def addexit(self, exit):
        self.exits.append(exit)

    def lookshort(self, character):
        character.send(self.shortdesc.expand(
            {"character" : character}
            ))

    def looklong(self, character):
        self.lookshort(character)
        character.send(self.longdesc.expand(
            {"character": character}
            ))

    def displayall(self):
        for character in self.game.character:
            if character.room == self:
                self.looklong(character)

    def setshortdesc(self):
        # self.shortdesc = Template("")
        pass

    def setlongdesc(self):
        #self.longdesc = Template("")
        pass
