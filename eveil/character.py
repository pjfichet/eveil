from .utils import log
from . import world


class Character():
    MALE, FEMALE = range(2)

    def __init__(self, db, player):
        self.db = db
        self.player = player
        self.id = None
        self.key = None
        self.name = None
        self.lastname = None
        self.gender = None
        self.room = world.rooms[0]
        self.rommid = self.room.id
        self.longdesc = None
        self.shortdesc = None
        self.skill = None
        self.talent = None

    def send(self, text):
        self.player.send(text)

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
            self.roomid = data["roomid"]
            self.longdesc = data["longdesc"]
            self.shortdesc = data["shortdesc"]
            self.skill = data["skill"]
            self.talent = data["talent"]
            return True
        else:
            return  False

    def put(self):
        """ Record the datas of the character in the db."""
        self.setkey()
        self.db.put(self.key, {"name": self.name, "lastname": self.lastname,
            "gender": self.gender, "roomid": self.room.id, 
            "longdesc": self.longdesc, "shortdesc": self.shortdesc,
            "skill": self.skill, "talent": self.talent })

    def new(self):
        """ Create a new character, record it in the db."""
        self.id = self.db.new("character")
        self.db.put("character:" + self.name, self.id)
        self.put()
        self.player.addcharacter()

    def checkname(self, text):
        """ Check if a given name match with a character name,
        and if the player owns that character. In all case,
        put the player in game, be it in chargen."""
        if self.player.characters and text is not None:
            if text in self.player.characters:
                self.name = text
                self.get()
                world.characters.append(self)
                log("Character {} enters the game in room {}.".format(self.name, self.room.id))
        # put the character in game.
        self.room.addcharacter(self)
        self.room.looklong(self)

    def cmd_gender(self, text):
        """ Define the gender of the character """
        if text == "homme":
            self.gender = Character.MALE
            self.send("<p>Il sera un homme.</p>")
        elif text == "femme":
            self.gender = Character.FEMALE
            self.send("<p>Elle sera une femme.</p>")
        else:
            self.send("<p>genre: [homme|femme]</p>")

    def cmd_name(self, text):
        """ Define the name of the character. This is also
        when the character is actually recorded in the database."""
        self.name = text
        if self.gender == Character.FEMALE:
            self.send("<p>Elle se nomme {}.</p>".format(self.name))
        else:
            self.send("<p>Il se nomme {}.</p>".format(self.name))
        self.new()
        log("Character {} created.".format(self.name))

    def cmd_shortdesc(self, text):
        """ Define the short description of the character."""
        self.shortdesc = text
        self.send("</p>Apparence enregistrée.</p>")
        self.put()

    def cmd_longdesc(self, text):
        """ Define the long description of the character."""
        self.longdesc = text
        self.send("<p>Description enregistrée.</p>")
        self.put()

    def cmd_skill(self, text):
        """ Define the skill of the character. """
        if text in Character.SKILLS:
            self.skill = text
            self.put()
        else:
            self.send("<code>métier: <i>artisan|chasseur|druide|guerrier|barde</i></code>")

    def cmd_talent(self, text):
        """ Define the talent of the character. """
        if text in Character.TALENTS:
            self.talent = Character.TALENTS
            self.put()
        else:
            self.send("talent: <i>sagesse|intelligence|constitution|force|agileté</i></code>")
