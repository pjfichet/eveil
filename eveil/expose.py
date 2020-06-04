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

import re

def info(player, text):
    "Game information sent to a player."
    player.client.send("<p class='info'>{}</p>".format(text))

def _has_name(name, text):
    name = '/' + name.lower()
    if re.search("/il|/elle|/{}".format(name), text, re.IGNORECASE):
        return True
    else:
        return False

def pose(from_char, text):
    "Print a short pose or what some games call an action."
    if not _has_name(from_char.data['name'], text):
        from_char.player.client.send(
            """<p><code><i>/{}</i>, <i>/il</il> ou <il>/elle</il>,
            doit apparaître dans la pose.</code></p>"""
            .format(from_char.data['name']))
        return
    if text[-1] in ('.', '!', '?'):
        text = text[:-1]
    for to_char in from_char.room.characters:
        newtext = expose_format(from_char, to_char, text)
        to_char.player.client.send("<p>{}.</p>".format(newtext))
    from_char.data['pose'] = text

def expose(from_char, text):
    "Print a long expose, ie an emote."
    if not _has_name(from_char.data['name'], text):
        from_char.player.client.send(
            """<p><code><i>/{}</i>, <i>/il</il> ou <il>/elle</il>,
            doit apparaître dans l'exposition.</code></p>"""
            .format(from_char.data['name']))
        return
    for to_char in from_char.room.characters:
        newtext = expose_format(from_char, to_char, text)
        to_char.player.client.send("<p><b>{}</b>. — {}</p>".format(
            to_char.remember.get_remember(from_char), newtext))

def off_topic(from_char, text):
    "Off topic, or out of character, communication."
    for to_char in from_char.room.characters:
        newtext = expose_format(from_char, to_char, text)
        to_char.player.client.send(
            "<p class='off_topic'>{}</p>".format(newtext))

def expose_format(from_char, to_char, text):
    "Format an expose."
    # We want to subsitute /keyword with a character name.
    # The difficulty is that "keyword" is only valid from the
    # sender point of view, and the character name depends on
    # the recipient point of view.

    # First, we define a backend function for re.sub()
    # we have to place it here, because the backend only accepts
    # one argument, and we need to pass it from_char and to_char.
    def find_name(matchobj):
        keyword = matchobj.group(0)
        keyword = keyword[1:] # removes the '/'
        # /Il /Elle /il /elle refers to the sender's character
        if keyword in ('Il', 'Elle', 'il', 'elle'):
            if keyword[0] in ('I', 'E'):
                return to_char.remember.get_remember(from_char).capitalize()
            return to_char.remember.get_remember(from_char)
        # Otherwise, check who that keyword may refer to.
        for char in from_char.room.characters:
            # Search who that keyword refers to from the sender
            # point of view.
            if keyword.lower() in from_char.remember.get_remember(char).lower():
                # Search how that character is known from the
                # recipient point of view
                return to_char.remember.get_remember(char)
        # If nothing, returns the keyword itself.
        return keyword

    # Now, we substitute, and call the find_name function
    text = re.sub("/\w+", find_name, text)
    return text

