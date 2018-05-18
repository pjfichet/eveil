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

class Item():

    def __init__(self):
        self.id = None
        self.shortdesc = None
        self.longdesc = None
        self.attributes = []

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def has_attribute(self, name):
        for attribute in self.attributes:
            if attribute.name == name:
                return True
        return False

    def get_attribute(self, name):
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute
        return None


class AtContainer():

    def __init__(self, item):
        self.item = item
        self.name="container"
        self.max_volume = 10
        self.volume = 0
        self.items = []

    def add_item(self, item):
        vol = 0
        volume =  item.get_attribute(volume)
        if volume:
            vol = volume.volume
        if self.volume + vol <= self.max_volume:
            return False
        self.volume = self.volume + vol
        self.items.append(item)
        return True
        
    def rem_item(self, item):
        if item not in self.items:
            return False
        vol = 0
        volume = item.get_attribute(volume)
        if volume:
            vol = volume.volume
        self.volume = self.volume - vol
        self.items.remove(item)
        return True


class AtQuality():
    QUALITIES = [ "rough", "normal", "fine" ]

    def __init__(self, item):
        self.item = item
        self.name="quality"
        self.quality = 0


class AtValue():

    def __init__(self, item):
        self.item = item
        self.name="value"
        self.value = 0


class AtWear():
    LEVELS = [ "underwear", "outerwear", "cloak" ]

    def __init__(self, item):
        self.item = item
        self.name="wear"
        self.level = 1

