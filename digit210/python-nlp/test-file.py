import spacy
import os


nlp = spacy.load('en_core_web_md')
phrase = "hello"
print(phrase)

example = nlp(phrase)
for token in example:
    print(token.pos_)

# *************************************************************

workingDir = os.getcwd()
print("current working directory: " + workingDir)

# os.listdir lists files and folders inside a path:
insideDir = os.listdir(workingDir)
print("inside this directory are the following files AND directories: " + str(insideDir))

# use os.path.join to connect the subdirectory to the working directory:
# CollPath = os.path.join(workingDir, 'textCollection')
# print(CollPath)

def readTextFiles(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        readFile = f.read()
        # print(readFile)
        stringFile = str(readFile)

        # lengthFile = len(readFile)
        # print(lengthFile)
        tokens = nlp(stringFile)
        # vectors = tokens.vector_norm
        # print(vectors)

        wordOfInterest = nlp(u'panic')
        print(wordOfInterest, ': ', wordOfInterest.vector_norm)


        highSimilarityDict = {}
        for token in tokens:
            if (token and token.vector_norm):

                if wordOfInterest.similarity(token) > .3:
                    highSimilarityDict[token] = wordOfInterest.similarity(token)
                    # The line above creates the structure for each entry in my dictionary.
                    # print(token.text, "IS SIMILAR TO", wordOfInterest, "----->", wordOfInterest.similarity(token))
        # print("This is a dictionary of words most similar to the word " + wordOfInterest.text + " in this file.")

        # print(highSimilarityDict)

        highSimilarityReduced = {}
        for key, value in highSimilarityDict.items():
            if value not in highSimilarityReduced.values():
                highSimilarityReduced[key] = value
        # print(highSimilarityReduced)
        print(len(highSimilarityReduced.items()), " vs ", len(highSimilarityDict.items()))

        print("The values are: ")
        print(highSimilarityReduced.values())


        sortedVals = sorted(highSimilarityReduced.values())
        print ("the sorted vals are: ")
        print(sortedVals)







for file in os.listdir(workingDir): # calls on the function readTextFiles
    if file.endswith(".txt"):
        filepath = f"{workingDir}\{file}"
        print(filepath)
        readTextFiles(filepath)

    # else: print("Not a txt file")