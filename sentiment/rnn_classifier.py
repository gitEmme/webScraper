#import pymongo
from rnn.classifier import classify

#client=pymongo.MongoClient('localhost')

#print(client.list_database_names())


def classify_all():
    for item in [
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
        ]:
        print(item)
        classify(item)


classify_all()