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
from .character import Character, check_character_name
from .parser import State

account_menu = Template("""
<h2>Éveil</h2>
<h3>Bienvenue {{player.data.pseudo}},</h3>
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
            <li><code>créer <i>nom_du_personnage</i></code></li>
        </ul>
    </p>
{% else %}
    <p>Creez un personnage en entrant <code>créer <i>nom_du_personnage</i></code>.</p>
{% endif %}
<p>Vous pouvez aussi modifier ici les données de votre compte avec
les commandes suivantes:</p>
<ul>
    <li><code>pseudo <i>nouveau_pseudonyme</i></code></li>
    <li><code>secret <i>ancien_mdp nouveau_mdp</i></code></li>
    <li><code>email <i>mail@exemple.net</i></code></li>
</ul>
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
        self.data = {
            'pseudo' : None,
            'password' : None,
            'email' : None,
            'creation_dt' : None,
            'login_dt' : None,
            'logout_dt' : None,
            'characters' : [],
            }
        self.state = State.LOGIN

    def get_state(self):
        "Get the player state, which depends on character state."
        if self.character:
            return self.character.data['state']
        return self.state

    def _key(self, pseudo=None):
        "Format the key for the database."
        if pseudo:
            return 'player:' + pseudo
        return 'player:' + self.data['pseudo']

    def _get(self):
        """ With the pseudo, extract datas from the db."""
        self.data = self.game.db.get(self._key())
        if self.data:
            self.charlist = ', '.join(name for name in self.data['characters'])
            return True
        return False

    def _put(self):
        """ Record the player datas in the database. """
        self.game.db.put(self._key(), self.data)

    def create(self, pseudo, password, confirm, email):
        """ Create an account for a new player. """
        # we capitalize the pseudo despite player intention
        # and take care to do it at each login attempt.
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
            self.state = State.ACCOUNT
            self._put()
            self.game.log(
                "Player {} created."
                .format(self.data['pseudo']))
            # Send a short welcome.
            self.client.send(account_menu.render({"player": self, "State": State}))
        else:
            self.client.send("Le mot de passe ne correspond pas à sa confirmation.")
            self.client.close()

    def login(self, pseudo, password):
        """ Log in an existing player, checking pseudo and password."""
        # we take care to capitalize the pseudo.
        self.data['pseudo'] = pseudo.capitalize()
        if self._get():
            password = crypt.crypt(password, self.data['password'])
            if self.data['password'] == password:
                # Login successful, put the player in the account menu.
                self.game.log(
                    "Player {} logs in."
                    .format(self.data['pseudo']))
                self.state = State.ACCOUNT
                # Send a short welcome.
                self.client.send(
                    account_menu.render(
                    {"player": self, "State": State}))
            else:
                self.client.send("Mot de passe invalide.")
                self.client.close()
                return
        else:
            self.client.send("Identifiant invalide.")
            self.client.close()

    def logout(self):
        """ Record the player data, and remove the player """
        if self.character:
            self.character.logout()
            self.character = None
        if self.state > State.LOGIN:
            self.data['logout_dt'] = datetime.now()
            self._put()
            self.game.log("Player {} logs out.".format(self.data['pseudo']))

    def set_pseudo(self, pseudo):
        """ Player command to change his pseudo. """
        # take care to capitalize the pseudo
        pseudo = pseudo.capitalize()
        if self.game.db.get(self._key(pseudo)):
            # someone uses that pseudo.
            self.client.send(
                "Le pseudonyme {} est déjà utilisé."
                .format(self.data['pseudo']))
        else:
            # remove the old player entry.
            oldpseudo = self.data['pseudo']
            self.game.db.rem(self._key())
            # create a new one
            self.data['pseudo'] = pseudo
            # record the new player data
            self._put()
            self.game.log("Player {} renamed {}.".format(
                oldpseudo, self.data['pseudo']))
            self.client.send(
                "<p>Votre pseudonyme est {}.</p>"
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
        self.client.send(
            "<p>Votre email est {}.</p>"
            .format(self.data['email']))

    def create_character(self, name):
        """ creates a new character."""
        name = name.capitalize()
        if not check_character_name(self, name):
            return
        if name in self.data['characters']:
            self.game.log(
                "Vous avez déjà un personnage nommé {}."
                .format(name))
        # the name is valid, use it.
        self.data['characters'].append(name)
        self._put()
        self.character = Character(self.game, self, name)
        self.game.log("Character {} created.".format(self.character.data['name']))

    def play_character(self, name):
        "Plays an existing character."
        name = name.capitalize()
        if name in self.data['characters']:
            self.character = Character(self.game, self, name)
