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
A list of default items. They're poorly described, as an invitation
for players to do it carefully.
"""

ITEMS = {

"sous-vêtement": {
    "shortdesc": "un sous-vêtement",
    "longdesc" : "Ce sous-vêtement est parfaitement quelconque.",
    "roomdesc" : "Un sous-vêtement est ici.",
    "worndesc" : "Un sous-vêtement couvre sa peau.",
    "wornplace" : 1,    # hold=0, underwear=1, outerwear=2, cloak=3
    "gender" : 1,       # neutre=0 masculin=1, féminin=2
    "number" : 0,       # singulier=0, pluriel=1
    "volume" : 1,       # When folded, in dm3. Minimum is 1.
    "value" : 10,       # default to 10
    "quality" : 0,      # rough=0, normal=1, fine=2
    "weight" : 250,     # in gram.
    "inner_volume" : 0, # container volume - 0 if not a container.
    "container_id" : None,
    "position_id" : None,
},

"vêtement": {
    "shortdesc": "un vêtement quelconque",
    "longdesc" : "Ce vêtement est parfaitement quelconque.",
    "roomdesc" : "Un vêtement est ici.",
    "worndesc" : "Un vêtement est sur ses épaules.",
    "wornplace" : 2,    # hold=0, underwear=1, outerwear=2, cloak=3
    "gender" : 1,       # neutre=0 masculin=1, féminin=2
    "number" : 0,       # singulier=0, pluriel=1
    "volume" : 1,       # When folded, in dm3. Minimum is 1.
    "value" : 10,       # default to 10
    "quality" : 0,      # rough=0, normal=1, fine=2
    "weight" : 250,     # in gram.
    "inner_volume" : 0, # container volume - 0 if not a container.
    "container_id" : None,
    "position_id" : None,
},

"manteau": {
    "shortdesc": "un manteau",
    "longdesc" : "Ce manteau est parfaitement quelconque.",
    "roomdesc" : "Un manteau est ici.",
    "worndesc" : "Un manteau lui couvre les épaules.",
    "wornplace" : 3,    # hold=0, underwear=1, outerwear=2, cloak=3
    "gender" : 1,       # neutre=0 masculin=1, féminin=2
    "number" : 0,       # singulier=0, pluriel=1
    "volume" : 1,       # When folded, in dm3. Minimum is 1.
    "value" : 10,       # default to 10
    "quality" : 0,      # rough=0, normal=1, fine=2
    "weight" : 250,     # in gram.
    "inner_volume" : 0, # container volume - 0 if not a container.
    "container_id" : None,
    "position_id" : None,
},

"sac": {
    "shortdesc": "un sac",
    "longdesc" : "Ce sac est parfaitement quelconque.",
    "roomdesc" : "Un sac est ici.",
    "worndesc" : "Un sac est sur ses épaules.",
    "wornplace" : 2,        # hold=0, underwear=1, outerwear=2, cloak=3.
    "gender" : 1,           # neutre=0 masculin=1, féminin=2.
    "number" : 0,           # singulier=0, pluriel=1.
    "volume" : 1,          # When folded, in dm3. Minimum is 1.
    "value" : 10,           # default to 10.
    "quality" : 0,          # rough=0, normal=1, fine=2.
    "weight" : 250,         # in gram.
    "inner_volume" : 10,   # container volume - 0 if not a container.
    "container_id" : None,
    "position_id" : None,
},

} # End of ITEMS
