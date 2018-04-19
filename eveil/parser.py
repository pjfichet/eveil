
class Parser():

    def __init__(self):
        pass

    def parse(self, player, message):
        if player.state != player.LOGGED:
            player.parse(message)
        else:
            pass
