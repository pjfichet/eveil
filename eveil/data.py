import shelve
from datetime import datetime


class Data:
    """
    Implement a reddis like database:
    - Keys are of the form 'key:id',
    - id starts at 1,
    - the last id for a given key is stored in the key 'key'.
    Dictionaries are used to store various data for a given key.
    """

    def __init__(self, game, filename):
        """
        Open the file containing the data.
        """
        self.game = game
        self.filename = filename
        self.db = shelve.open(self.filename)
        init = self.get('init')
        if init:
            self.game.log("Opening {} created on {}".format(self.filename, init))
        else:
            self.game.log("Creating {}".format(self.filename))
            self.put('init', datetime.now())

    def put(self, key, data):
        """
        Record a data.
        Should only be used to edit an existing entry.
        To create a new one, 'add' should be used instead.
        """
        self.db[key] = data

    def get(self, key):
        """ Get a data."""
        try:
            data = self.db[key]
        except KeyError:
            return False
        return data

    def rem(self, key):
        """ Delete an entry. """
        del self.db[key]

    def new(self, key):
        """
        Define a new key id by increasing the recorded one.
        """
        keyid = self.get(key)
        if keyid:
            keyid = keyid + 1
            self.put(key, keyid)
            return keyid
        else:
            self.put(key, 1)
            return 1

    def add(self, key, data):
        """
        Create a new entry, increase and record the key id.
        (Maybe not useful)
        """
        keyid = self.key(key)
        self.put(key + ':' + keyid, data)
        return keyid

    def close(self):
        """
        Close the database.
        """
        self.game.log("Closing {}.".format(self.filename))
        self.db.close()

    def serialize(self, key, function):
        """
        Apply a function to all the entries of a given key.
        """
        i = 1
        data = self.get(key + ':' + i)
        while data:
            function(key + ':' + i, data)
            i = i + 1
            data = self.get(key + ':' + i)
