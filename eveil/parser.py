
class Parser():

    def __init__(self):
        pass

    def parse(self, player, message):
        # Player logging
        if player.state != player.LOGGED:
            player.parse(message)
            return
        # Character generation commands
