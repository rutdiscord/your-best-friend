from . import language_processing
import random

def generate(username, text):
    noun_phr, verb, adj = language_processing.tokenize(text) # Converts input text into tokens.
    print(noun_phr, verb, adj)

    try:
        randPhrase = random.choice(noun_phr)
    except IndexError:
        return False

    print(randPhrase)

    un_adj = []
    un_verb = []

    for x in adj:
        if x not in randPhrase and x not in un_adj:
            un_adj.append(x)

    for x in verb:
        if x not in randPhrase and x not in un_verb:
            un_verb.append(x)

    print(un_adj)

    if len(un_adj) == 0:
        return False
    if len(un_verb) == 0:
        un_verb = ["IS"]

    rand_un_adj = random.choice(un_adj)
    rand_un_verb = random.choice(un_verb)

    return headlineGenerator(username, randPhrase, rand_un_adj, rand_un_verb)

def headlineGenerator(name, phrase, adjective, verb):

    headline = f"{name.upper()} thinks that {phrase.upper()} {verb.upper()} {adjective.upper()}!"

    return headline