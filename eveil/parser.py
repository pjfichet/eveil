import re

class Cmd():
    """ This class implements a decorator used to:
    - record the ingame name and function name of a user command,
    - match the user input with the command name and arguments,
    - print a short usage if the arguments don't match.
    """
    commands = {}

    def __init__(self, name, usage, regex):
        #Cmd.commands.append(cmd)
        self.name = name # Ingame name of the command
        self.usage = usage # human readable argument
        self.regex = re.compile(regex) # regex matching the argument

    def __call__(self, fn):
        """ the decorator itself. If the arguments match,
        fn is executed, otherwise, a short usage is sent.
        """
        # We record the function name for that command
        Cmd.commands[self.name] = fn.__name__
        # And we decorate the function
        def decorated(cls, player, arg):
            m = self.regex.match(arg)
            if m:
                # if arguments match, we execute the command
                return fn(cls, player, m)
            else:
                # orelse we print a short usage
                return player.client.send(
                    "<p>Usage: <code>{} <i>{}</i></code></p>"
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
        # build the regex matching all commands.
        cmd_list = '|'.join(cmd for cmd in Cmd.commands)
        self.cmd_regex = re.compile(
            "^(?P<command>{})(?:\s+(?P<arguments>.*))?$".format(cmd_list)
            )

    def parse(self, player, message):
        """ If the message matches with the regex of all commands,
        execute the function relative to the matching command."""
        #test if the message match a command name
        matched = self.cmd_regex.match(message)
        if matched:
            # execute the relative function
            cmd = matched.group("command")
            arg = matched.group("arguments") or ''
            getattr(self, Cmd.commands[cmd])(player, arg)
        else:
            player.client.send("<p><code>Arglebargle&nbsp;!?</code></p>")


    ### Commands
    # The decorator define the command name and arguments
    # The regex is used to match the arguments

    ### Universal commands ###

    @Cmd("quitter", "", "\s*$")
    def _quit(self, player, arg):
        # game._parse_queue handles disconnect correctly
        player.client.close("Au revoir.")

    ### Player commands ###

    @Cmd("create", "pseudo password confirm email",
        "(\w+)\s+(\S+)\s+(\w+)\s+([^@]+@[^@]+)\s*$")
    def _create(self, player, arg):
        player.create(arg[1], arg[2], arg[3], arg[4])

    @Cmd("login", "password", "(\w+)\s+(\S+)\s*$")
    def _login(self, player, arg):
        player.login(arg[1], arg[2])

    @Cmd("pseudo", "nouveau_pseudo", "(\w+)\s*$")
    def _pseudo(self, player, arg):
        player.set_pseudo(arg[0])

    @Cmd("secret", "ancien_mdp nouveau_mdp", "(\S+)\s+(\S+)\s*$")
    def _password(self, player, arg):
        player.set_password(arg[1], arg[2])

    @Cmd("email", "mail@example.com", "([^@]+@[^@]+)\s*$")
    def _email(self, player, arg):
        player.set_email(arg[0])

    @Cmd("nouveau", "", "^$")
    def _new_character(self, player, arg):
        player.set_character()

    @Cmd("jouer", "personnage", "(\w+)\s*$")
    def _play(self, player, arg):
        player.set_character(arg[0])

    ### General character commands ###

    @Cmd("vers", "mot_clé", "(\w+)\s*$")
    def _go(self, player, arg):
        player.character.room.move(player.character, arg[0])

    ### Chargen commands ###
   
    @Cmd("genre", "homme|femme", "(homme|femme)\s*$")
    def _gender(self, player, arg):
        player.character.set_gender(arg[0])

    @Cmd("nom", "nom", "(\w+)\s*$")
    def _name(self, player, arg):
        player.character.set_name(arg[0])

    @Cmd("apparence", "courte description", "(\w[\s\w]+)\s*$")
    def _shortdesc(self, player, arg):
        player.character.set_shortdesc(arg[0])

    @Cmd("description", "longue description", "(\w[\s\w]+)\s*$")
    def _longdesc(self, player, arg):
        player.character.set_longdesc(arg[0])

    @Cmd("métier", "artisan|barde|chasseur|druide|guerrier",
            "(artisan|barde|chasseur|druide|guerrier)\s*$")
    def _skill(self, player, arg):
        player.character.set_skill(arg[0])

    @Cmd("talent", "agileté|constitution|force|intelligence|sagesse",
        "(agileté|constitution|force|intelligence|sagesse)\s*$")
    def _talent(self, player, arg):
        player.character.set_talent(arg[0])

    ### Admin commands ###

    @Cmd("shutdown", "", "\s*$")
    def _shutdown(self, player, arg):
        self.game.shutdown()

