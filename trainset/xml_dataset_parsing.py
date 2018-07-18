import pprint
import re

from bs4 import BeautifulSoup
infile = open("dev_v1.4.xml","r")
contents = infile.read()
soup = BeautifulSoup(contents,'xml')
documents = soup.find_all('Document')
dataset=[]
for doc in documents:
    pprint.pprint(doc)
    soup=BeautifulSoup(str(doc),'xml')
    sentiment=soup.find('sentiment')
    text=soup.find('text')
    text=re.findall(r'<text>(.*)</text>',str(text))
    sentiment=re.findall(r'<sentiment>(.*)</sentiment>', str(sentiment))
    print(sentiment)
    print(text)

""" ok it works: re.find return text sentiment couple for each document in xml"""




