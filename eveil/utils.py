from datetime import datetime

def log(message):
    print("{}: {}".format(datetime.now(), message))
