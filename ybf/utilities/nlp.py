from . import language_processing
import random

def generate(username, text, useverb=True):
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

    return headlineGenerator(username, randPhrase, rand_un_adj, rand_un_verb, useverb)

def headlineGenerator(name, phrase, adjective, verb='', useverb=True):

    if useverb == True:
        v_ = verb
    else:
        v_ = 'IS'

    c_list = ["thinks that", "said that", "stated that", "strongly believes that", "does not believe that", "made it public that they think that", "determined that", "believes that", "did not understand that"]

    c_ = random.choice(c_list)

    hl_list = [
        f"{name} {c_} {phrase.upper()} {v_.upper()} {adjective.upper()}!",
        f"You Won't Believe What {name} Has To Say About {phrase.upper()}!",
        f"{phrase.upper()} {v_.upper()} {adjective.upper()}? {name.upper()} Thinks So!",
        f"5 Signs You Might Be Like {name}: Do you think {phrase.upper()} {v_} {adjective.upper()}?",
        f"{name} hates this one weird trick! Learn to {v_} {adjective.upper()} Today!",
        f"Did you know that {name} believes in {phrase.upper()}?",
        f"The Verge has rated {name} as {v_.upper()} {phrase.upper()} of the year!",
        f"10 Reasons why {name} believes {v_.upper()} {phrase.upper()}",
        f"Do you know {name}? Then did you know that {name} {c_} {v_}"
    ]

    headline = random.choice(hl_list)

    return headline