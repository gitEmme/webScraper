import csv
import codecs

list=[]

with codecs.open('annotated_posts_v2.csv','r',encoding='utf-8',errors='ignore') as f: #
    r=csv.reader(f,delimiter=';')
    for row in r:
        temp=[row[0],row[2],row[4],row[5]] #row[3],row[2],
        list.append(temp)
    print(list[1:10])
    list=[item for item in list if (item[2]in {'SentimentNeutral','SentimentNegative','SentimentPositive'} and item[3]=='1')]
    print(list[:10])
    dict = {}

    for item in list:
        if(item[0] not in dict.keys()):
            p,n,neg=0,0,0
            if item[1]=='SentimentNeutral':
                n+=1
            elif item[1]=='SentimentPositive':
                p+=1
            else :
                neg+=1
            tuple=(item[1],p,n,neg)
            dict[item[0]]=tuple
        else:
            p,n,neg=dict[item[0]][1],dict[item[0]][2],dict[item[0]][3]
            if item[1]=='SentimentNeutral':
                n+=1
            elif item[1]=='SentimentPositive':
                p+=1
            else :
                neg+=1
            tuple=(item[1],p,n,neg)
            dict[item[0]] = tuple

    print(dict)
