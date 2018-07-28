from textblob_de import TextBlobDE
from textblob_de.classifiers import NaiveBayesClassifier
import pickle

def build_naive():
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


def count_labeled_dataset(fileName):
    with open(fileName, 'rb') as fs:
        read = pickle.load(fs)
    fs.close()
    p=0
    neg=0
    neu=0
    count=0
    for text, label in read:
        count+=1
        if(label==1):
            neu+=1
        if(label==2):
            neg+=1
        if(label==0):
            p+=1

    print('p '+str(p))
    print('neg '+str(neg))
    print('neu '+str(neu))

    print('tot '+str(count))


#count_labeled_dataset('raw_num_labeled')
count_labeled_dataset('train_v1.4relabeled_num')