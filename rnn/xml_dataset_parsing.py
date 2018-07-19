import pprint
import re
import pickle
from bs4 import BeautifulSoup

def fromXmlToTupleList(filename):
    infile = open(filename+'.xml',"r")
    contents = infile.read()
    soup = BeautifulSoup(contents,'xml')
    documents = soup.find_all('Document')
    dataset=[]
    for doc in documents:
        #pprint.pprint(doc)
        soup=BeautifulSoup(str(doc),'xml')
        sentiment=soup.find('sentiment')
        text=soup.find('text')
        text=re.findall(r'<text>(.*)</text>',str(text))
        sentiment=re.findall(r'<sentiment>(.*)</sentiment>', str(sentiment))
        text=re.sub('\"','',text[0])
        print(sentiment)
        print(text)
        dataset.append((text,sentiment[0]))
    with open(filename,'wb') as f:
        pickle.dump(dataset,f)
    f.close()

#fromXmlToTupleList('train_v1.4')

def openSaved(filename):
    with open(filename,'rb') as f:
        read=pickle.load(f)
    f.close()
    pprint.pprint(read[:5])
    print(len(read))

openSaved('train_v1.4')

""" ok it works: re.find return text sentiment couple for each document in xml"""




