
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

def pronoun(pronoun, number=SINGULAR, gender=MASCULINE, capitalize=False):
    """ Shortcut to agree pronouns in number and gender. """
    if capitalize:
    	return PRONOUNS[pronoun][number][gender].capitalize()
    else:
    	return PRONOUNS[pronoun][number][gender]


