from .state import ClientState


class Parser():

    def __init__(self):
        pass

    def parse(self, client, message):
        if client.getState() == ClientState.player:
            client.player.parse(message)
        elif client.getState() == ClientState.chargen:
            pass
            #client.character.parse(message)
