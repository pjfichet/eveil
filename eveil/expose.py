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

def expose_all(from_char, text):
    for to_char in from_char.room.characters:
        expose_one(from_char, to_char, text)

def expose_one(from_char, to_char, text):

    # We want to subsitute /keyword with a character name.
    # The difficulty is that "keyword" is only valid from the
    # sender point of view, and the character name depends on
    # the recipient point of view.

    # First, we define a backend function for re.sub()
    # we have to place it here, because the backend only accepts
    # one argument. And we need to know who from_char and to_char
    # are.
    def find_name(matchobj):
        keyword = matchobj.group(0)
        keyword = keyword[1:] # removes the '/'
        for char in from_char.room.characters:
            # Search who that keyword refers to from the sender
            # point of view.
            if keyword.lower() in from_char.get_remember(char).lower():
                # Search how that character is known from the
                # recipient point of view
                name = to_char.get_remember(char)
                return name
        return keyword

    # Now, we substitute, and call the find_name function
    text = re.sub("/\w+", find_name, text)
    to_char.player.client.send("<p>— {}</p>".format(text))