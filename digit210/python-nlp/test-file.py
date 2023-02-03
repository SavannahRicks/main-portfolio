import spacy


nlp = spacy.load('en_core_web_sm')
phrase = "hello"
print(phrase)

example = nlp(phrase)
for token in example:
    print(token.pos_)

