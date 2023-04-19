
import os
import spacy
from spacy.pipeline import EntityRuler
import re as regex
from saxonche import PySaxonProcessor

nlp = spacy.load('en_core_web_lg')


workingDir = os.getcwd()
print('current working directory: ' + workingDir)
insideDir = os.listdir(workingDir)
print('inside workingDir is: ' + str(insideDir))

CollPath = os.path.join(workingDir, 'bojack-files')
print('CollPath is: ' + str(CollPath))
TargetPath = os.path.join(workingDir,'bojack-output')

#########################################################################################
# ebb: After reading the sorted dictionary output, we know spaCy is making some mistakes.
# So, here let's try adding an EntityRuler to customize spaCy's classification. We need
# to configure this BEFORE we send the tokens off to nlp() for processing.
##########################################################################################

config = {"spans_key": None, "annotate_ents": True, "overwrite": True, "validate": True}
ruler = nlp.add_pipe("span_ruler", before="ner", config=config)
patterns = [

    {"label": "PERSON", "pattern": "Peanutbutter and"},
    {"label": "PERSON", "pattern": "Peanutbutter"},
    {"label": "NULL", "pattern": "��♪ BoJack �"},
    {"label": "NULL", "pattern": "TV Guide"},
    {"label": "TIME", "pattern": "sec"},
    {"label": "NULL", "pattern": "TV][cell"},
    # {"label": "GPE", "pattern": "Bree"},
    # {"label": "LOC", "pattern": "Middle-earth"},
    # {"label": "GPE", "pattern": "Minas Tirith"},
    # {"label": "LOC", "pattern": "the Misty Mountains"},
    # {"label": "LOC", "pattern": "Rauros"},
    # {"label": "GPE", "pattern": "Rohan"},
    # {"label": "GPE", "pattern": "Gondor"},

    #
    # {"label": "PERSON", "pattern": "Gandalf"},
    # {"label": "PERSON", "pattern": [{"TEXT" : {"REGEX": "Meriadoc( Brandybuck)?"}}]},
    # {"label": "PERSON", "pattern": [{"TEXT" : {"REGEX": "Peregrin( Took)?"}}]},
    # {"label": "PERSON", "pattern": "Rose"},

    {"label": "NULL", "pattern": "TV]�"},
    {"label": "NULL", "pattern": "ding]Todd"},
    {"label": "NULL", "pattern": "music]�"},
    {"label": "NULL", "pattern": "music]♪ ♪♪ Back"},
    {"label": "NULL", "pattern": ".[grunting]Wait"},
    {"label": "NULL", "pattern": "��♪ ♪�"},
    {"label": "NULL", "pattern": "���"},
    {"label": "NULL", "pattern": "Spanish][laughter][cheering][laughter]Señor Horseman"}
]
ruler.add_patterns(patterns)

# 3. Here, the function imports each individual file, one at a time
# (received from the for-loop below.
def readTextFiles(filepath):
    # with open(filepath, 'r', encoding='utf8') as f:
    with PySaxonProcessor(license=False) as proc:
        xml = open(filepath, encoding='utf-8').read()
        # ebb: Here we changed to the Saxon processor to read files with XPath.
        # From here on, we change how we formulate the string that Python will send to NLP.
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=xml)
        xp.set_context(xdm_item=node)

        xpath = xp.evaluate('//script//line ! normalize-space() => string-join()')
        # ebb: Let's get the string() value of all the <p> elements that are descendants of <book>.
        # The XPath function normalize-space() gets the string value and removes extra spaces.
        # That way we avoid the prologue, preface material.
        # I'm sending the whole thing to string-join() to bundle it together as one string
        # instead of a new string for every <p> element.
        # string = xpath.__str__()
        string = str(xpath)
        cleanedUp = regex.sub(r"_", r" ", string)
        cleanedUp = regex.sub(r"'([A-Z])]", r" \1", cleanedUp)
        cleanedUp = regex.sub(r"([.!?;'`])([A-Z'`]])", r"\1 \2", cleanedUp)
        tokens = nlp(cleanedUp)

        dictEntities = entitycollector(tokens)  # sends to entitycollector function
        print(f"{dictEntities=}" + " ----------- did this print? #2")
        return(dictEntities)

def entitycollector(tokens):
    entities = {}
    for ent in sorted(tokens.ents):
        if ent.label_ == "LOC" or ent.label_=="FAC" or ent.label_=="ORG" or ent.label_=="GPE" or ent.label_=="NORP":
            if not regex.match(r"\w*[.,!?;:']\w*", ent.text):
                entities[ent.text] = ent.label_
    print(f"{entities=}" + " ----------- DID THIS PRINT #1")
    return entities

def assembleAllNames(CollPath):
    AllNames = {}
    for file in os.listdir(CollPath):
        if file.endswith(".xml"):
            filepath = f"{CollPath}/{file}"

            eachFileDict = readTextFiles(filepath)  # sends to readTextFiles
            print(f"{eachFileDict=}" + " ----------- Did this print #3")
            AllNames.update(eachFileDict)
            # ebb: The line above adds each file's new NLP data to the dictionary.

    print(f"{AllNames=}")
    AllNamesKeys = list(AllNames.keys())
    AllNamesKeys.sort()
    SortedDict =  {i: AllNames[i] for i in AllNamesKeys}
    print(f"{SortedDict=}")
    writeSortedEntries(SortedDict) # sends to writeSortedEntries

    for file in os.listdir(CollPath):
        if file.endswith(".xml"):
            sourcePath = f"{CollPath}/{file}"
            eachFileData = xmlTagger(sourcePath, SortedDict) # sends down to function xmlTagger function
            print("did this print #4")
    return eachFileData

def writeSortedEntries(dictionary):
    with open('distTrained-ORG-LOC-GPE-NORP.txt', 'w') as f:
        for key, value in dictionary.items():
            f.write(key + ' : ' + value + '\n  did this print too? #5 --- ')
def xmlTagger(sourcePath, SortedDict):
    with open(sourcePath, 'r', encoding='utf8') as f:
        readFile = f.read()
        stringFile = str(readFile)

        # ebb: Get the current filename. We need to know it to write its new output version
        filename = os.path.basename(f.name)
        print(f"{filename=}")
        targetFile = f"{TargetPath}/{filename}"
        print(f"{targetFile=}"+" ------- did this print? #6")

        # ebb: Work with stringFile variable to look for matches from the distinctNames set.
        for key, val in SortedDict.items():
            replacement = '<name type="' + val + '">' + key + '</name>'
            # print(f"{replacement=}")
            stringFile = stringFile.replace(key, replacement)
            # print(f"{stringFile=}")      ########   WORKING ##

        with open(targetFile, 'w') as f:
            f.write(stringFile)

assembleAllNames(CollPath)

# ebb: The functions are all initiated here now.
# This just delivers the collection path up to the first function in the sequence.