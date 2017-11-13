import pickle
import re

from nltk import word_tokenize

from germalemma import GermaLemma #works only if file in same folder as data ClassifierBasedGermanTagger , nltk_german_classifier_data.pickle and germalemma.py

def lemmatizer_funct(text):
    tokens = word_tokenize(text, language="german")
    lemmatizer = GermaLemma()
    with open('nltk_german_classifier_data.pickle', 'rb') as f:
        tagger = pickle.load(f)
    tag_token = tagger.tag(tokens)
    found_list = []
    for val in tag_token:
        # to filter for tags supported by germalemma
        if re.match('N|V|(ADJ)|(ADV)', val[1]) != None:
            found_list.append(val)
    lemma_result = []
    for val in found_list:
        lemma = lemmatizer.find_lemma(val[0], val[1])
        lemma_result.append(lemma)

    return lemma_result