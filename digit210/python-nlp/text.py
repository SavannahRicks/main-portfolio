import spacy
# nlp = spacy.cli.download('en_core_web_sm')
nlp = spacy.load('en_core_web_sm')
text = "ChatGPT Prompts Tell a joke Say a riddle Make a crochet pattern of a sweater for a cat"
print(text)

example = nlp(text)
print(example)

for token in example:
    print(token.text, "****", token.pos_,"   ", token.pos)
