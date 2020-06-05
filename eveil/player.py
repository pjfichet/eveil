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
from .message import error, info

account_menu = Template("""
<h2>Éveil</h2>
<h4>Bienvenue {{player.data.pseudo}},</h4>
{% if player.data.characters %}
    {% if player.data.characters|len > 1 %}
        <p>Vous avez plusieurs personnages : {{player.charlist}}.
        Vous pouvez jouer avec l'un de ces personnages ou en
        créer un nouveau en entrant :
        <ul>
            <li><code>jouer <i>nom_du_personnage</i></code></li>
    {% else %}
        <p>Vous avez créé un personnage : {{player.charlist}}.
        Vous pouvez jouer avec ce personnage ou en créer un nouveau
        en entrant :
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
les commandes suivantes :</p>
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
        self.uid = None
        self.character = None
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

    def charlist(self):
        """Returns a formatted list of characters."""
        return ', '.join(name for name in self.data['characters'])

    def create(self, pseudo, password, confirm, email):
        """ Create an account for a new player. """
        # we capitalize the pseudo despite player intention
        # and take care to do it at each login attempt.
        pseudo = pseudo.capitalize()
        if self.game.db.has('player', pseudo):
            error(self, "Le pseudonyme {} est déjà utilisé.".format(pseudo))
            self.client.close()
            return
        if password == confirm:
            password = crypt.crypt(password)
            # Create a new account.
            self.data['uid'] = self.game.db.uid()
            self.data['pseudo'] = pseudo
            self.data['password'] = password
            self.data['email'] = email
            self.data['creation_dt'] = datetime.now()
            self.data['login_dt'] = datetime.now()
            self.state = State.ACCOUNT
            self.game.db.put('player', self.data['pseudo'], self.data)
            self.game.log(
                "Player {} created."
                .format(self.data['pseudo']))
            # Send a short welcome.
            self.client.send(account_menu.render({"player": self, "State": State}))
        else:
            error(self, "Le mot de passe ne correspond pas à sa confirmation.")
            self.client.close()

    def login(self, pseudo, password):
        """ Log in an existing player, checking pseudo and password."""
        # we take care to capitalize the pseudo.
        pseudo = pseudo.capitalize()
        if not self.game.db.has('player', pseudo):
            error(self, "Identifiant invalide.")
            self.client.close()
            return
        self.data = self.game.db.get('player', pseudo)
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
            error(self, "Mot de passe invalide.")
            self.client.close()

    def logout(self):
        """ Record the player data, and remove the player """
        if self.character:
            self.character.logout()
            self.character = None
        if self.state > State.LOGIN:
            self.data['logout_dt'] = datetime.now()
            self.game.db.put('player', self.data['pseudo'], self.data)
            self.game.log("Player {} logs out.".format(self.data['pseudo']))

    def set_pseudo(self, pseudo):
        """ Player command to change his pseudo. """
        # take care to capitalize the pseudo
        pseudo = pseudo.capitalize()
        if self.game.db.has('player', pseudo):
            # someone uses that pseudo.
            info(self,
                "Le pseudonyme {} est déjà utilisé."
                .format(self.data['pseudo']))
        else:
            # rename the database entry.
            oldpseudo = self.data['pseudo']
            self.game.db.rem('player', oldpseudo)
            self.data['pseudo'] = pseudo
            self.game.db.put('player', self.data['pseudo'], self.data)
            self.game.log("Player {} renamed {}.".format(
                oldpseudo, self.data['pseudo']))
            info(self,
                "Votre pseudonyme est {}."
                .format(self.data['pseudo']))

    def set_password(self, old, new):
        """ Player command to change his password. """
        old = crypt.crypt(old, self.data['password'])
        new = crypt.crypt(new)
        if self.data['password'] != old:
            info(self,
                "Le mot de passe entré ne correspond pas au vôtre.")
        else:
            self.data['password'] = new
            self.game.db.put('player', self.data['pseudo'], self.data)
            info(self, "Votre nouveau mot de passe est enregistré.")

    def set_email(self, email):
        """ Player command to change his email. """
        self.data['email'] = email
        self.game.db.put('player', self.data['pseudo'], self.data)
        info(self,
            "Votre adresse électronique est ‹<i>{}</i>›."
            .format(self.data['email']))

    def create_character(self, name):
        """ creates a new character."""
        name = name.capitalize()
        if name in self.data['characters']:
            info(self,
                "Vous avez déjà un personnage nommé {}."
                .format(name))
            return
        if not check_character_name(self, name):
            return
        # the name is valid, use it.
        self.data['characters'].append(name)
        self.game.db.put('player', self.data['pseudo'], self.data)
        self.character = Character(self.game, self, name)
        self.game.log("Character {} created.".format(self.character.data['name']))

    def play_character(self, name):
        "Plays an existing character."
        name = name.capitalize()
        if name in self.data['characters']:
            self.character = Character(self.game, self, name)
