
class Parser():

    def __init__(self, game):
        self.game = game

    def parse(self, player, message):
        # Admin commands
        if message == "shutdown":
            self.game.shutdown()
        # Player logging
        if player.state != player.LOGGED:
            player.parse(message)
            return
        try:
            command, text = message.split(' ', 1)
        except ValueError:
            return
        # Character generation commands
        if command == "genre:":
            player.character.cmd_gender(text)
        elif command == "nom:":
            player.character.cmd_name(text)
        elif command == "apparence:":
            player.character.cmd_shortdesc(text)
        elif command == "descripton:":
            player.character.cmd_longdesc(text)
        elif command == "métier:":
            player.character.cmd_skill(text)
        elif command == "talent:":
            player.character.cmd_talent(text)

