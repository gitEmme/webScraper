import pymongo
import pprint
import timeit
import pickle
from translate_to_english import translator_func
import codecs
import csv

client=pymongo.MongoClient('172.17.0.2')

def open_import_data():
    db=client.spiegel
    file_list = ['comments/politik_', 'comments/wirtschaft_'
        , 'comments/panorama_', 'comments/sport_'
        , 'comments/kultur_', 'comments/netzwelt_'
        , 'comments/wissenschaft_', 'comments/gesundheit_'
        , 'comments/lebenundlernen_', 'comments/karriere_'
        , 'comments/reise_', 'comments/auto_']
    for i in file_list:
        if (i == 'comments/karriere_'):
            max = 19
        elif (i == 'comments/auto_'):
            max = 29
        elif (i == 'comments/wissenschaft_'):
            max = 24
        elif (i == 'comments/gesundheit_'):
            max = 23
        elif (i == 'comments/lebenundlernen_'):
            max = 30
        else:
            max = 31
        for j in range(1, max):
            file=open_file(i,j)
            start = timeit.default_timer()
            if(i=='comments/politik_'):
               spiegel_collection=db.politik
               spiegel_collection.insert_many(file)
            elif(i=='comments/wirtschaft_'):
                spiegel_collection = db.wirtschaft
                spiegel_collection.insert_many(file)
            elif(i=='comments/panorama_'):
                spiegel_collection = db.panorama
                spiegel_collection.insert_many(file)
            elif(i=='comments/sport_'):
                spiegel_collection = db.sport
                spiegel_collection.insert_many(file)
            elif(i=='comments/kultur_'):
                spiegel_collection = db.kultur
                spiegel_collection.insert_many(file)
            elif (i=='comments/netzwelt_'):
                spiegel_collection = db.netzwelt
                spiegel_collection.insert_many(file)
            elif (i=='comments/wissenschaft_'):
                spiegel_collection = db.wissenschaft
                spiegel_collection.insert_many(file)
            elif (i=='comments/gesundheit_'):
                spiegel_collection = db.gesundheit
                spiegel_collection.insert_many(file)
            elif (i=='comments/lebenundlernen_'):
                spiegel_collection = db.lebenundlernen
                spiegel_collection.insert_many(file)
            elif (i=='comments/karriere_'):
                spiegel_collection = db.karriere
                spiegel_collection.insert_many(file)
            elif (i=='comments/reise_'):
                spiegel_collection = db.reise
                spiegel_collection.insert_many(file)
            else:
                spiegel_collection = db.auto
                spiegel_collection.insert_many(file)
            stop = timeit.default_timer()
            print('Running time for import : ' + str(stop - start))
            print(spiegel_collection)


def open_file(i,j):
    print('opening '+i+str(j))
    with open(i + str(j), 'rb') as fp:
        data = pickle.load(fp)
    fp.close()
    return data

def delete_db():
    client.drop_database('spiegel')

def look_for_word(mentioned_word,sentiment):
    count=0
    count_p=0
    mentioned=[]
    found=client.spiegel.politik.find()
    for c in found:
        count_p=count_p+1
        if(mentioned_word in c['body']):
            #print(c['body'])
            count=count+1
            #t=[c['body'],translator_func(c['body']),sentiment]
            #mentioned.append(t)
    print(mentioned_word+' '+str(count)+' times')
    #print('total politik ' + str(count_p))
    return mentioned
#delete_db()
#open_import_data()

#look_for_word('Merkel')
#look_for_word('Trump')
#look_for_word('Putin')
#res=look_for_word('dumm','negative')
#look_for_word('Berlusconi')
#look_for_word('nicht gut','negative')

#look_for_word('falsch','negative')
#res=look_for_word('finde gut','positive')   #only 14 comments but they look quite positive!
#res=look_for_word('fantastisch','positive') #only 100 comments
#res=look_for_word('tolle idee','positive') #only 1
#res=look_for_word('toll','positive')  #4263 comments
res=look_for_word('witzig','positive')  #859 comments
for t in res:
    pprint.pprint(t)
"""
with open('schädlich','wb') as f:
    pickle.dump(res,f)#f.close()

with open('schädlich','rb') as f :
    read=pickle.load(f)
f.close()
print(read[:3])

with open("schädlich.csv",'w') as resultFile:
    wr = csv.writer(resultFile, delimiter='\t')
    wr.writerows(read)
"""


