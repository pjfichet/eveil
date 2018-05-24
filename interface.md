# Eveil User Interface

This file list the commands and documents the user interface of eveil.
Not all commands are currently implemented: this file actually serves
to define and ponder the user interface.

## Universal commands
- `quitter`
- `aide <helpfile_keyword>`

## Account commands

- `pseudo <new_pseudonyme>`
- `secret <new_password>`
- `email <new_email>`
- `jouer <character_name>`
- `nouveau <character_name>`

## chargen commands

- `nom <character_name>`
- `genre <character_gender>`
- `apparence <character_shortdesc>`
- `description <character_longdesc>`

## universal character commands

- `aller <room_name_keyword>` move to the first next room containing the keyword.
- `chemin <room_name_keyword>` sets a path. Move with `aller`.
- `voir [<object_keyword>]`

## Crafting commands

- `item` list the categories of items one can create.
- `item <item_category>` set the category of the item.
- From now, `item` lists the available attribute fields and their
content. Remember that some attributes are read only.
- `item <field_name> <text|value>` sets the content of a field, ie:
  - `item apparence <item short description>`
  - `item description <item long description>`
  - `item posé <item description as seen on a room>`
  - `item porté <item description as seen when worn>`
- `item fabrique` creates the item, reset all fields.
- `item <object_in_inventory>` delete the object, but fill the item fields
with the attributes of the object, allowing one to edit the attributes
and create the object again. That should probably be reserved to the
initial creator of the object.

## admin commands

- `shutdown`
- `reboot` reboot the game without shutting down the server.
