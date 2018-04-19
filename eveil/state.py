
class ClientState():
    player, chargen, game, admin, superadmin = range(5)

class PlayerState():
    checkpseudo, createpwd, checkpwd1, checkpwd2, \
        checkpwd3, confirmpwd, email, logged = range(8)

class CharacterState():
    checkname, playing = range(2)
