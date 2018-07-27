import pymongo
import re
import pprint
client=pymongo.MongoClient('localhost')
from googletrans import Translator
#print(client.list_database_names())

def translator_func(txt):
    translator=Translator()
    transtxt=translator.translate(txt,src='de',dest='en').text
    pprint.pprint(transtxt)
    return transtxt

def count_all_data_in_db():
    total=0
    topic_count_map={
    'auto':0,
    'gesundheit':0,
    'karriere':0,
    'kultur':0,
    'lebenundlernen':0,
    'netzwelt':0,
    'panorama':0,
    'politik':0,
    'reise':0,
    'sport':0,
    'wirtschaft':0,
    'wissenschaft':0,}
    for key in topic_count_map.keys():
        print('Counting comments in collection:  '+key)
        for comment in client.spiegel[key].find():
            topic_count_map[key]+=1
        print('Total:  '+ str(topic_count_map[key]))
        total+=topic_count_map[key]
    pprint.pprint(topic_count_map)
    print('Total  :'+str(total))

#count_all_data_in_db()

def count_mentioned(word1,word2,word3,collection):
    count = 0
    for comment in client.spiegel[collection].find():
        if re.match(word1,comment['body']) or re.match(word2,comment['body']) or re.match(word3,comment['body']):
            count+=1
            #pprint.pprint(comment['body'])
    return count
"""
print(count_mentioned(r'audi',r'Audi',r'AUDI','auto'))
print(count_mentioned(r'bmw',r'Bmw',r'BMW','auto'))
print(count_mentioned(r'Ferrari',r'ferrari',r'FERRARI','auto'))
print(count_mentioned(r'Volkswagen',r'Vw',r'VW','auto'))

print('Merkel '+str(count_mentioned(r'Merkel',r'merkel',r'MERKEL','politik')))
print('Trump '+str(count_mentioned(r'Trump',r'Trump',r'TRUMP','politik')))
print('Berlusconi '+str(count_mentioned(r'Berlusconi',r'berlusconi',r'BERLUSCONI','politik')))
print('Macron '+str(count_mentioned(r'Macron',r'macron',r'MACRON','politik')))
print('Renzi '+str(count_mentioned(r'Renzi',r'renzi',r'RENZI','politik')))
print('Mattarella '+str(count_mentioned(r'Mattarella',r'mattarella',r'MATTARELLA','politik')))
"""
def in_process_sentiment(collection,num):
    count=0
    count_missing=0
    for c in client.spiegel[collection].find({'sentiment'+num : {'$nin' : ['positive','negative','neutral']}},no_cursor_timeout=True):
        count+=1
    print(count)
    for c in client.spiegel[collection].find({'sentiment'+num : None},no_cursor_timeout=True):
        count_missing+=1
    print(count_missing)


def sentiment3(collection):
    pos = 0
    neu = 0
    neg = 0
    for c in client.spiegel[collection].find(no_cursor_timeout=True):
        if c['sentiment3']=='negative':
            neg+=1
        elif c['sentiment3']=='neutral':
            neu+=1
        else:
            pos+=1
    res=[pos,neu,neg]
    print(res)
    return res

def sentiment(collection):
    pos = 0
    neu = 0
    neg = 0
    for c in client.spiegel[collection].find(no_cursor_timeout=True):
        if c['sentiment']=='negative':
            neg+=1
        elif c['sentiment']=='neutral':
            neu+=1
        else:
            pos+=1
    res=[pos,neu,neg]
    print(res)
    return res



#sentiment3('politik')

#in_process_sentiment('reise','')

def find_sentiment(collection,num,sentiment):
    for c in client.spiegel[collection].find({'sentiment'+num: sentiment},no_cursor_timeout=True):
        pprint.pprint(c)
        translator_func(c['body'])


find_sentiment('reise','','negative')