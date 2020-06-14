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
Item manipulation: get, drop, put, wear, remove, etc.
"""

import re
from .message import info, pose

def get_item(character, command):
    """Parses the get command."""
    # first, we sanitize spaces
    command = re.sub(r"\s+", " ", command).lower()
    # prendre objet:
    match = re.match(r"(le |la |les |l')?(\w+)\s*$", command)
    if match:
        get_item_from_room(character, match.group(2))
        return
    # prendre objet dans boite:
    match = re.match(r"(le |la |les |l')?(\w+) dans (le |la |les |l')?(\w+)\s*$", command)
    if match:
        get_item_from(character, match.group(2), match.group(4))
        return
    info(character.player, """<b>Usage:</b><br/>
         prendre [le|la|les|l'] <i>mot_clé</i></br>
         prendre [le|la|les|l'] <i>mot_clé</i> dans [le|la|les|l']
         <i>mot_clé</i>""")

def put_item(character, command):
    """Parses the put command."""
    # first, we sanitize spaces
    command = re.sub(r"\s+", " ", command).lower()
    # prendre objet:
    match = re.match(r"(le |la |les |l')?(\w+)\s*$", command)
    if match:
        put_item_in_room(character, match.group(2))
        return
    # prendre objet dans boite:
    match = re.match(r"(le |la |les |l')?(\w+) dans (le |la |les |l')?(\w+)\s*$", command)
    if match:
        put_item_in(character, match.group(2), match.group(4))
        return
    info(character.player, """<b>Usage:</b><br/>
         poser [le|la|les|l'] <i>mot_clé</i></br>
         poser [le|la|les|l'] <i>mot_clé</i> dans [le|la|les|l']
         <i>mot_clé</i>""")

def get_item_from_room(character, keyword):
    """Get an item (from the room)."""
    item = character.room.container.get_item('roomdesc', keyword)
    if not item:
        info(character.player,
             "Aucun objet ne correspond au mot clé {}.".format(keyword))
        return
    # we've found the item, move it
    character.room.container.rem_item(item)
    if character.inventory.add_item(item):
        pose(character, "/Il prend {}.".format(item.data["shortdesc"]))
    else:
        character.room.container.add_item(item)
        info(character.player,
             "{} transporte trop de choses pour pouvoir prendre {}."
             .format(character.data["name"], item.data["shortdesc"]))

def put_item_in_room(character, keyword):
    """Drop an item in the room."""
    item = character.inventory.get_item('shortdesc', keyword)
    if not item:
        info(character.player,
             "{} ne transporte aucun objet correspondant au mot clé {}."
             .format(character.data['name'], keyword))
        return
    # we've found the item, move it
    character.inventory.rem_item(item)
    if character.room.container.add_item(item):
        pose(character, "/Il pose {}.".format(item.data["shortdesc"]))
    else:
        character.inventory.add_item(item)
        info(character.player,
             "Il y a trop de choses ici pour que {} puisse y déposer {}."
             .format(character.data["name"], item.data['shortdesc']))

def wear_item(character, keyword):
    """Wears an item (on the equipment)"""
    item = character.inventory.get_item('shortdesc', keyword)
    if not item:
        info(character.player,
             "{} ne transporte aucun objet correspondant au mot clé {}."
             .format(character.data['name'], keyword))
        return
    # we've found the object, move it
    character.inventory.rem_item(item)
    if character.equipment.add_item(item):
        pose(character, "/il porte {}."
             .format(item.data['shortdesc']))
    else:
        character.inventory.add_item(item)
        info(character.player,
             "{} porte trop de choses pour pouvoir mettre {}."
             .format(character.data['name'], item.data['shortdesc']))

def rem_item(character, keyword):
    """removes an item (from the equipment)"""
    item = character.equipment.get_item("worndesc", keyword)
    if not item:
        info(character.player,
             "{} ne porte aucun objet correspondant au mot clé {}."
             .format(character.data['name'], keyword))
        return
    # we've found the object, move it
    character.equipment.rem_item(item)
    if character.inventory.add_item(item):
        pose(character, "/il enlève {}."
             .format(item.data['shortdesc']))
    else:
        character.equipment.add_item(item)
        info(character.player,
             "{} transporte trop de choses pour pouvoir retirer {}."
             .format(character.data['name'], item.data['shortdesc']))

def put_item_in(character, item_kw, container_kw):
    """Put an item in something."""
    # search for the container in the inventory
    item = character.inventory.get_item('shortdesc', container_kw)
    if item:
        if item.container:
            put_item_in_container(character, item, item_kw)
            return
    # search for the container in the equipment
    item = character.equipment.get_item('worndesc', container_kw)
    if item:
        if item.container:
            put_item_in_container(character, item, item_kw)
            return
    # search for the container in the room
    item = character.room.container.get_item('roomdesc', container_kw)
    if item:
        if container.container:
            put_item_in_container(character, item, item_kw)
            return
    # no container found
    info("Aucun objet ne correspond au mot clé {}.".format(container_kw))

def put_item_in_container(character, container, item_kw):
    """Put an item in a container."""
    item = character.inventory.get_item('shortdesc', item_kw)
    if not item:
        info("Aucun objet ne correspond au mot clé {}.".format(item_kw))
        return
    # item is found, move it in the container
    character.inventory.rem_item(item)
    if container.container.add_item(item):
        pose(character, "/Il met {} dans {}."
             .format(item.data['shortdesc'], container.data['shortdesc']))
    else:
        character.inventory.add_item(item)
        info("{} est déjà plein.").format(container.data['shortdesc'])

def get_item_from(character, item_kw, container_kw):
    """Get an item from something."""
    # search for the container in the inventory
    item = character.inventory.get_item('shortdesc', container_kw)
    if item:
        if item.container:
            get_item_from_container(character, item, item_kw)
            return
    # search for the container in the equipment
    item = character.equipment.get_item('worndesc', container_kw)
    if item:
        if item.container:
            get_item_from_container(character, item, item_kw)
            return
    # search for the container in the room
    item = character.room.container.get_item('roomdesc', container_kw)
    if item:
        if item.container:
            get_item_from_container(character, item, item_kw)
            return
    # nothing found
    info("Aucun objet ne correspond au mot clé {}.".format(container_kw))

def get_item_from_container(character, container, item_kw):
    """Get an item from a container."""
    item = container.container.get_item('shortdesc', item_kw)
    if not item:
        info("{} ne contient aucun objet correspondant au mot clé {}."
             .format(container.data['shortdesc'], item_kw))
        return
    # item is found, move it
    container.container.rem_item(item)
    if character.inventory.add_item(item):
        pose(character, "/il prend {} dans {}."
             .format(item.data['shortdesc'], container.data['shortdesc']))
    else:
        container.container.add_item(item)
        info(character.player,
             "{} transporte trop de choses pour pouvoir prendre {}."
             .format(character.data['name'], item.data['shortdesc']))
