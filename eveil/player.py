# Copyright (C) 2018 Pierre Jean Fichet
# <pierrejean dot fichet at posteo dot net>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from datetime import datetime
import crypt

from .template import Template
from .character import Character
from .parser import State

account_menu = Template("""
<h2>Éveil</h2>
<h3>Bienvenue {{player.data.pseudo}},</h3>
{%if player.state == State.ACCOUNT %}
    {% if player.data.characters %}
        {% if player.data.characters|len > 1 %}
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
        <li><code>pseudo <i>nouveau_pseudonyme</i></code></li>
        <li><code>secret <i>ancien_mdp nouveau_mdp</i></code></li>
        <li><code>email <i>mail@exemple.net</i></code></li>
    </ul>
{% endif %}
""", {'len': len})



class Player():
    """ Represent the player. Some information about him is
    recorded in the database, as well as a list of its characters.
    At login, he must provide these informations, and choose
    a character to play.
    """

    def __init__(self, game, client):
        self.client = client
        self.game = game
        self.character = None
        self.charlist = ""
        self.data = {'pseudo' : None,
            'password' : None,
            'email' : None,
            'creation_dt' : None,
            'login_dt' : None,
            'logout_dt' : None,
            'characters' : [],
            }
        self.state = State.LOGIN

    def _key(self, pseudo = None):
        if pseudo:
            return 'player:' + pseudo
        else:
            return 'player:' + self.data['pseudo']

    def _get(self):
        """ With the pseudo, extract datas from the db."""
        self.data = self.game.db.get(self._key())
        if self.data:
            self.charlist = ', '.join(name for name in self.data['characters'])
            return True
        else:
            return False

    def _put(self):
        """ Record the player datas in the database. """
        self.game.db.put(self._key(), self.data)

    def create(self, pseudo, password, confirm, email):
        """ Create an account for a new player. """
        pseudo = pseudo.capitalize()
        if self.game.db.get(self._key(pseudo)):
            self.client.send("Le pseudonyme {} est déjà utilisé.".format(pseudo))
            self.client.close()
            return
        if password == confirm:
            password = crypt.crypt(password)
            # Create a new account.
            self.data['pseudo'] = pseudo
            self.data['password'] = password
            self.data['email'] = email
            self.data['creation_dt'] = datetime.now()
            self.data['login_dt'] = datetime.now()
            self._put()
            self.game.log("Player {} created."
                .format(self.data['pseudo']))
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
        self.data['pseudo'] = pseudo.capitalize()
        if self._get():
            password = crypt.crypt(password, self.data['password'])
            if self.data['password'] == password:
                # Login successful, put the player in the account menu.
                self.game.log("Player {} logs in."
                    .format(self.data['pseudo']))
                self.state = State.ACCOUNT
                self.game.players.append(self)
            else:
                self.client.send("Mot de passe invalide.")
                self.client.close()
                return
        else:
            self.client.send("Identifiant invalide.")
            self.client.close()

    def logout(self):
        """ Record the player data, and remove the player """
        if self.state >= State.LOGIN:
            self.data['logout_dt'] = datetime.now()
            self._put()
        if self in self.game.players:
            self.game.players.remove(self)
        if self.character:
            self.character.logout()
        self.game.log("Player {} logs out.".format(self.data['pseudo']))

    def set_pseudo(self, pseudo):
        """ Player command to change his pseudo. """
        pseudo = pseudo.capitalize()
        if self.game.db.get(self._key(pseudo)):
            # someone uses that pseudo.
            self.client.send("Le pseudonyme {} est déjà utilisé."
                .format(self.data['pseudo']))
        else:
            # remove the old player entry.
            self.game.db.rem(self._key())
            # create a new one
            self.data['pseudo'] = pseudo
            # record the new player data
            self._put()
            self.client.send("<p>Votre pseudonyme est {}.</p>"
                .format(self.data['pseudo']))

    def set_password(self, old, new):
        """ Player command to change his password. """
        old = crypt.crypt(old, self.data['password'])
        new = crypt.crypt(new)
        if self.data['password'] != old:
            self.client.send("<p>Le mot de passe entré ne correspond pas au vôtre.</p>")
        else: 
            self.data['password'] = new
            self._put()
            self.client.send("<p>Votre nouveau mot de passe est enregistré.</p>")

    def set_email(self, email):
        """ Player command to change his email. """
        self.data['email'] = email
        self._put()
        self.client.send("<p>Votre email est {}.</p>"
            .format(self.data['email']))

    def set_character(self, name=None):
        """ Instanciate a character object for the player. """
        self.state = State.CHARGEN
        self.character = Character(self.game, self)
        # check if the player owns a character with that name
        if self.data['characters'] and name is not None:
            name = name.capitalize()
            if name in self.data['characters']:
                self.character.name = name
        # in all case, put the character in game:
        self.character.create()

    def record_character(self):
        """ When a character is actually created, this method must
        be called to link the character with the player account.
        """
        if self.character.name not in self.data['characters']:
            self.data['characters'].append(self.character.name)
            self._put()


