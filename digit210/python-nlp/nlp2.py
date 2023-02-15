import spacy
# nlp = spacy.cli.download("en_core_web_md")
nlp = spacy.load('en_core_web_md')
import os
workingDir = os.getcwd()
print("current working directory: " + workingDir)    # python-nlp is a directory

insideDir = os.listdir(workingDir)
print("inside this directory are the following files AND directories: " + str(insideDir))


def readTextFiles(filepath):    # readTextFiles can be named anthing
    with open(filepath, 'r', encoding='utf8') as f:
        readFile = f.read()
        stringFile = str(readFile)
        # print(stringFile)

        tokens = nlp(stringFile)

        vectors = tokens.vector_norm
        print(vectors)
        print(tokens)



for file in os.listdir(workingDir):
    if file.endswith(".txt"):
        filepath = f"{workingDir}\{file}"
        print(filepath)
        readTextFiles(filepath)
    else: print("Not a txt file")

