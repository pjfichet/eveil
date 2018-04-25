import re

COMMAND_REGEX = re.compile("^(?P<command>\
login|create|pseudo|secret|email|nouveau|jouer|\
genre|nom|apparence|description|metier|talent|\
shutdown)\
(?:\s+(?P<text>.*))?\
$")

ARGUMENT_REGEX = {
    # login commands
    "login": [ re.compile("(\w+)\s+(\S+)\s*$"),
        "login <i>login password</i>" ],
    "create": [ re.compile("(\w+)\s+(\S+)\s+(\w+)\s+([^@]+@[^@]+)\s*$"),
        "create <i>pseudo password confirm email</i>" ],
    # account commands
    "pseudo": [ re.compile("(\w+)\s*$"),
        "pseudo <i>nouveau_pseudo</i>" ],
    "secret": [ re.compile("(\S+)\s+(\S+)\s*$"),
        "secret <i>ancien_mdp nouveau_mdp</i>" ],
    "email" : [ re.compile("([^@]+@[^@]+)\s*$"),
        "email <i>mail@example.com</i>" ],
    "nouveau": [ re.compile("^$"),
        "nouveau" ],
    "jouer": [ re.compile("\s*$"),
        "jouer <i>personnage</i>" ],
    # chargen commands
    "genre": [ re.compile("(homme|femme)\s*$"),
        "genre <i>homme|femme</i>" ],
    "nom": [ re.compile("(\w+)\s*$"),
        "nom <i>nom</i>" ],
    "apparence": [ re.compile("(\w[\s\w]+)\s*$"),
        "apparence <i>courte description</i>" ],
    "description": [ re.compile("(\w[\s\w]+)\s*$"),
        "description <i>longue description</i>" ],
    "metier": [ re.compile("(artisan|barde|chasseur|druide|guerrier)\s*$"),
        "metier <i>artisan|chasseur|druide|guerrier|barde</i>" ],
    "talent": [ re.compile("(agileté|constitution|force|intelligence|sagesse)\s*$"),
        "talent <i>agileté|constitution|force|intelligence|sagesse</i>" ],
    # admin commands
    "shutdown": [ re.compile("\s*$"),
        "shutdown" ],
}

class Parser():

    def __init__(self, game):
        self.game = game

    ### Parser methods ###

    def usage(self, player, message):
        player.send("<p><b>Usage:</b> <code>{}</code></p>".format(message))

    def parse(self, player, message):
        """ If the message matches with the command regex,
        execute the function relative to that command."""
        #test if command match
        matched = COMMAND_REGEX.match(message)
        if matched:
            # test if arguments match
            cmd = matched.group("command")
            txt = matched.group("text")
            arg = ARGUMENT_REGEX[cmd][0].match(txt or '')
            #print(cmd, txt, arg)
            if arg:
                # arg is a match object:
                # arg[0] contains the whole matching sentence
                # arg[1] the first matching group
                getattr(self, "cmd_{0}".format(cmd))(player, arg)
            else:
                # TODO: find the correct way to handle special case failures
                if cmd == "login" or cmd == "create":
                    player.client.close()
                else:
                    self.usage(player, ARGUMENT_REGEX[cmd][1])

        else:
            # TODO: print the list of available commands
            player.send("<p><code>Arglebargle&nbsp;?</code></p>")

    ### Player commands ###

    def cmd_login(self, player, arg):
        player.dologin(arg[1], arg[2])

    def cmd_create(self, player, arg):
        player.docreate(arg[1], arg[2], arg[3], arg[4])

    def cmd_pseudo(self, player, arg):
        player.setpseudo(arg[0])

    def cmd_secret(self, player, arg):
        player.setpassword(arg[1], arg[2])

    def cmd_email(self, player, arg):
        player.setemail(arg[0])

    def cmd_nouveau(self, player, arg):
        player.setcharacter()

    def cmd_jouer(self, player, arg):
        player.setcharacter(arg[0])

    ### character commands ###

    def cmd_genre(self, player, arg):
        player.character.cmd_gender(arg[0])

    def cmd_nom(self, player, arg):
        player.character.cmd_name(arg[0])

    def cmd_apparence(self, player, arg):
        player.character.cmd_shortdesc(arg[0])

    def cmd_description(self, player, arg):
        player.character.cmd_longdesc(arg[0])

    def cmd_metier(self, player, arg):
        player.character.cmd_skill(arg[0])

    def cmd_talent(self, player, arg):
        player.character.cmd_talent(arg[0])

    ### Admin commands ###

    def cmd_shutdown(self, player, arg):
        self.game.shutdown()

