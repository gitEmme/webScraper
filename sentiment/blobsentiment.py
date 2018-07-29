from textblob_de import TextBlobDE

import pymongo
import pprint
client=pymongo.MongoClient('localhost')


def blob_classify(text,id,collection):
    blob=TextBlobDE(text)
    client.spiegel[collection].update({'_id': id}, {"$set": {'blobPolarity': float(blob.sentiment.polarity)}})
    print(blob.sentiment.polarity)

def classify_collection(collection):
    for comment in client.spiegel[collection].find({'blobPolarity':None}):
        print(type(comment['body']))
        blob_classify(comment['body'],comment['_id'],collection)


classify_collection('wissenschaft')

def blob_classify_all():
    lista = [
        'auto',
        'gesundheit',
        'karriere',
        'kultur',
        'lebenundlernen',
        'netzwelt',
        'panorama',
        'politik',
        'reise',
        'sport',
        'wirtschaft',
        'wissenschaft'
    ]
    for collection in lista:
        classify_collection(collection)
