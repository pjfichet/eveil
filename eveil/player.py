#! python

from datetime import datetime

from .state import ClientState, PlayerState

class Player():
    players = []

    def __init__(self, game, client):
        self.client = client
        self.db = game.db
        self.id = None
        self.key = None
        self.pseudo = None
        self.passwd = None
        self.email = None
        self.creation = None
        self.login = None
        self.logout = None
        self.characters = []
        self.state = PlayerState.checkpseudo
        self.client.sendMessage("Indiquez votre pseudonyme:")

    def setkey(self):
        self.key = "player:" + str(self.id)

    def get(self):
        """ With the pseudo, extract datas from the db."""
        self.id = self.db.get("player:" + self.pseudo)
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
        self.setkey()
        self.db.put(self.key, {"pseudo": self.pseudo, "passwd": self.passwd,
            "email": self.email, "creation": self.creation,
            "login": self.login, "logout": self.logout,
            "characters": self.characters })

    def new(self):
        self.creation = datetime.now()
        self.login = datetime.now()
        self.id = self.db.new("player")
        self.db.put("player:" + self.pseudo, self.id)
        self.put()

    def checkpseudo(self, text):
        self.pseudo = text
        if self.get():
            self.client.sendMessage("Indiquez votre mot de passe:")
            self.state = PlayerState.checkpwd1
        else:
            self.client.sendMessage("Création d'un compte sous le pseudonyme «{}».".format(self.pseudo))
            self.client.sendMessage("Choisissez un mot de passe:")
            self.state = PlayerState.createpwd

    def checkpwd(self, data):
        if self.passwd == data:
            if self.characters:
                self.client.sendMessage("Choisissez votre personnage, ou créez-en un nouveau.")
                self.client.sendMessage("Personnages existants: {}.".format(self.characters))
            else:
                self.client.sendMessage("Choisissez le nom de votre personnage:")
            self.login = datetime.now()
            self.state = PlayerState.logged
            self.client.setState(ClientState.chargen)
        else:
            if self.state == PlayerState.checkpwd3:
                self.client.sendMessage("Mot de passe erronné.")
                # todo: kick
            else:
                self.client.sendMessage("Mot de passe erronné. Veuillez ré-essayer:")
                if self.state == PlayerState.checkpwd2:
                    self.state = PlayerState.checkpwd3
                else:
                    self.state = PlayerState.checkpwd2

    def createpwd(self, data):
        self.passwd = data
        self.client.sendMessage("Confirmez votre mot de passe:")
        self.state = PlayerState.confirmpwd

    def confirmpwd(self, data):
        if self.passwd == data:
            self.client.sendMessage("Veuillez indiquer une adresse mail \
(les adresses mail ne sont utilisées qu'à votre demande, \
pour vous communiquer un nouveau mot de passe).")
            self.state = PlayerState.email
        else:
            self.client.sendMessage("La confirmation ne correspond pas au mot de passe. Recommencez s'il vous plaît.")
            self.client.sendMessage("Choisissez un mot de passe:")
            self.passwd = None
            self.state = PlayerState.createpwd

    def getemail(self, data):
        self.email = data
        self.new()
        self.client.sendMessage("Bravo, votre compte est bien enregistré!")
        self.client.sendMessage("Choisissez le nom de votre personnage:")
        self.state = PlayerState.logged
        self.client.setState(ClientState.chargen)

    def parse(self, text):
        if self.state == PlayerState.checkpseudo:
            self.checkpseudo(text)
        elif self.state == PlayerState.createpwd:
            self.createpwd(text)
        elif self.state == PlayerState.checkpwd1 \
            or self.state == PlayerState.checkpwd2 \
            or self.state == PlayerState.checkpwd3:
            self.checkpwd(text)
        elif self.state == PlayerState.confirmpwd:
            self.confirmpwd(text)
        elif self.state == PlayerState.email:
            self.getemail(text)
        elif self.state == PlayerState.logged:
            # should not arrive here
            pass




