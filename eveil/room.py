
class Room():

    def __init__(game):
        self.game = game
        self.id = None
        self.area = None
        self.shortdesc = None
        self.longdesc = None
        self.exits = []

    def display(self):
        for character in self.game.character:
            if character.roomid == self.id:
                character.client.sendMessage(self.shortdesc)
                character.client.sendMessage(self.longdesc)
                for exit in self.exits:
                    character.client.sendMessage(exit)

    def addexit(self):
        pass

