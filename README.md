# Eveil: a roleplaying mud using websocket

## Description

Like some MUDs (Multi-User Dungeon) and MUSHes (Multi-User Shared
Hallucination), this game aims to provide a text only roleplaying
environment: The player creates a character and interacts with others
by describing its actions with the `pose` command.

But while MUDs and MUSHes are traditionnaly played via telnet, this
game uses the websocket protocol, and is playable from the web browser.

The focus of this game being a roleplaying environment, it will
not provide any mobile, non playing, characters, nor hack and slash
mechanics. Instead, it aims to provide simple functionalities to improve
the roleplaying atmosphear:

- A templating system to write dynamics room descriptions. This allows to
adapt the description with the weather or the time of the day, or to center
it on the current character.
- A simple path finding algorytm.
- A versatile crafting system (to do), to create unique items.
- An RPXP system (to do): the player earns points by roleplaying, these
points can be used to improve his character.
- And since there's no french roleplaying mud, the official game language
is french.

## Installation

The game is developped with `python` version `3.6.5`, other versions
are not tested.
- Persistent storage is provided by the standart `shelve` module.
For better performances, you should install `gdbm`, which `shelve`
will use as backend.
- Passwords are encypted with the standart `crypt` module. For stronger
encryption, you should install `sha256`, which `crypt` will use.

## Usage

Open the file `eveil.html` with your web browser, and starts the game
with `make start`. That will create a database in the file `data.db`.

## License

The game is distributed under the ISC license, except for these two third
party files, distributed under the MIT License:
- `eveil/template.py`, which is a modification of templite.py by Ned Batchelder,
distributed as part of the _500 lines_ book,
<https://github.com/aosabook/500lines/tree/master/template-engine/code>,
- `eveil/SimpleWebSocket.py`, written by Dave P.,
<https://github.com/dpallot/simple-websocket-server>.
