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
    """Class to agree objects in number and gender."""
    
    GENDERS = ["neutre", "masculin", "féminin"]
    NUMBERS = ["singulier", "pluriel"]
    WORDS = {
        "neutre": {
            "pronom_sujet": "il",
            "pronom_cod": "le",
            "pronom_coi": "lui",
            "pronom_disjoint": "se",
            "article": "un",
            "determinant_possessif": "son",
            "mot_homme": "homme",
            },
        "masculin": {
            "pronom_sujet": "il",
            "pronom_cod": "le",
            "pronom_coi": "lui",
            "pronom_disjoint": "se",
            "article": "un",
            "determinant_possessif": "son",
            "mot_homme": "homme",
            },
        "féminin": {
            "pronom_sujet": "elle",
            "pronom_cod": "la",
            "pronom_coi": "lui",
            "pronom_disjoint": "se",
            "article": "une",
            "determinant_possessif": "sa",
            "mot_homme": "femme",
            },
    }
 
    def __init__(self, number_id=0, gender_id=0):
        self.agree(number_id, gender_id)

    def agree(self, number_id, gender_id):
        self.number = Grammar.NUMBERS[number_id]
        self.gender = Grammar.GENDERS[gender_id]
        self.il = self._get_word("pronom_sujet")
        self.le = self._get_word("pronom_cod")
        self.lui = self._get_word("pronom_coi")
        self.se = self._get_word("pronom_disjoint")
        self.un = self._get_word("article")
        self.son = self._get_word("determinant_possessif")
        self.homme = self._get_word("mot_homme")

    def _get_word(self, word):
        """ Shortcut to fetch a word in the WORDS dictionary."""
        return Grammar.WORDS[self.gender][word]
