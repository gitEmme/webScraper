from textblob_de import TextBlobDE

import pymongo

client=pymongo.MongoClient('localhost')


def blob_classify(text,id):
    blob=TextBlobDE(text)
    client.spiegel.wirtschaft.update({'_id': id}, {"$set": {'blobPolarity': float(blob.sentiment.polarity)}})
    print(blob.sentiment.polarity)

for comment in client.spiegel.wirtschaft.find():
    blob_classify(comment['body'],comment['_id'])