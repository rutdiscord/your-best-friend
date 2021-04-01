from . import language_processing
import random

no_good_phrases = [
    'I',
    'IT',
    'IT\'S',
    'ITS'
]

def generate(username, text, useverb=True):
    noun_phr, verb, adj = language_processing.tokenize(text) # Converts input text into tokens.
    print(noun_phr, verb, adj)

    noun_phr = [phrase for phrase in noun_phr if phrase not in no_good_phrases]

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
        un_verb = ["is"]

    try:
        rand_un_adj = random.choice(un_adj)
    except IndexError:
        return False
        
    rand_un_verb = random.choice(un_verb)

    return headlineGenerator(username, randPhrase, rand_un_adj, rand_un_verb, useverb)

def headlineGenerator(name, phrase, adjective, verb='', useverb=True):

    if useverb:
        v_ = verb
    else:
        v_ = 'is'

    c_list = ["thinks that", "said that", "stated that", "strongly believes that", "does not believe that", "made it public that they think that", "determined that", "believes that", "did not understand that"]

    c_ = random.choice(c_list)

    news_list = ["The Verge", "The Washington Post", "The BBC", "The Daily Mail", "The New York Times", "Fox News", "CNN", "NBC News", "Channel 4 News", "The /r/Undertale News Network", "MTT News", "Orangestar", "Bliv", "The /r/Undertale Staff Team", "The Sun", "MSNBC News", "The Fake News Network"]

    hl_list = [
        f"{name} {c_} {phrase.upper()} {v_.upper()} {adjective.upper()}!",
        f"You won't believe what {name} has to say about {phrase.upper()}!",
        f"{phrase.upper()} {v_.upper()} {adjective.upper()}? {name} thinks so!",
        f"5 Signs you might be like {name}: Do you think {phrase.upper()} {v_} {adjective.upper()}?",
        f"{name} hates this one weird trick! Learn to {v_.upper()} {phrase.upper()} today!",
        f"Did you know that {name} believes in {phrase.upper()}?",
        f"{random.choice(news_list)} has rated {name} as the {adjective} {phrase.upper()} of the year!",
        f"10 Reasons why {name} believes {adjective} {v_.upper()} {phrase.upper()}",
        f"The rumour come out: Does {phrase.upper()} {v_.upper()} {adjective.upper()}? {name} thinks so!",
        f"Is the last {phrase.upper()} you'll ever need?! r/Undertale User {name} thinks so!",
        f"{name}'s list of 10 {phrase.upper()}'s that actually work!",
        f"{name}'s opinion: {phrase.upper()} {v_.upper()} {adjective.upper()}. Do you agree?",
        f"/r/Undertale Exclusive: {name} was once spotted in {random.randint(2000, 2020)} rambling about {phrase.upper()}",
        f"Cancel Culture gone too far! Controversy strikes after {name} said: {adjective.upper()} {v_.upper()} {phrase.upper()}",
        f"Newhome in chaos! {phrase.upper()} is {adjective.upper()} says {name}!",
        f"Before you buy {phrase.upper()}, read what {name} said about it!",
        f"TESTED: Is {phrase.upper()} really {adjective.upper()}? An analysis by {name}",
        f"{name}'s favourite: {phrase.upper()}.",
        f"Are you a {adjective} {phrase.upper()}? Take {name}'s quiz today to find out!",
        f"Dentists hate them! Learn {name}'s one simple trick to become an {adjective} at using {phrase.upper()}",
        f"A day to remember! {name} has revealed that they think {phrase} is {adjective}!"
    ]

    headline = random.choice(hl_list)

    return headline