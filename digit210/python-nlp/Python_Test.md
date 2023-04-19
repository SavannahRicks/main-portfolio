# My Python Test Documentation
Ok so right now the only output I was able to get is from the code's run output and the text I have from distTrained-ORG-LOC-GPE-NORP.txt. But I still have an idea on how the code works, so I'll explain what I have and what I think the issues are. 

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. As shown below, this block of code is made to add spacy, regex and PySaxonProcessor into the python file and the nlp is set to be able to load in and process large files.
```
import os
import spacy
from spacy.pipeline import EntityRuler
import re as regex
from saxonche import PySaxonProcessor

nlp = spacy.load('en_core_web_lg')
```
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
2. 
```
workingDir = os.getcwd()
print('current working directory: ' + workingDir)
insideDir = os.listdir(workingDir)
print('inside workingDir is: ' + str(insideDir))

CollPath = os.path.join(workingDir, 'bojack-files')
print('CollPath is: ' + str(CollPath))
TargetPath = 'bojack-output'
```
Here, we get the current filepath to our python file and label it `workingDir`. Then we label whats inside `workingDir` and call it `insideDir`. Then `CollPath` takes `workingDir` and extends it by adding 'bojack-files' to the end of it. Now we set a new destination for our output by making `TargetPath` to the empty file bojack-output.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------

3.
```
config = {"spans_key": None, "annotate_ents": True, "overwrite": True, "validate": True}
ruler = nlp.add_pipe("span_ruler", before="ner", config=config)
patterns = [

    {"label": "PERSON", "pattern": "Peanutbutter and"},
    {"label": "PERSON", "pattern": "Peanutbutter"},
    {"label": "NULL", "pattern": "��♪ BoJack �"},
    {"label": "NULL", "pattern": "TV Guide"},
    {"label": "TIME", "pattern": "sec"},
    {"label": "NULL", "pattern": "TV][cell"},
```
Here we make sure that everything we're about to process is going through the necessary filters in the correct order. So we first declare all the filters to `config`, then in `ruler` we make a new pipe to sort the order of them. Inside of `patterns` are specific patterns that I've noticed were incorrect when running the python, so I rewrite them manually to correct them. One problem I've noticed while doing this is that when fixing the special musical characters, it doesn't actually redifine them. I also noticed that if I use a label that isn't GPE, LOC, or ORG, the entity will completely disappear insead of with a better label.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
4.
`assembleAllNames(CollPath)` is the the first indicator to start the tagging procress. This call will send `CollPath` to the function `assembleAllNames`

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
5.
```
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
```
This funtion will first look for all the files in the `CollPath` that are xml, and send those to the `readTextFiles` function. After those files have been run through `readTextFiles`, it will be placed into the list `AllNames`. After all files have successfully been through `readTextFiles` and placed in `AllNames`, each key will be placed in the variable `AllNamesKeys`, then sorted, then paired with their rightful file. The list of pairs will be sent off to the function `writeSortedEntries`. Next, we're gonna look at all the xml files from `CollPath` again and send the files to `xmlTagger` function with all the pairs, aka `SortedDict` to finally get tagged and outputed. 

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
6.
```
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
```
From within the `readTextFiles` function, each xml file is imorted, opened and read. We also make sure to read each file using PySaxonProcessor, in order to use XPath. Not gonna lie, variables `xp` and `naode` confuse me, but variable `xpath`, we take those values and evaluate each file using XPath. We then take that result (`xpath`) and make it into a string in order to use regex to clean up the text. The cleaned text is then using nlp to tokenize it (`tokens`). Those tokens will now be sent to the function `entitycollectoer`. Afterwords, they will be placed in variable `dictEntities` and returned back into it's called function inside of `assembleAllNames`.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
7.
```
def entitycollector(tokens):
    entities = {}
    for ent in sorted(tokens.ents):
        if ent.label_ == "LOC" or ent.label_=="FAC" or ent.label_=="ORG" or ent.label_=="GPE" or ent.label_=="NORP":
            if not regex.match(r"\w*[.,!?;:']\w*", ent.text):
                entities[ent.text] = ent.label_
    print(f"{entities=}" + " ----------- DID THIS PRINT #1")
    return entities
```
Inside of `entityCollector` we have imported tokens from `readTextFiles`. Then for each entity found in tokens that has the specified labels of LOC, FAC, ORG, GPE, or NORP and does not match a specific regex rule, it will be placed in the list `entities`. Then that filtered list will be returned back to where `entitycollector` is originally called in `readTextFiles`.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
8.

```
def writeSortedEntries(dictionary):
    with open('distTrained-ORG-LOC-GPE-NORP.txt', 'w') as f:
        for key, value in dictionary.items():
            f.write(key + ' : ' + value + '\n  did this print too? #5 --- ')
```
`writeSortedEntries` function has been called from the `assembleAllNames` function with the variable `SortedDict` (a list of entities and their labels). In this function, it opens a new document to write in. Then each `key` and `val` from SortedDict is written in pairs inide of this new file. This function doesn't return anything back to `assembleAllNames`, so `assembleAllNames` will continue.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
9.
```
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
```
`xmlTagger` function is orriginally called from the `assembleAllNames` function with importing individual xml files (`sourcePath`) and nlp entities with their labels (`SortedDict`). The function first opens the file inported to read and make it a string. Then takes the name of the file and labels it `filename` and takes `TargetPath` from #2 of this Documentation and created a copy of the original `filename` but inside of `TargetPath`. Next we take `key` and `val` from `SortedDict` and place them in a manually crafted string that includes xml tagging and call that `replacemant`. That special string will then take the spot of the original text from the open file. Since this open file has been changed, we don't wanna save the output over the original, so then we open the blank copy file with a different uri (`targetFile`), and write the new virsion in it (`stringFile`).
