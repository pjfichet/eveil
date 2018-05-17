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

class Grammar():
    """Meta class to agree heritating objects in number and gender."""
    GENDERS = ["homme", "femme"]
    MASCULINE = 0
    FEMININE = 1
    SINGULAR = 0
    PLURAL = 1
    PRONOUNS = {
        # pronoun: {
        #   [singular masculine, singular feminine],
        #   [plural masculine, plural feminine]
        # }
        'ce': [['ce', 'cette'], ['ces', 'ces']],
        'du': [['du', 'de la'], ['des', 'des']],
        'il': [['il', 'elle'], ['ils', 'elles']],
        'son': [['son', 'sa'], ['leur', 'leur']],
        'un': [['un', 'une'], ['des', 'des' ]],
    }


    def __init__(self):
        self.gender = None
        self.number = None

    def pronoun(self, pronoun, capitalize=False):
        """ Shortcut to agree pronouns in number and gender. """
        if capitalize:
        	return Grammar.PRONOUNS[pronoun][self.number][self.gender].capitalize()
        else:
        	return Grammar.PRONOUNS[pronoun][self.number][self.gender]

    