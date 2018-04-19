
class Character():

    def __init__(self, db, player):
        self.db = db
        self.player = player
        self.id = None
        self.key = None
        self.name = None
        self.lastname = None
        self.gender = None
        self.room = None
        self.longdesc = None
        self.shortdesc = None
        self.stats = []

    def setkey(self):
        self.key = "character:" + str(self.id)

    def get(self):
        """ With the character name, extract datas from the db."""
        self.id = self.db.get("character:" + self.name)
        if self.id:
            self.setkey()
            data = self.db.get(self.key)
            self.lastname = data["lastname"]
            self.gender = data["gender"]
            self.room = data["room"]
            self.longdesc = data["longdesc"]
            self.shortdesc = data["shortdesc"]
            self.stats = data["stats"]
            return True
        else:
            return  False

    def put(self):
        self.setkey()
        self.db.put(self.key, {"name": self.name, "lastname": self.lastname,
            "gender": self.gender, "room": self.room, 
            "longdesc": self.longdesc, "shortdesc": self.shortdesc,
            "stats": self.stats, "state": self.state })

    def new(self):
        self.id = self.db.new("character")
        self.room = "chargen01"
        self.state = CharacterState.chargen
        self.db.put("character:" + self.name, self.id)
        self.put()

    def checkname(self, text):
        if self.player.characters:
            if text in self.player.characters:
                self.name = text
                self.get()
        self.entergame()

    def entergame(self):
        #todo: enter the game
        pass



