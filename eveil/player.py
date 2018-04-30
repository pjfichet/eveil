#! python

from datetime import datetime
import crypt

from .template import Template
from .character import Character
from .parser import State

account_menu = Template("""
<h2>Éveil</h2>
<h4>Bienvenue, {{player.pseudo}}.</h4>
{%if player.state == State.ACCOUNT %}
    {% if player.characters %}
        {% if player.characters|len > 1 %}
            <p>Vous avez plusieurs personnages: {{player.charlist}}.
            Vous pouvez jouer avec l'un de ces personnages ou en
            créer un nouveau en entrant:
            <ul>
                <li><code>jouer <i>nom_du_personnage</i></code></li>
        {% else %}
            <p>Vous avez créé un personnage: {{player.charlist}}.
            Vous pouvez jouer avec ce personnage ou en créer un nouveau
            en entrant:
            <ul>
                <li><code>jouer <i>{{player.charlist}}</i></code></li>
        {% endif %}
                <li><code>nouveau</code></li>
            </ul>
        </p>
    {% else %}
        <p>Creez un personnage en entrant <code>nouveau</code>.</p>
    {% endif %}
    <p>Vous pouvez aussi modifier ici les données de votre compte avec
    les commandes suivantes:</p>
    <ul>
        <li><code>pseudo: <i>nouveau_pseudonyme</i></code></li>
        <li><code>secret: <i>ancien_mdp nouveau_mdp</i></code></li>
        <li><code>email: <i>mail@exemple.net</i></code></li>
    </ul>
{% endif %}
""", {'len': len})



class Player():
    """ Represent the player. Some information about him is
    recorded in the database, as well as a list of its characters.
    At login, he must provide those informations, and choose
    a character to play.
    """

    # Initialize an enumeration of states
    LOGIN, ACCOUNT, LOGGED = range(3)

    def __init__(self, game, client):
        self.client = client
        self.game = game
        self.id = None
        self.key = None
        self.pseudo = None
        self.password = None
        self.email = None
        self.creation_dt = None
        self.login_dt = None
        self.logout_dt = None
        self.characters = []
        self.state = State.LOGIN

    def _get(self, pseudo):
        """ With the pseudo, extract datas from the db."""
        self.id = self.game.db.get("player:" + pseudo)
        if self.id:
            self.key = "player:" + str(self.id)
            data = self.game.db.get(self.key)
            self.pseudo = data["pseudo"]
            self.password = data["password"]
            self.email = data["email"]
            self.creation_dt = data["creation_dt"]
            self.login_dt = data["login_dt"]
            self.logout_dt = data["logout_dt"]
            self.characters = data["characters"]
            if len(self.characters) == 1:
                self.charlist = self.characters[0]
            else:
                self.charlist = ', '.join(name for name in self.characters)
            return True
        else:
            return False

    def _put(self):
        """ Record the player datas in the database. """
        self.key = "player:" + str(self.id)
        self.game.db.put(
                self.key,
                {"pseudo": self.pseudo, "password": self.password,
                "email": self.email, "creation_dt": self.creation_dt,
                "login_dt": self.login_dt, "logout_dt": self.logout_dt,
                "characters": self.characters
                })

    def _new(self):
        """ Create a new player in the database. """
        self.creation_dt = datetime.now()
        self.login_dt = datetime.now()
        self.id = self.game.db.new("player")
        self.game.db.put("player:" + self.pseudo, self.id)
        self._put()

    def create(self, pseudo, password, confirm, email):
        """ Create an account for a new player. """
        pseudo = pseudo.capitalize()
        if self.game.db.get("player:" + pseudo):
            self.client.send("Le pseudonyme {} est déjà utilisé.".format(pseudo))
            self.client.close()
            return
        if password == confirm:
            password = crypt.crypt(password)
            # Create a new account.
            self.pseudo = pseudo
            self.password = password
            self.email = email
            self._new()
            self.game.log("Player {} created.".format(self.pseudo))
            self.game.players.append(self)
            # Send a short welcome.
            self.client.send(account_menu.render({"player": self, "State": State}))
            # And put the player in chargen.
            self.set_character()
        else:
            self.client.send("Le mot de passe ne correspond pas à sa confirmation.")
            self.client.close()

    def login(self, pseudo, password):
        """ Log in an existing player, checking pseudo and password."""
        pseudo = pseudo.capitalize()
        if self._get(pseudo):
            password = crypt.crypt(password, self.password)
            if self.password == password:
                # Login successful, put the player in the account menu.
                self.game.log("Player {} logs in.".format(self.pseudo))
                self.state = State.ACCOUNT
                self.game.players.append(self)
                self.client.send(account_menu.render(
                    {"player": self, "State": State}
                    ))
            else:
                self.client.send("Mot de passe invalide.")
                self.client.close()
                return
        else:
            self.client.send("Identifiant invalide.")
            self.client.close()

    def logout(self):
        """ Record the player data, and remove the player """
        if self.state == State.CHARGEN:
            self.logout_dt = datetime.now()
            self._put()
        if self in self.game.players:
            self.game.players.remove(self)
        self.game.log("Player {} logs out.".format(self.pseudo))

    def set_pseudo(self, pseudo):
        """ Player command to change his pseudo. """
        pseudo = pseudo.capitalize()
        if self.game.db.get("player:" + pseudo):
            # someone uses that pseudo.
            self.client.send("Le pseudonyme {} est déjà utilisé.".format(self.pseudo))
        else:
            # remove the old player entry.
            self.game.db.rem("player:" + self.pseudo)
            # create a new one
            self.pseudo = pseudo
            self.game.db.put("player:" + self.pseudo, self.id)
            # record the new player data
            self._put()
            self.client.send("<p>Votre pseudonyme est {}.</p>".format(self.pseudo))

    def set_password(self, old, new):
        """ Player command to change his password. """
        old = crypt.crypt(old, self.password)
        new = crypt.crypt(new)
        if self.password != old:
            self.client.send("<p>Le mot de passe entré ne correspond pas au vôtre.</p>")
        else: 
            self.password = new
            self._put()
            self.client.send("<p>Votre nouveau mot de passe est enregistré.</p>")

    def set_email(self, email):
        """ Player command to change his email. """
        self.email = email
        self._put()
        self.client.send("<p>Votre email est {}.</p>".format(self.email))

    def set_character(self, name=None):
        """ Instanciate a character object for the player. """
        self.state = State.CHARGEN
        self.character = Character(self.game, self)
        # check if the player owns a character with that name
        if self.characters and name is not None:
            name = name.capitalize()
            if name in self.characters:
                self.character.name = name
        # in all case, put the character in game:
        self.character.create()

    def record_character(self):
        """ When a character is actually created, this method must
        be called to link the character with the player account.
        """
        self.characters.append(self.character.name)
        self._put()


