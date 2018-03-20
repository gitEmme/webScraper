import requests
from bs4 import BeautifulSoup
import re
import csv
import pickle


################# urls ############################
site='http://www.spiegel.de'
forum='http://www.spiegel.de/forum/'
site_themen='http://www.spiegel.de/thema/index-a.html'
##################### unused urls to cancel ##################################
map={}
map['politik']='http://www.spiegel.de/politik/'
map['meinung']='http://www.spiegel.de/thema/meinung/'
map['witschaft']='http://www.spiegel.de/wirtschaft/'
map['panorama']='http://www.spiegel.de/panorama/'
map['sport']='http://www.spiegel.de/sport/'
map['kultur']='http://www.spiegel.de/kultur/'
map['netzwelt']='http://www.spiegel.de/netzwelt/'
map['wissenschaft']='http://www.spiegel.de/wissenschaft/'
map['einestages']='http://www.spiegel.de/einestages/'
map['gesundheit']='http://www.spiegel.de/gesundheit/'
map['karriere']='http://www.spiegel.de/karriere/'
map['lebenundlernen']='http://www.spiegel.de/lebenundlernen/'
map['bento']='http://www.spiegel.de/bento/'
map['reise']='http://www.spiegel.de/reise/'
map['auto']='http://www.spiegel.de/auto/'
map['stil']='http://www.spiegel.de/stil/'
map['backstage']='http://www.spiegel.de/backstage/'

############################### unused scripts #########################################


def prepare_main(**map):
    for address in map.values():
        main_page=requests.get(address)
        soup=BeautifulSoup(main_page.text,'html.parser')
        res=[]
        for item in soup.find_all(class_='article-title'):
            res.append(str(item))
        links=[]
        for e in res:
            found=re.search(r'(?<=href=").*?(?=")',e) #'href=[\'"]?([^\'" >]+)
            links.append(site+found.group())
        for t in links:
            print(t)

#prepare_main(**map)

def search_next_page(*lista):
    related=[]
    for item in lista:
        related + prepare_single_page(item, 'thread-content')
        temp = prepare_single_page(item, 'page-next')
        while(len(temp)):
            for t in temp:
                related + prepare_single_page(t, 'thread-content')
                temp = prepare_single_page(t, 'page-next')
    return related

#komm=prepare_single_page(forum,'forum-name')  #funct used under
#with open('spiegel_forum_sections', 'wb') as fb:
 #  pickle.dump(komm,fb)
#fb.close()

map_topics={}
map_topics[0]='forum/spiegel_forum_politik'
map_topics[1]='forum/spiegel_forum_wirtschaft'
map_topics[2]='forum/spiegel_forum_panorama'
map_topics[3]='forum/spiegel_forum_sport'
map_topics[4]='forum/spiegel_forum_kultur'
map_topics[5]='forum/spiegel_forum_netzwelt'
map_topics[6]='forum/spiegel_forum_wissenschaft'
map_topics[7]='forum/spiegel_forum_gesundheit'
map_topics[8]='forum/spiegel_forum_karriere'
map_topics[9]='forum/spiegel_forum_lebenundlernen'
map_topics[10]='forum/spiegel_forum_reise'
map_topics[11]='forum/spiegel_forum_auto'
topics={}
#for n in range(0,12):
 #   topics[komm[n]]=map_topics[n]
#print(topics)
#with open('map_topicfilename','wb') as f:
 #   pickle.dump(topics,f)
########################################################################################################

def prepare_single_page(site,address,string):
    main_page = requests.get(address)
    soup = BeautifulSoup(main_page.text, 'html.parser')
    res = []
    for item in soup.find_all(class_=string):
        res.append(str(item))
    links = []
    for e in res:
        found = re.findall(r'(?<=href=").*?(?=")', e)  # 'href=[\'"]?([^\'" >]+)'  or '(?<=href=").*?(?=")'
        for i in found:
            if 'http' not in i:
                links.append(site + i)
            else:
                links.append(i)
    for t in links:
        print(t)
    return links

def search_next_page(url_item):
    related=[]
    for t in prepare_single_page(site,url_item,'thread-content'):
        related.append(t)
    temp = prepare_single_page(site,url_item,'page-next')
    while(len(temp)):
        for t in temp:
            print(type(t))
            for l in prepare_single_page(site,t,'thread-content'):
                related.append(l)
            print(type(related[0]))
        temp = prepare_single_page(site,t,'page-next')
    print(len(related))
    print(type(related[0]))
    return related

def save_links(*lista,**mappa):
 for item in lista:
    all_links=search_next_page(item)
    #with open(mappa[item], 'wb') as fp:
    #    pickle.dump(all_links,fp)
    #fp.close()

with open('spiegel_forum_sections', 'rb') as fb:
    l=pickle.load(fb)
fb.close()
with open('map_topicfilename','rb') as fi:
    m=pickle.load(fi)
fi.close()
save_links(*l,**m)
#all_links=search_next_page(*komm)
#all_links=[]
#for item in komm[8:9]:
#    all_links=search_next_page(item)
 #   with open('spiegel_forum_karriere', 'wb') as fp:
  #      pickle.dump(all_links,fp)
 #   fp.close()

#with open('spiegel_forum_links','rb') as fp:
 #   read=pickle.load(fp)
  #  print(read[:10])