# Copyright (C) 2018 Pierre Jean Fichet
# <pierrejean dot fichet at posteo dot net>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

class Container():
    def __init__(self, game, id=None):
        self.items = []
        self.items_id = []
        self.volume = 0
        self.max_volume = 10
        self.game = game
        if id:
            self.id = id
            self.get()
        else:
            self.id = self.game.db.new("container")
            self.put()

    def put(self):
        key = "container:" + str(self.id)
        self.game.db.put(key, self.items_id)

    def get(self):
        self.items_id = self.game.db.get("container:" + str(self.id))
        for id in self.items_id:
            item = Item(self.game)
            item.id = id
            item.get()
            self.items.append(item)
            self.items_id.append(item.id)

    def add_item(self, item):
        new_volume = self.volume
        if "volume" in item.attributes:
            new_volume = self.volume + item.attributes["volume"]
            if new_volume > self.max_volume:
                return False
        self.items.append(item)
        self.items_id.append(item.id)
        self.volume = new_volume
        return True

    def rem_item(self, item):
        if item not in self.items:
            return False
        if "volume" in item.attributes:
            self.volume = self.volume - item.attributes["volume"]
        self.items.remove(item)
        self.items_id.remove(item.id)
        return True


class Item():
    attributes = {
        "shortdesc": "the short description.",
        "longdesc" : "the long description.",
        "roomdesc" : "the description shown when the item is in a room.",
        "worndesc" : "the item is wearable, description when worn.",
        "wornplace" : "where the item is worn: underwear, outerwear, head, cloak."
        "gender" : "the gender of the item: masculine or feminine.",
        "number" : "the number of the itme: singular or plural.",
        "volume" : "the inimal volume of the item (when folded), in dm3.",
        "inner_volume" : "the maximal volume of the container, in dm3.",
        "container" : "the item is a container, the id of the container.",
        "value" : "The value of the item, in coins.",
        "quality" : "the quality of the item: rough, normal, or fine.",
        "weight" : "the weight of the item, in kg.",
    }

    def __init__(self, game, id=None):
        self.attributes = {}
        self.container = None
        self.game = game
        if id:
            self.id = id
            self.get()
        else:
            self.id = self.game.db.new("item")
            self.put()

    def put(self):
        key = "item:" + str(self.id)
        self.game.db.put(key, self.attributes)

    def get(self):
        self.attributes = self.game.db.get("item:" + str(self.id))
        if "container" in self.attributes:
            self.container = Container(game, self.attributes["container"])

    def set_container():
        if self.container == None:
            self.container = Container(self.game)
            self.attributes["container"] = self.container.id
