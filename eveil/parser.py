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

import re
from .message import pose, expose, info
from .look import look, look_in_inventory, look_in_equipment
from .tool import tool
from .manipulation import get_item, put_item, wear_item, rem_item, destroy_item

# Player states defining commands availability
class State():
    """ Player states defining commands availability """
    LOGIN = 10
    ACCOUNT = 20
    CHARGEN = 30
    IC = 40
    OOC = 50
    ADMIN = 60
    GOD = 70

class Scope():
    """ Scopes in which commands are availables """
    length = 9
    LOGIN, INGAME, ACCOUNT, CHARACTER, CHARGEN, IC, OOC, ADMIN, GOD = range(length)

class Cmd():
    """ This class implements a decorator used to:
    - record the ingame name and function name of a user command,
    - match the user input with the command name and arguments,
    - print a short usage if the arguments don't match.
    """
    # Dictionary of Cmd() instances
    commands = {}

    def __init__(self, scope, name, usage, regex, onfail = None):
        self.scope = scope # Scope in which the command is available
        self.name = name # Ingame name of the command
        self.usage = usage # human readable argument
        self.regex = re.compile(regex) # regex matching the argument
        self.onfail = onfail
        self.fn = None # Function name
        Cmd.commands[self.name] = self

    def __call__(self, fn):
        """ the decorator itself. If the arguments match,
        fn is executed, otherwise, a short usage is sent.
        """
        # We record the function name for that command
        self.fn = fn.__name__
        # And we decorate the function
        def decorated(cls, player, arg):
            m = self.regex.match(arg)
            if m:
                # if arguments match, we execute the command
                return fn(cls, player, m)
            else:
                # orelse we print a short usage
                if self.onfail is not None:
                    return getattr(cls, self.onfail)(player, arg)
                else:
                    return info(player,
                        "<b>Usage:</b> <code>{} <i>{}</i></code>."
                        .format(self.name, self.usage)
                        )
        return decorated


