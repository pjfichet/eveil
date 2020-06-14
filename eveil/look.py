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

"""
Functions for the command look.
"""

import re
from .message import info, fmt

def look(from_char, command):
    """Command look. We check various matches and pick the correct
    one."""
    # first, we sanitize spaces
    command = re.sub(r"\s+", " ", command).lower()
    # regarder l'objet:
    match = re.match(r"(le |la |les |l')?(\w+)\s*$", command)
    if match:
        look_at(from_char, match.group(2))
        return
    # regarder dans la boite:
    match = re.match(r"(dans|sur) (le |la |les |l')?(\w+)\s*$", command)
    if match:
        look_in(from_char, match.group(3))
        return
    # regarder l'objet dans la boite
    match = re.match(r"(le |la |les |l')?(\w+)\s(dans|de|sur)\s(le |la |les |l')?(\w+)\s*$", command)
    if match:
        look_at_in(from_char, match.group(5), match.group(2))
        return
    info(from_char.player, """<b>Usage:</b>
        <code>regarder [le|la|les|l'] <i>mot_clé</i></code><br/>
        <code>regarder [dans|sur] [le|la|les|l'] <i>mot_clé</i></code><br/>
        <code>regarder [le|la|les|l'] <i>mot_clé</i> [dans|de|sur|d']
        [le|la|les|l'] <i>mot_clé</i></code>""")

def look_fmt(character, shortdesc, longdesc):
    character.player.client.send("<p><b>{} regarde {}</b>. — {}</p>"
        .format(character.data["name"], shortdesc, longdesc))

def look_at(from_char, keyword):
    """Regarder émilie"""
    # look at character
    for character in from_char.room.characters:
        if keyword in from_char.remember.get_remember(character).lower():
            look_at_character(from_char, character)
            return
    # look at item in inventory
    item = from_char.inventory.get_item('shortdesc', keyword)
    if item:
        look_at_item(from_char, item)
        return
    # look at item in equipment
    item = from_char.equipment.get_item('worndesc', keyword)
    if item:
        look_at_item(from_char, item)
        return
    # look at item in room
    item = from_char.room.container.get_item('roomdesc', keyword)
    if item:
        look_at_item(from_char, item)
        return
    # nothing found
    info(from_char.player,
         "Aucun personnage ni objet ne correspond au mot clé « {} »."
         .format(keyword))

def wornlist(character, top=False):
    if not character.equipment.items:
        if character.data['gender'] > 1:
            return "Elle est toute nue."
        else:
            return "Il est tout nu."
    layers = {}
    visible = 0
    for item in character.equipment.items:
        # sort items by wornplace
        key = item.data['wornplace']
        if key > visible:
            visible = key
        if key in layers:
            layers[key] = layers[key] + ", " + item.data['worndesc']
        else:
            layers[key] = item.data['worndesc']
    if top:
        return layers[visible].capitalize() + '.'
    garment = '. '.join([layers[key].capitalize() for key in layers])
    garment += '.'
    return garment


def look_in_equipment(from_char, to_char):
    """ Look in equipment, only show visible items."""
    layers = wornlist(from_char)
    fmt(from_char,
        "{} regarde son équipement".format(from_char.data['name']),
        layers)

def look_at_character(from_char, to_char):
    """Look at a character."""
    visible = wornlist(from_char, top=True) 
    if from_char == to_char:
        title = "{} se regarde".format(from_char.data['name'])
    else:
        title =  "{} regarde {}".format(
                    from_char.data['name'],
                    from_char.remember.get_remember(to_char))
    content = "{}</p><p>{}".format(to_char.data['longdesc'], visible)
    fmt(from_char, title, content)

def look_at_item(from_char, item):
    """Look at an item."""
    title = "{} regarde {}".format(
                from_char.data['name'],
                item.data['shortdesc'])
    fmt(from_char, title, item.data['longdesc'])

def look_in(from_char, keyword):
    """Regarder dans le coffre"""
    # look in character = look at his equipment
    for character in from_char.room.characters:
        if keyword in from_char.remember.get_remember(character).lower():
            visible = wornlist(character, top=True) 
            if from_char == character:
                title = "{} regarde son équipement".format(from_char.data['name'])
            else:
                title = "{} regarde l'équipement de {}".format(
                            from_char.data['name'],
                            from_char.remember.get_remember(character))
            fmt(from_char, title, visible)
            return
    # look in something in inventory
    item = from_char.inventory.get_item('shortdesc', keyword)
    if item:
        look_in_container(from_char, item)
        return
    # look in something in equipment
    item = from_char.equipment.get_item('worndesc', keyword)
    if item:
        look_in_container(from_char, item)
        return
    # look in something in room
    item = from_char.room.container.get_item('roomdesc', keyword)
    if item:
        look_in_container(from_char, item)
        return
    info(from_char.player, "Aucun objet ne correspond au mot clé « {} »."
        .format(keyword))

def look_in_container(from_char, item):
    """Look in a container."""
    if not item.container:
        info(from_char.player, "{} ne peut pas regarder dans {}."
             .format(from_char.data["name"], item.data['shortdesc']))
        return
    if not item.container.items:
        info(from_char.player, "{} est vide.".format(
             item.data["shortdesc"].capitalize() ))
        return
    title = "{} regarde dans {}".format(from_char.data['name'],
                item.data['shortdesc'])
    fmt(from_char, title, item.container.list_items('shortdesc'))

def look_in_inventory(from_char, to_char):
    """ look in inventory."""
    if not to_char.inventory.items:
        info(from_char.player, "{} ne transporte rien.".format(
             to_char.data["name"]))
        return
    items = to_char.inventory.list_items('shortdesc')
    title = "{} regarde son inventaire".format(from_char.data['name'])
    fmt(from_char, title, items)

def look_at_in(from_char, key_container, key_item):
    """look at something in container. Here, we search for the correct
    container key"""
    # look at something on character
    for character in from_char.room.characters:
        if key_container in from_char.remember.get_remember(character).lower():
            look_at_in_equipment(from_char, character, key_item)
            return
    # look at something in inventory
    item = from_char.inventory.get_item('shortdesc', key_container)
    if item:
        look_at_in_container(from_char, item, key_item)
        return
    # look at something in equipment
    item = from_char.equipment.get_item('shortdesc', key_container)
    if item:
        look_at_in_container(from_char, item, key_item)
        return
    # look at something in room
    item = from_char.room.container.get_item('roomdesc', key_container)
    if item :
        look_at_in_container(from_char, item, key_item)
        return
    # nothing found
    info(from_char.player,
        "Aucun personnage ni objet ne correspond au mot clé « {} »."
        .format(key_container))

def look_at_in_equipment(from_char, to_char, keyword):
    "look at something in equipment"
    item = to_char.equipment.get_item('worndesc', keyword)
    if item:
        look_at_item(from_char, item)
    else:
        info(from_char.player,
            "{} ne porte aucun objet correspondant au mot clé « {} »."
            .format(from_char.remember.get_remember(to_char), keyword))

def look_at_in_container(from_char, item, keyword):
    """look at something in container. Here, we have found the
    container, we search for an object in it"""
    if not item.container:
        info(from_char.player, "{} ne peut pas regarder dans {}."
             .format(from_char.data["name"], item.data['shortdesc']))
        return
    obj = item.container.get_item('shortdesc', keyword)
    if obj:
        look_at_item(from_char, obj)
    else: 
        info(from_char.player,
            "{} ne contient aucun object correspondant au mot clé « {} »."
            .format(item.data["shortdesc"], keyword))
