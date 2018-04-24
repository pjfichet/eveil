#! python

from datetime import datetime
from step import Template

from .character import Character
from .utils import log
from . import world

account_menu = Template("""
<h2>Éveil</h2>
%if player.state != Player.ACCOUNT:
<p>Bienvenue, {{player.pseudo}}.</p>
%else:
<h3>Bienvenue {{player.pseudo}}</h3>
    %if player.characters:
        <p>Choisissez votre personnage ou creez-en un nouveau en entrant
        <code>nouveau</code>.
        %if len(player.characters) > 1:
            Vos personnages sont: {{player.charlist}}.
        %else:
            Votre personnage est {{player.character[0]}}.
        %endif
        </p>
    %else:
        <p>Creez un personnage en entrant <code>nouveau</code>.</p>
    %endif
    <p>Vous pouvez aussi modifier ici les données de votre compte avec
    les commandes suivantes:</p>
    <ul>
        <li><code>pseudo: <i>nouveau_pseudonyme</i></code></li>
        <li><code>secret: <i>ancien_mdp nouveau_mdp</i></code></li>
        <li><code>email: <i>mail@exemple.net</i></code></li>
    </ul>
%endif
""")



class Player():
    """ Represent the player. Some information about him is
    recorded in the database, as well as a list of its characters.
    At login, he must provide those informations, and choose
    a character to play."""

    # Initialize an enumeration of states
    LOGIN, ACCOUNT, LOGGED = range(3)

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
        """ A shortcut to send message to the player's client."""
        self.client.sendMessage("<div>" + text + "</div>")

    def setkey(self):
        """ Set the key used to fetch the player datas in the database."""
        self.key = "player:" + str(self.id)

    def setcharlist(self):
        """ Format a human readable list of characters """
        self.charlist = ', '.join(name for name in self.characters)

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
            self.setcharlist()
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

    def dologin(self, pseudo, passwd):
        """ Log in an existing player, checking pseudo and password."""
        if self.get(pseudo):
            if self.passwd == passwd:
                # Login successful, put the player in the account menu.
                log("Player {} logs in.".format(self.pseudo))
                self.state = Player.ACCOUNT
                world.players.append(self)
                self.send(account_menu.expand({"player": self, "Player": Player}))
                return
        # Log out everyone else
        self.client.close()

    def docreate(self, pseudo, passwd, confirm, mail):
        """ Create an account for a new player. """
        if self.db.get("player:" + pseudo):
            # A player with that name exists, try to log him in.
            self.dologin(pseudo, passwd)
            return
        if passwd == confirm:
            # Create a new account.
            self.pseudo = pseudo
            self.passwd = passwd
            self.mail = mail
            self.new()
            log("Player {} created.".format(self.pseudo))
            world.players.append(self)
            # Send a short welcome.
            self.send(account_menu.expand({"player": self, "Player": Player}))
            # And put the player in chargen.
            self.setcharacter()
            return
        # Log out everyone else
        self.client.close()

    def setcharacter(self, text=None):
        """ Instanciate a character object for the player. """
        self.character = Character(self.db, self)
        self.state = self.LOGGED
        self.character.checkname(text)

    def setpseudo(self, text):
        """ player command to change his pseudo. """
        if self.db.get("player:" + text):
            # someone uses that pseudo.
            self.send("Le pseudonyme {} est déjà utilisé.".format(self.pseudo))
            return
        # remove the old player entry.
        self.db.rem("player:" + self.pseudo)
        # create a new one
        self.pseudo = text
        self.db.put("player:" + self.pseudo, self.id)
        # record the new player data
        self.put()
        self.send("<p>Votre pseudonyme est {}.</p>".format(self.pseudo))

    def setpassword(self, old, new):
        """ Player command to change his password. """
        if self.passwd != old:
            self.send("<p>Le mot de passe entré ne correspond pas au votre.</p>")
            return
        self.passwd = new
        self.put()
        self.send("<p>Votre nouveau mot de passe est enregistré.</p>")

    def setemail(self, text):
        """ Player command to change his email. """
        self.email = text
        self.put()
        self.send("<p>Votre email est {}.</p>".format(self.email))

    def addcharacter(self):
        """ When a character is created, this method must be called
        to link the character with the player account. """
        self.characters.append(self.character.name)
        self.put()

    def log_out(self):
        """ Record the player data, and remove the player """
        if self.state == self.LOGGED:
            self.logout = datetime.now()
            self.put()
        world.players.remove(self)
        log("Player {} logs out.".format(self.pseudo))

    def parse(self, text):
        """ Parse the datas on login and the account commands. """
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
        elif self.state == Player.ACCOUNT:
            self.setcharacter(text)
        else:
            # we should not arrive here
            pass