class Parser():
    """ This class implements a parser for the user input.
    The first word is matched against a list of available commands.
    If that match, the command is executed.
    Since the command functions are decorated with the Cmd decorator,
    their arguments are actually matched before the function is executed.
    """

    def __init__(self, game):
        self.game = game
        # We build a regex matching all available commands for a player State
        self.cmd_regex = {}
        self.cmd_regex[State.LOGIN] = self._make_regex(Scope.LOGIN)
        self.cmd_regex[State.ACCOUNT] = self._make_regex(
                Scope.INGAME, Scope.ACCOUNT
                )
        self.cmd_regex[State.CHARGEN] = self._make_regex(
                Scope.INGAME, Scope.CHARACTER, Scope.CHARGEN
                )
        self.cmd_regex[State.ADMIN] = self._make_regex(
                Scope.INGAME, Scope.CHARACTER, Scope.ADMIN
                )


    def _make_regex(self, *scopes):
        """ Build a regex matching all commands in the
        scopes given as arguments. """
        cmds = []
        # We go through all commands, and collect those
        # who are in one of the given scopes:
        for name in Cmd.commands:
            for scope in scopes:
                if Cmd.commands[name].scope == scope:
                    cmds.append(name)
        # Build the regex using the the "or" operator
        cmd_list = '|'.join(cmd for cmd in cmds)
        regex = re.compile(
            "^(?P<command>{})(?:\s+(?P<arguments>.*))?$".format(cmd_list)
            )
        return regex

    def parse(self, player, message):
        """ If the message matches with the regex of available commands
        for a given player state, execute the function relative to the
        matching command."""
        #test if the message match a command available for the player state
        matched = self.cmd_regex[player.get_state()].match(message)
        if matched:
            # execute the relative function
            cmd = matched.group("command")
            arg = matched.group("arguments") or ''
            getattr(self, Cmd.commands[cmd].fn)(player, arg)
        else:
            #self.game.log(
            #    "Unknown command <{}> for state {}."
            #    .format(message, player.get_state()))
            info(player, "<code>Arglebargle&nbsp;!?</code>")


    ### Commands
    # The decorator define the command scope, name, arguments
    # and regex used to match the arguments

    ### Universal commands ###

    @Cmd(Scope.INGAME, "quitter", "", "\s*$",)
    def _quit(self, player, arg):
        # game._parse_queue handles disconnect correctly
        info(player, "Au revoir.")
        player.client.close()

    ### Login commands ###

    @Cmd(Scope.LOGIN, "create", "pseudo password confirm email",
        "(\w+)\s+(\S+)\s+(\w+)\s+([^@]+@[^@]+)\s*$", "_logout")
    def _create(self, player, arg):
        player.create(arg[1], arg[2], arg[3], arg[4])

    @Cmd(Scope.LOGIN, "login", "password",
        "(\w+)\s+(\S+)\s*$", "_logout")
    def _login(self, player, arg):
        player.login(arg[1], arg[2])

    def _logout(self, player, arg):
        player.client.close()

    ### Account commands ###

    @Cmd(Scope.ACCOUNT, "pseudo", "nouveau_pseudo", "(\w+)\s*$")
    def _pseudo(self, player, arg):
        player.set_pseudo(arg[0])

    @Cmd(Scope.ACCOUNT, "secret", "ancien_mdp nouveau_mdp", "(\S+)\s+(\S+)\s*$")
    def _password(self, player, arg):
        player.set_password(arg[1], arg[2])

    @Cmd(Scope.ACCOUNT, "email", "mail@example.com", "([^@]+@[^@]+)\s*$")
    def _email(self, player, arg):
        player.set_email(arg[0])

    @Cmd(Scope.ACCOUNT, "créer", "nom_du_personnage", "(\w+)\s*$")
    def _new_character(self, player, arg):
        player.create_character(arg[0])

    @Cmd(Scope.ACCOUNT, "jouer", "nom_du_personnage", "(\w+)\s*$")
    def _play(self, player, arg):
        player.play_character(arg[0])

    ### General character commands ###

    @Cmd(Scope.CHARACTER, "aller", "[vers][ le| la| les] mot_clé", r".*\b(\w+)\s*$")
    def _go(self, player, arg):
        player.character.room.move(player.character, arg[1])

    @Cmd(Scope.CHARACTER, "regarder", "regarder [objet]", "(.*)$")
    def _look(self, player, arg):
        if arg[1]:
            look(player.character, arg[1])
        else:
            player.character.room.send_longdesc(player.character)

    @Cmd(Scope.CHARACTER, "inventaire", "", "^$")
    def _inventory(self, player, arg):
        look_in_inventory(player.character, player.character)

    @Cmd(Scope.CHARACTER, "équipement", "", "^$")
    def _equipment(self, player, arg):
        look_in_equipment(player.character, player.character)

    @Cmd(Scope.CHARACTER, "prendre", "prendre objet", "(.+)$")
    def _get_item(self, player, arg):
        get_item(player.character, arg[1]) 

    @Cmd(Scope.CHARACTER, "poser", "poser objet", "(.+)$")
    def _put_item(self, player, arg):
        put_item(player.character, arg[1])

    @Cmd(Scope.CHARACTER, "mettre", "mot_clé", "(\w+)\s*$")
    def _wear_item(self, player, arg):
        wear_item(player.character, arg[1])

    @Cmd(Scope.CHARACTER, "enlever", "mot_clé", "(\w+)\s*$")
    def _remove_item(self, player, arg):
        rem_item(player.character, arg[1])

    @Cmd(Scope.CHARACTER, "détruire", "mot_clé", "(\w+)\s*$")
    def _destroy_item(self, player, arg):
        destroy_item(player.character, arg[1])

    @Cmd(Scope.CHARACTER, "connaissances", "", "^$")
    def _list_remember(self, player, arg):
        player.character.remember.list_remember()

    @Cmd(Scope.CHARACTER, "retenir", "mot_clé nom", "(\w+)\s+(\S*)\s*$")
    def _set_remember(self, player, arg):
        player.character.remember.set_remember(arg[1], arg[2])

    @Cmd(Scope.CHARACTER, "pose", "petite pose", "(.+)\s*$")
    def _set_pose(self, player, arg):
        pose(player.character, arg[0])

    @Cmd(Scope.CHARACTER, "expose", "longue exposition", ".*")
    def _expose(self, player, arg):
        expose(player.character, arg[0])

    ### Chargen commands ###
   
    @Cmd(Scope.CHARGEN, "genre", "masculin|féminin", "(masculin|féminin)\s*$")
    def _gender(self, player, arg):
        player.character.set_gender(arg[0])

    @Cmd(Scope.CHARGEN, "nom", "nom", "(\w+)\s*$")
    def _name(self, player, arg):
        player.character.set_name(arg[0])

    @Cmd(Scope.CHARGEN, "apparence", "courte description", "(.+)\s*$")
    def _shortdesc(self, player, arg):
        player.character.set_shortdesc(arg[0])

    @Cmd(Scope.CHARGEN, "description", "longue description", "(.+)\s*$")
    def _longdesc(self, player, arg):
        player.character.set_longdesc(arg[0])

    @Cmd(Scope.CHARGEN, "item", "", ".*\s*$")
    def _tool(self, player, arg):
        tool(player.character, arg[0])

    ### Admin commands ###

    @Cmd(Scope.ADMIN, "shutdown", "", "\s*$")
    def _shutdown(self, player, arg):
        self.game.shutdown()

