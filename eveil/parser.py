
class Parser():

    def __init__(self, game):
        self.game = game

    def parse(self, player, message):
        # Player logging
        if player.state != player.LOGGED:
            player.parse(message)
            return
        # Character generation commands
        # Admin commands
        if message == "shutdown":
            self.game.shutdown()
