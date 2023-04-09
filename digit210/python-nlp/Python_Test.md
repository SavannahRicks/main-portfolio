# My Python Test Documentation
Ok so right now the only output I was able to get is from the code's run output and the text I have from distTrained-ORG-LOC-GPE-NORP.txt. But I still have an idea on how the code works, so I'll explain what I have and what I think the issues are. 

1. As shown below, this block of code is made to add spacy, regex and PySaxonProcessor into the python file and the nlp is set to be able to load in and process large files.
```
import os
import spacy
from spacy.pipeline import EntityRuler
import re as regex
from saxonche import PySaxonProcessor

nlp = spacy.load('en_core_web_lg')
```

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
Here we make sure that everything we're about to process is going through the necessary filters in the correct order. So we first declare all the filters to `config`, then in `ruler` we make a new pipe to sort the order of them.
