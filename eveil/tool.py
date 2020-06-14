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
Command tool. Allows a character to create and define items.
"""

import re
from .message import info, pose
from .list_items import ITEMS
from .item import Item
from .grammar import Grammar

ITEMS_LIST = "|".join(ITEMS)

COMMANDS = {
    'apparence' : 'shortdesc',
    'description' : 'longdesc',
    'porté' : 'worndesc',
    'posé' : 'roomdesc',
    }
COMMANDS_LIST = "|".join(COMMANDS)

def tool(character, command):
    """Command tool: describe an item. We check for various matches
    and pick the correct one."""
    # first, we sanitize spaces
    command = re.sub(r"\s+", " ", command)
    character.game.log("tool {}".format(command))
    # we match for commands
    # fabriquer (un|une) (sous-vêtement|vêtement|manteau...)
    match = re.match(r"(un |une )*({})\s*$".format(ITEMS_LIST), command)
    if match:
        tool_create(character, match.group(2))
        return

    match = re.match(r"({}) (.*)\s*$".format(COMMANDS_LIST), command)
    if match:
        tool_describe(character, match.group(1), match.group(2))
        return

    match = re.match(r"genre (.*)\s*$", command)
    if match:
        tool_gender(character, match.group(1))
        return

    match = re.match(r"nombre (.*)\s*$", command)
    if match:
        tool_number(character, match.group(1))
        return

    match = re.match(r"finaliser\s*$", command)
    if match:
        tool_finalise(character)
        return

    info(character.player, """<b>Usage:</b><br/>
         item (un|une) [{}]<br/>
         item [{}] <i>description</i><br/>
         item genre <i>[masculin|féminin]</i><br/>
         item nombre <i>[singulier|pluriel]</i><br/>
         item finaliser"""
         .format(ITEMS_LIST, COMMANDS_LIST))

def get_item(character):
    """Finds the item in the character's inventory."""
    if not character.data["tooling"]:
        info(character.player, "Aucun objet n'est en cours de fabrication.")
        return None
    item = character.inventory.item_by_uid(character.data["tooling"])
    if not item:
        info(character.player, "Aucun objet trouvé.")
        return None
    return item

def tool_create(character, name):
    """Creates an item."""
    if character.data["tooling"]:
        item = get_item(character)
        info(character.player, "{} est déjà en train de fabriquer {}."
             .format(character.data["name"], item.data["shortdesc"]))
        return
    uid = character.game.db.uid()
    item = Item(character.game, uid)
    item.template(name)
    if not character.inventory.add_item(item):
        character.room.container.add_item(item)
    character.data["tooling"] = item.uid
    pose(character, "/Il fabrique {}.".format(item.data["shortdesc"]))

def retool(character, keyword):
    """Retool an item."""
    if character.data["tooling"]:
        item = get_item(character)
        info(character.player, "{} est déjà en train de fabriquer {}."
             .format(character.data["name"], item.data["shortdesc"]))
        return
    item = character.inventory.get_item('shortdesc', keyword)
    if item:
        character.data["tooling"] = item.uid
        pose(character, "/Il modifie {}.".format(item.data["shortdesc"]))
    else:
        info(character.player, "Aucun objet ne correspond au mot clé {}."
             .format(keyword))

def tool_describe(character, key, description):
    """Describe the item."""
    item = get_item(character)
    if not item:
        return
    # Fix punctuation.
    if key == 'shortdesc':
        description = re.sub('(.|!|?)?$', '', description).lower()
    else:
        if description[-1] != '.':
            description += '.'
        description = description.capitalize()
    item.data[COMMANDS[key]] = description
    item.put()
    info(character.player, "item {}: {}".format(key, description))

def tool_gender(character, gender):
    """Set the gender of the item."""
    item = get_item(character)
    if not item:
        return
    if gender not in Grammar.GENDERS:
        genders = "|".join(gen for gen in Grammar.GENDERS)
        info(character.player, "<b>Usage:</b> fabriquer genre <i>{}</i>"
             .format(genders))
        return
    item.data["gender"] = Grammar.GENDERS.index(gender)
    item.put()
    info(character.player, "item genre: {}.".format(gender))

def tool_number(character, number):
    """Set the number of the item."""
    item = get_item(character)
    if not item:
        return
    if number not in Grammar.NUMBERS:
        numbers = "|".join(num for num in Grammar.NUMBERS)
        info(character.player, "<b>Usage:</b> fabriquer genre <i>{}</i>"
             .format(numbers))
        return
    item.data["number"] = Grammar.NUMBERS.index(number)
    item.put()
    info(character.player, "item nombre: {}.".format(number))

def tool_finalise(character):
    """Finalize an item."""
    item = get_item(character)
    if not item:
        return
    pose(character, "/Il apporte les dernières touches à {}."
         .format(item.data["shortdesc"]))
    character.data["tooling"] = None
