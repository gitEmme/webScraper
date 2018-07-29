import pickle
from googletrans import Translator  #to be installed

def translator_func(txt):
    translator=Translator()
    transtxt=translator.translate(txt,src='de',dest='en').text
    print(transtxt)
    return transtxt

def english_body():
    file_list=['comments/politik_','comments/wirtschaft_'
        ,'comments/panorama_','comments/sport_'
        ,'comments/kultur_','comments/netzwelt_'
        ,'comments/wissenschaft_','comments/gesundheit_'
        ,'comments/lebenundlernen_' ,'comments/karriere_'
        ,'comments/reise_','comments/auto_']
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
        if(i=='comments/politik_'):
            for j in range(10,max):
                with open(i+str(j),'rb') as fp:
                    read=pickle.load(fp)
                fp.close()
                temp=[]
                for item in read:
                    body=item['body']
                    body=translator_func(body)
                    item['eng_body']=body
                    temp.append(item)
                    #print(temp)
                print('WRITING ON '+i +str(j))
                with open('comments_eng/'+i+str(j),'wb') as fp:
                    pickle.dump(temp, fp)
                fp.close()
        else:
            for j in range(1,max):
                with open(i+str(j),'rb') as fp:
                    read=pickle.load(fp)
                fp.close()
                temp=[]
                for item in read:
                    body=item['body']
                    body=translator_func(body)
                    item['eng_body']=body
                    temp.append(item)
                    #print(temp)
                print('WRITING ON '+i +str(j))
                with open('comments_eng/'+i+str(j),'wb') as fp:
                    pickle.dump(temp, fp)
                fp.close()

#translator_func("Ich bin gut")
#english_body()     #it takes to long suspended for now