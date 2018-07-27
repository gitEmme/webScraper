from tensorflow.python.keras.preprocessing.text import Tokenizer
import pickle
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
import gc
import tensorflow as tf
import pymongo

client=pymongo.MongoClient('localhost')

print(client.list_database_names())

def max_value(a,b,c):
    m=float(0)
    if a>=b:
        if c>=a:
            m=c
        else:
            m=a
    else:
        if c>=b:
            m=c
        else:
            m=b
    return m

def classify(collection):
    model=tf.keras.models.load_model(
        'zugsoftmodel.hdf5',
        custom_objects=None,
        compile=True
    )
    with open('alldata','rb') as f:
        data=pickle.load(f)
    f.close()
    dataset=[]
    for txt in data:
        dataset.append(txt)
    tokenizer=Tokenizer(num_words=None)
    tokenizer.fit_on_texts(dataset)
    for comment in client.spiegel[collection].find({'sentiment3': {'$nin' : ['positive','negative','neutral']}},no_cursor_timeout=True):
        texts = []
        texts.append(comment['body'])
        tokens = tokenizer.texts_to_sequences(texts)
        pad='pre'
        max_tokens=85
        tokens_pad = pad_sequences(tokens, maxlen=max_tokens,padding=pad, truncating=pad)
        res = model.predict(tokens_pad)[0]
        p = float(res[0])
        neu = float(res[1])
        neg = float(res[2])
        maximum = max_value(p, neu, neg)
        if maximum == p:
            sentiment = 'positive'
        elif maximum == neu:
            sentiment = 'neutral'
        else:
            sentiment = 'negative'

        client.spiegel[collection].update({'_id': comment['_id']}, {"$set": {'sentiment3': sentiment}}, upsert=True)
        client.spiegel[collection].update({'_id': comment['_id']}, {"$set": {'sentimentSoftZug': [p, neu, neg]}}, upsert=True)
        #print(sentiment)
        #print(res)
    gc.collect()

#classify('kultur')

for item in [
    #'auto',
    'gesundheit',
    'karriere',
    #'kultur',
    'lebenundlernen',
    'netzwelt',
    'panorama',
    #'politik',
    #'reise',
    'sport',
    'wirtschaft',
    'wissenschaft'
    ]:
    print(item)
    classify(item)