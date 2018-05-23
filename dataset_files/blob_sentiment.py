import textblob_de
from textblob_de import TextBlobDE
from textblob_de.classifiers import NaiveBayesClassifier
import pickle

from textblob_de import TextBlobDE
from textblob_de.classifiers import NaiveBayesClassifier
import pickle

with open('rawtext_labeled', 'rb') as fs:
    training_list = pickle.load(fs)
cl=NaiveBayesClassifier(training_list[:500])
cl.classify('das ist echt toll')
blob=TextBlobDE("Das ist super schade. Das tut mir so leid.")

for s in blob.sentences:
    print(s)
    print(cl.classify(s))
print(cl.accuracy(training_list[:1000]))
