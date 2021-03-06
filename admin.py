import argparse, sys
import shelve
from eveil.data import Data
from collections.abc import Iterable

DATABASE = 'data.db'

def null(arg):
    "replaces game.log(), but does nothing."
    pass


def get(key):
    "get data in key."
    db = shelve.open(DATABASE)
    if key in db:
        print(db[key])
    db.close()

def put(key, dkey, value):
    "set data in key."
    db = shelve.open(DATABASE)
    if key in db:
        data = db[key]
    if dkey in data:
        if value.isdigit():
            value = int(value)
        data[dkey] = value
    db[key] = data
    print(data)
    db.close()

def search(string):
    "search for string in the database."
    db = shelve.open(DATABASE)
    for key in db:
        data = db[key]
        if not isinstance(data, Iterable):
            continue
        for dkey in data:
            if not isinstance(data[dkey], Iterable):
                continue
            if string in data[dkey]:
                print(key)
    db.close()

def keys():
    "list keys in the database."
    db = shelve.open(DATABASE)
    for key in db:
        print(key)
    db.close()

def dump():
    "dump all the data."
    db = shelve.open(DATABASE)
    for key in db:
        print(db[key])
    db.close()

def uid():
    "Creates a new uid."
    db = Data(null, DATABASE)
    print(db.uid())
    db.close()

def main(argv):
    "parses options."
    parser = argparse.ArgumentParser(
        description="Admin tools for the game eveil.")
    parser.add_argument('command', nargs='*')

    args = parser.parse_args()

    #print(args.command)

    if args.command[0] == 'get':
        get(args.command[1])
    if args.command[0] == 'put':
        put(args.command[1], args.command[2], args.command[3])
    if args.command[0] == 'search':
        search(args.command[1])
    if args.command[0] == 'dump':
        dump()
    if args.command[0] == 'keys':
        keys()
    if args.command[0] == 'uid':
        uid()

if __name__ == "__main__":
    main(sys.argv[1:])
