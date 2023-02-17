
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
import gensim.corpora as corpora
from gensim.models import LdaModel
from gensim.models import Phrases
import pyLDAvis.gensim_models
import os


stop_words = stopwords.words('english')

print(f"{stop_words=}")

print(f"{string.punctuation=}")


newStopWords = ["said", "one", "go", "went", "came", "like", "one", "dont"]
stop_words.extend(newStopWords)
print("UPDATED: " + f"{stop_words=}")

workingDir = os.getcwd()
print("current working directory: " + workingDir)
srr_chatGPTPath = os.path.join(workingDir, 'srr-texts')
print(srr_chatGPTPath)


def clean_doc(doc):
    text = open(doc, encoding='utf-8').read()
    no_punct = ''
    for c in text:
        if c not in string.punctuation:
            no_punct = no_punct + c


    words = no_punct.lower().split()

    final_words = []
    for word in words:
        if word not in stop_words:
            final_words.append(word)

    # with list comprehension
    # final_words = [word for word in words if word not in stop_words]
    return final_words

# ebb: This controls our file handling as a for loop over the directory:
allDocs = []
for file in os.listdir(srr_chatGPTPath):
    if file.endswith(".txt"):
        filepath = f"{srr_chatGPTPath}\{file}"
        # print(filepath)
        allDocs.append(filepath)
        # clean_doc(filepath)
print(allDocs)

cleaned_docs = [clean_doc(doc) for doc in allDocs]
# Add bigrams and trigrams to docs (only ones that appear 20 times or more).
print(cleaned_docs)
bigram = Phrases(cleaned_docs, min_count=20)
for idx in range(len(cleaned_docs)):
    for token in bigram[cleaned_docs[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            cleaned_docs[idx].append(token)

print(cleaned_docs)

# ebb: We used this code to help us locate buggy text files. It will stop on files that can't be processed due to weird non-Unicode characters.
# cleaned_docs = []
# for doc in allDocs:
#     print("This doc is going to the cleaners: " + f"{doc=}")
#     clean_doc(doc)
id2word = corpora.Dictionary(cleaned_docs)

# print(id2word[260])
corpus = [id2word.doc2bow(cleaned_doc) for cleaned_doc in cleaned_docs]
print(corpus)

lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=10)
# Suggestion: Try 10 - 50 topics and vary in 5s
topics = lda_model.get_document_topics(corpus)
print(f"{len(topics)=}")
# ebb: len(topics) appears to be the number of documents. There are
# 209 documents in the Grimm collection.
print(f"{topics[2]=}")

sorted_topics = sorted(topics[2], key=lambda x: x[1], reverse=True)

print(f"{sorted_topics=}")

for topic in topics[2][:10]:
    print(f"{topic=}")
    terms = lda_model.get_topic_terms(topic[0], 15)
    for num in terms:
        num = num[0]
        print(num, id2word[num])
    print()

vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
pyLDAvis.save_html(vis, 'topicModel_Visualization.html')