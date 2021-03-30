import en_core_web_trf

def tokenize(text):
    # Load English tokenizer, tagger, parser and NER
    nlp = en_core_web_trf.load()

    doc = nlp(text)

    # Analyze syntax
    noun_phr = ([chunk.text for chunk in doc.noun_chunks])
    verb = ([token.lemma_ for token in doc if token.pos_ == "VERB"])
    adj = ([token.lemma_ for token in doc if token.pos_ == "ADJ"])
    return noun_phr, verb, adj

    # Find named entities, phrases and concepts
    for entity in doc.ents:
        print(entity.text, entity.label_)