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

from .list_items import ITEMS

class Container():
    """Defines a container, ie the capacity to contain items.
    Rooms and items can have a container object.
    Containers data are persistent.
    """
    def __init__(self, game, uid):
        self.game = game
        self.uid = uid
        self.items = []
        if self.game.db.has('container', self.uid):
            self.data = self.game.db.get('container', self.uid)
            for item_uid in self.data['items']:
                item = Item(self.game, item_uid)
                self.items.append(item)
        else:
            self.data = {
                'items': [],
                'used_volume' : 0,
                'max_volume' : 10
            }
            self.game.db.put('container', self.uid, self.data)

    def add_item(self, item):
        """Puts an item in the container."""
        new_volume = self.data['used_volume'] + item.data['volume']
        if new_volume > self.data['max_volume']:
            return False
        self.items.append(item)
        self.data['items'].append(item.uid)
        self.data['used_volume'] = new_volume
        self.game.db.put('container', self.uid, self.data)
        return True

    def rem_item(self, item):
        """Remove an item from the container."""
        if item not in self.items:
            return False
        self.data['used_volume'] = self.data['used_volume'] - item.data['volume']
        self.items.remove(item)
        self.data['items'].remove(item.uid)
        self.game.db.put('container', self.uid, self.data)
        return True

    def get_item(self, uid):
        """Finds and returns an item by its uid."""
        for item in self.items:
            if item.uid == uid:
                return item
        return None

    def set_volume(self, volume):
        self.data['max_volume'] = volume
        self.game.db.put('container', self.uid, self.data)


class Item():
    """Defines an item. Items are all kind of ingame objects.
    They can have a container, and thus contain other items.
    Items data are persistent.
    Their data are:
        shortdesc: the short description.
        longdesc : the long description.
        roomdesc : the description shown when the item is in a room.
        worndesc : the item is wearable, description when worn.
        wornplace : where the item is worn: underwear, outerwear, head, cloak.
        gender : the gender of the item: masculine, feminine or neutral.
        number : the number of the item: singular or plural.
        volume : the volume of the item, in dm3.
        inner_volume: the volume of the container.
        container_id : the item is a container, the id of the container.
        position_id : the id of the container where the item is.
        value : The value of the item, in coins.
        quality : the quality of the item: rough, normal, or fine.
        weight : the weight of the item, in kg.
    """

    def __init__(self, game, uid=None):
        self.container = None
        self.game = game
        if uid:
            self.uid = uid
        else:
            self.uid = self.game.db.uid()
        if self.game.db.has('item', self.uid):
            self.data = self.game.db.get('item', self.uid)
            if self.data['container']:
                self.container = Container(self.game, self.data['container'])
        else:
            self.data = {
                "shortdesc": None,
                "longdesc" : None,
                "roomdesc" : None,
                "worndesc" : None,
                "wornplace" : None,
                "gender" : None,
                "number" : None,
                "volume" : 0,
                "container_id" : None,
                "position_id" : None,
                "value" : 0,
                "quality" : None,
                "weight" : 0,
            }
            self.game.db.put('item', self.uid, self.data)

    def template(self, name):
        """Creates a new item using list_items."""
        if name not in ITEMS:
            self.game.log("There's no item template named {}.".format(name))
            return
        self.data = ITEMS[name]
        if self.data['inner_volume'] > 0:
            self.data['container'] = self.game.db.uid()
            self.container = Container(self.game, self.data['container'])
            self.container.set_volume = self.data['inner_volume']
        self.game.db.put('item', self.uid, self.data) 

    def put(self):
        self.game.db.put('item', self.uid, self.data)
