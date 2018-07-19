from nltk.stem.snowball import  GermanStemmer
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def stem_rawtext(txt):
    stemmer=GermanStemmer()
    return stemmer.stem(txt)

def stem_train():
    stem_data=[]
    with open('rawtext_labeled','rb') as f:
        data=pickle.load(f)
    for text,label in data:
        txt=re.sub(r'\n','',text)
        txt = re.sub(r'\r', '', txt)
        #txt=stem_rawtext(txt)
        print(txt+'___'+label)
        stem_data.append((txt,label))
    print(len(data))
    save_data(stem_data,'cleaned_raw_labeled')
    return stem_data


def token(txt):
    tok_txt=word_tokenize(txt)
    return tok_txt

def save_data(data,fileName):
    with open(fileName, 'wb') as f:
        pickle.dump(data, f)
    f.close()
    print(len(data))

def tokenize_data(data_list):
    tokenized_labeled = []
    for text, label in data_list:
        temp = (token(text), label)
        tokenized_labeled.append(temp)
        print(temp)
    save_data(tokenized_labeled,'list_token_labeled')



def check_saved_tok(fileName):
    with open(fileName, 'rb') as f:
        read = pickle.load(f)
    f.close()
    print(read[:4])

stem_train()

check_saved_tok('cleaned_raw_labeled')