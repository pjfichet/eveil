#! python

from datetime import datetime

class Player():
    # Initialize an enumeration of states
    CHECKPSEUDO, CREATEPWD, CHECKPWD1, CHECKPWD2, \
        CHECKPWD3, CONFIRMPWD, EMAIL, LOGGED = range(8)

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
        self.state = self.CHECKPSEUDO
        self.send("Indiquez votre pseudonyme:")

    def send(self, text):
        # shortcut to send messages
        self.client.sendMessage(text)

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
            self.send("Indiquez votre mot de passe:")
            self.state = self.CHECKPWD1
        else:
            self.send("Création d'un compte sous le pseudonyme «{}».".format(self.pseudo))
            self.send("Choisissez un mot de passe:")
            self.state = self.CREATEPWD

    def checkpwd(self, data):
        if self.passwd == data:
            if self.characters:
                self.send("Choisissez votre personnage, ou créez-en un nouveau.")
                self.send("Personnages existants: {}.".format(self.characters))
            else:
                self.send("Choisissez le nom de votre personnage:")
            self.login = datetime.now()
            self.state = self.LOGGED
        else:
            if self.state == self.CHECKPWD3:
                self.send("Mot de passe erronné.")
                # todo: kick
            else:
                self.send("Mot de passe erronné. Veuillez ré-essayer:")
                if self.state == self.CHECKPWD2:
                    self.state = self.CHECKPWD3
                else:
                    self.state = self.CHECKPWD2

    def createpwd(self, data):
        self.passwd = data
        self.send("Confirmez votre mot de passe:")
        self.state = self.CONFIRMPWD

    def confirmpwd(self, data):
        if self.passwd == data:
            self.send("Veuillez indiquer une adresse mail \
(les adresses mail ne sont utilisées qu'à votre demande, \
pour vous communiquer un nouveau mot de passe).")
            self.state = self.EMAIL
        else:
            self.send("La confirmation ne correspond pas au mot de passe. Recommencez s'il vous plaît.")
            self.send("Choisissez un mot de passe:")
            self.passwd = None
            self.state = self.CREATEPWD

    def getemail(self, data):
        self.email = data
        self.new()
        self.send("Bravo, votre compte est bien enregistré!")
        self.send("Choisissez le nom de votre personnage:")
        self.state = self.LOGGED

    def parse(self, text):
        if self.state == self.CHECKPSEUDO:
            self.checkpseudo(text)
        elif self.state == self.CREATEPWD:
            self.createpwd(text)
        elif self.state == self.CHECKPWD1 \
            or self.state == self.CHECKPWD2 \
            or self.state == self.CHECKPWD3:
            self.checkpwd(text)
        elif self.state == self.CONFIRMPWD:
            self.confirmpwd(text)
        elif self.state == self.EMAIL:
            self.getemail(text)
        elif self.state == self.LOGGED:
            # should not arrive here
            pass

