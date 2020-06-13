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
from .message import info

def look(from_char, command):
    """Command look. We check various matches and pick the correct
    one."""
    # first, we sanitize spaces
    command = re.sub(r"\s+", " ", command).lower()
    # regarder émilie:
    match = re.match(r"(\w+)\s*$", command)
    if match:
        look_at(from_char, match.group(1))
        return
    # regarder l'objet:
    match = re.match(r"(le |la |les |l')(\w+)\s*$", command)
    if match:
        look_at(from_char, match.group(2))
        return
    # regarder dans boite:
    match = re.match(r"(dans|sur) (\w+)\s*$", command)
    if match:
        look_in(from_char, match.group(2))
        return
    # regarder dans la boite:
    match = re.match(r"(dans|sur) (le |la |les |l')(\w+)\s*$", command)
    if match:
        look_in(from_char, match.group(3))
        return
    # regarder objet boite:
    match = re.match(r"(\w+)\s(\w+)\s*$", command)
    if match:
        look_at_in(from_char, match.group(2), match.group(1))
        return
    # regarder objet dans boite | regarder objet de|du|sur personnage:
    match = re.match(r"(\w+)\s(dans |de |du |sur |d')(\w+)\s*$", command)
    if match:
        look_at_in(from_char, match.group(3), match.group(1))
        return
    # regarder l'objet dans boite | regarder l'objet de personnage
    match = re.match(r"(le |la |les |l')(\w+)\s(dans |de |du |sur |d')(\w+)\s*$", command)
    if match:
        look_at_in(from_char, match.group(4), match.group(2))
        return
    # regarder objet dans la boite | regarder objet de|sur le personnage:
    match = re.match(r"(\w+)\s(dans|de|sur)\s(le |la |les |l')(\w+)\s*$", command)
    if match:
        look_at_in(from_char, match.group(4), match.group(1))
        return
    # regarder l'objet dans la boite | regarder l'objet de|sur le personnage:
    match = re.match(r"(le |la |les |l')(\w+)\s(dans|de|sur)\s(le |la |les |l')(\w+)\s*$", command)
    if match:
        look_at_in(from_char, match.group(5), match.group(2))
        return
    info(from_char.player, """<b>Usage:</b>
        <code>regarder [le|la|les|l'] <i>mot_clé</i></code><br/>
        <code>regarder [dans|sur] [le|la|les|l'] <i>mot_clé</i></code><br/>
        <code>regarder [le|la|les|l'] <i>mot_clé</i> [dans|de|sur|d']
        [le|la|les|l'] <i>mot_clé</i></code>""")



def look_at(from_char, keyword):
    """Regarder émilie"""
    for character in from_char.room.characters:
        if keyword in from_char.remember.get_remember(character).lower():
            look_at_character(from_char, character)
            return
    for item in from_char.inventory.items:
        if keyword in item.data['shortdesc'].lower():
            look_at_item(from_char, item)
            return
    for item in from_char.equipment.items:
        if keyword in item.data['worndesc'].lower():
            look_at_item(from_char, item)
            return
    for item in from_char.room.container.items:
        if keyword in item.data['roomdesc'].lower():
            look_at_item(from_char, item)
            return
    info(
        from_char.player,
        "Aucun personnage ni objet ne correspond au mot clé « {} »."
        .format(keyword))

def wornlist(character):
    if not character.equipment.items:
        if character.data['gender'] > 1:
            return "Elle est toute nue."
        else:
            return "Il est tout nu."
    wearlist = {}
    visible = 0
    for item in character.equipment.items:
        # sort items by wornplace
        key = item.data['wornplace']
        if key > visible:
            visible = key
        if key in wearlist:
            wearlist[key] = wearlist[key] + ", " + item.data['worndesc']
        else:
            wearlist[key] = item.data['worndesc']
    # we only returns the highest wornplace, since it covers
    # the other ones.
    return wearlist[visible]

def look_at_character(from_char, to_char):
    """Look at a character."""
    items = wornlist(from_char) 
    from_char.player.client.send(
        "<p>{}</p><p>{}</p>"
        .format(to_char.data['longdesc'], items.capitalize()))


def look_at_item(from_char, item):
    """Look at an item."""
    from_char.player.client.send(
        "<p>{}</p>"
        .format(item.data['longdesc']))

def look_in(from_char, keyword):
    """Regarder dans le coffre"""
    for item in from_char.room.container.items:
        if keyword in item.data['roomdesc'].lower():
            if item.container:
                look_in_container(from_char, item)
                return
            info(from_char.player, "{} ne peut pas regarder dans {}."
                .format(from_char.data["name"], item.data['shortdesc']))
    for character in from_char.room.characters:
        if keyword in from_char.remember.get_remember(character).lower():
            look_in_equipment(from_char, character)
            return
    info(from_char.player, "Aucun objet ne correspond au mot clé « {} »."
        .format(keyword))

def look_in_container(from_char, item):
    """Look in a container."""
    if not item.container.items:
        info(from_char.player, "{} est vide.".format(
            item.data["shortdesc"].capitalize() ))
        return
    list_items = ", ".join(
        obj.data["shortdesc"]
        for obj in item.container.items)
    from_char.player.client.send("<p>{}.</p>"
        .format(list_items.capitalize()))

def look_in_equipment(from_char, to_char):
    if not to_char.equipment.items:
        info(from_char.player, "{} ne porte rien.".format(
            to_char.data["name"]))
        return
    list_items = ", ".join(item.data["worndesc"]
        for item in to_char.equipment.items)
    from_char.player.client.send(
        "<p>{}.</p>".format(list_items.capitalize()))

def look_in_inventory(from_char, to_char):
    if not to_char.inventory.items:
        info(from_char.player, "{} ne transporte rien.".format(
             to_char.data["name"]))
        return
    list_items = ", ".join(item.data["shortdesc"]
        for item in to_char.inventory.items)
    from_char.player.client.send(
        "<p>{}.</p>".format(list_items.capitalize()))

def look_at_in(from_char, key_container, key_item):
    "regarder la veste d'émilie."
    for character in from_char.room.characters:
        if key_container in from_char.remember.get_remember(character).lower():
            look_at_in_equipment(from_char, character, key_item)
            return
    for item in from_char.room.container.items:
        if key_container in item.data['shortdesc'].lower():
            if item.container:
                look_at_in_container(from_char, item, key_item)
                return
            info(from_char.player, "{} ne peut pas regarder dans {}."
                .format(from_char.data["name"], item.data['shortdesc']))
    info(from_char.player,
        "Aucun personnage ni objet ne correspond au mot clé « {} »."
        .format(key_container))

def look_at_in_equipment(from_char, to_char, keyword):
    "regarder la veste d'émilie"
    for item in to_char.equipment.items:
        if keyword in item.data['worndesc'].lower():
            look_at_item(from_char, item)
            return
    info(from_char.player,
        "{} ne porte aucun objet correspondant au mot clé « {} »."
        .format(from_char.remember.get_remember(to_char), keyword))

def look_at_in_container(from_char, item, keyword):
    "regarder dans le coffre"
    if not item.container:
        return
    for obj in item.container.items:
        if keyword in obj.data["shortdesc"].lower():
            look_at_item(from_char, obj)
            return
    info(from_char.player,
        "{} ne contient aucun object correspondant au mot clé « {} »."
        .format(item.data["shortdesc"], keyword))
