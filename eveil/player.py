#! python

from datetime import datetime

from .character import Character
from .utils import log
from . import world



class Player():
    """ Represent the player. Some information about him is
    recorded in the database, as well as a list of its characters.
    At login, he must provide those informations, and choose
    a character to play."""

    # Initialize an enumeration of states
    LOGIN, CHARACTER, LOGGED = range(3)

    def __init__(self, db, client):
        self.client = client
        self.db = db
        self.id = None
        self.key = None
        self.pseudo = None
        self.passwd = None
        self.email = None
        self.creation = None
        self.login = None
        self.logout = None
        self.characters = []
        self.state = self.LOGIN

    def send(self, text):
        # shortcut to send messages
        self.client.sendMessage("<div>" + text + "</div>")

    def setkey(self):
        self.key = "player:" + str(self.id)

    def get(self, pseudo):
        """ With the pseudo, extract datas from the db."""
        self.id = self.db.get("player:" + pseudo)
        if self.id:
            self.setkey()
            data = self.db.get(self.key)
            self.pseudo = data["pseudo"]
            self.passwd = data["passwd"]
            self.email = data["email"]
            self.creation = data["creation"]
            self.login = data["login"]
            self.logout = data["logout"]
            self.characters = data["characters"]
            return True
        else:
            return False

    def put(self):
        """ Record the player datas in the database. """
        self.setkey()
        self.db.put(self.key, {"pseudo": self.pseudo, "passwd": self.passwd,
            "email": self.email, "creation": self.creation,
            "login": self.login, "logout": self.logout,
            "characters": self.characters })

    def new(self):
        """ Create a new character in the database. """
        self.creation = datetime.now()
        self.login = datetime.now()
        self.id = self.db.new("player")
        self.db.put("player:" + self.pseudo, self.id)
        self.put()

    def parse(self, text):
        words = text.split()
        if self.state == Player.LOGIN:
            if len(words) == 2:
                self.dologin(words[0], words[1])
                return
            if len(words) == 4:
                self.docreate(words[0], words[1], words[2], words[3])
                return
            # Log out everyone else
            self.client.close()
        elif self.state == Player.CHARACTER:
            self.setcharacter(text)
        else:
            # we should not arrive here
            pass

    def dologin(self, pseudo, passwd):
        """ Log in an existing player, checking pseudo and password."""
        if self.get(pseudo):
            if self.passwd == passwd:
                log("Player {} logs in.".format(self.pseudo))
                self.welcome()
                if self.characters:
                    self.send("<p>Choisissez votre personnage, ou creez-en un nouveau en appuyant sur «Entrée».</p>")
                else:
                    self.send("<p>Appuyez sur «Entrée» pour creer un personnage.</p>")
                return
        # Log out everyone else
        self.client.close()

    def docreate(self, pseudo, passwd, confirm, mail):
        """ Create an account for a new player. """
        if self.db.get("player:" + pseudo):
            self.dologin(pseudo, passwd)
            return
        if passwd == confirm:
            self.pseudo = pseudo
            self.passwd = passwd
            self.mail = mail
            self.new()
            log("Player {} created.".format(self.pseudo))
            self.welcome()
            self.send("<p>Votre compte est maintenant créé.</p>")
            return
        # Log out everyone else
        self.client.close()

    def welcome(self):
        self.send("<h2>Éveil</h2>")
        self.send("<p>Bienvenue {}!</p>".format(self.pseudo))
        self.state = Player.CHARACTER
        world.players.append(self)

    def setcharacter(self, text):
        self.character = Character(self.db, self)
        self.state = self.LOGGED
        self.character.checkname(text)

    def logout(self):
        """ Record the player data, and remove the player """
        if self.state == self.LOGGED:
            self.logout = datetime.now()
            self.put()
        world.players.remove(self)
        log("Player {} logs out.".format(self.pseudo))
