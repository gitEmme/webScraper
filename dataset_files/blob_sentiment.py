from textblob_de import TextBlobDE
from textblob_de.classifiers import NaiveBayesClassifier
import pickle

with open('raw_num_labeled', 'rb') as fs:
    training_list = pickle.load(fs)
cl=NaiveBayesClassifier(training_list[:3000])
#cl.classify('das ist echt toll')
print(cl.classify('das ist echt toll'))
blob=TextBlobDE("Das ist super schade. Das tut mir so leid.")

for s in blob.sentences:
    print(s)
    print(cl.classify(s))
print(cl.accuracy(training_list[3000:]))
