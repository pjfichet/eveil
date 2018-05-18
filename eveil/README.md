# Eveil source tree

This folder contains the main code of the game, and this short explanation
should help people to find their way in the source tree.

## SimpleWebSocket.py

This is the code of the websocket server. It is a third party module,
which has not been modified.

## server.py

It adapts the SimpleWebSocket module for the needs of the game by monkey
patching. It adds a queue to each connection, which is used to send datas
to the game. It links each connection with a player instance. And it it
setups the server to be started in a dedicated thread, using the Thread module.

## __init__.py

It starts the game. It creates a server instance and a game instance. It
creates a queue used to send datas from the server to the game.it loads
each python script contained in the _world/_ directory. It starts the
server in a dedicated thread, and eventually starts the game.

## game.py

The main game loop. It initializes the database, the map, the game time,
the parser, and listens for messages comming from the server through the
queue: it deals with connection and disconnection by creating or recording
a player instance, and sends received messages to the parser. It also
handles properly the shutdown.

## data.py

The connection to the database. It uses the standart shelve module as
database, which in turns will use gdbm if available. It implements a
reddis like database. Keys are of the form `key:id`, with `id` starting at
1. The last `id` of a given key is stored in the key `key`. Dictionaries
are used to store various data on a given key. The main  methods publicly
exposed are:
- Data.put(key, data): record `data` in key `key`. It should only be
used to update an entry, to add a new entry to the database, Data.add
should be used instead.
- Data.get(key): gets the data from key `key`. Returns false if there's
no such key in the database.
- Data.rem(key): removes (delete) an entry from the database.
- Data.new(key): It defines a new key id, by incrementing the last `id`
of the key `key`. It returns that last id.

A simple usage would be:

```python
id = new("key")
put("key:" + id, "Some data")
data = get("key:" + id)
```

# parser.py

Parses the data sent by the user, and executes the required command.
This file implements the Cmd class which is used to _decorate_
each commands to define:
- the scope in which the command is available,
- the command name, as exposed to the users,
- a short usage,
- and a regex matching the arguments the command accepts.
When a command sent by the player is recognized, the Cmd decorator checks
that the arguments matches before executing the command, and send the
short usage otherwise.

When instanciated, the Parser class builds, for each scope, a regex
matching all the commands names available in that scope. These regexes
are used to match the player input.

This file also contains the list of scopes, in the class State.

# player.py

A class instanciated for each player or connection. A player has a pseudo,
a password, an email, and some connection datas, which are all recorded
in the database. A player may also have several created character. On
login the player can update these informations, create a new character
or play an old one.

# character.py

Each player can have several characters. The characters states are
recorded in the database.

# grammar.py

Since characters have a gender, the file grammar.py implements a class to
easily write texts agreeing the pronouns with the gender of the character.

# template.py

It is a third party module implementing a template renderer, using the
Django syntax. Its author, Ned Batcheler, published a complete description
of its algorytm:
<http://aosabook.org/en/500L/a-template-engine.html>.

For the purpose of the game, it has been modified so that more test
cases are available. Templates are used to describe rooms.

# map.py

This file implements a directed graph defining the map (or grid). The
class Map implements the graph, the Room class implements the nodes,
and the Link class implements the edges. The Door class implements door
which can be added to a Link instance.

The class Map should be used to instanciate rooms and links with the
`new_room` and `new_link` methods:

```python
# the map instance
map = Map(game)
# create some rooms
room_1 = map.new_room()
room_1.shortdesc = "An example room"
room_1.longdesc = Template("<h3>{{room_2.shortdesc}}</h3>")
room_2 = map.new_room()
room_2.shortdesc = "A second room"
room_2.longdesc = Templat("<h3>{{room_2.shortdesc}}</h3>")
# create some links
link_1_2 = map.new_link(room_1, room_2)
link_1_2.dynadesc = "leaving the first room"
link_2_1 = map.new_link(room_2, room_1)
link_2_1.dynadesc = "leaving the second room"
```

# item.py

A set of classes used to define the items in game. It uses a kind of
Entity-Component approach: the Item class is only a support for various
attributes. Each attribute is defined as an independant class. There are,
for example, an attribute value, quality, wearable, etc.
