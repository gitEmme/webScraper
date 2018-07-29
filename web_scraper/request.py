import requests
from bs4 import BeautifulSoup
import re
import pickle
import timeit

################# urls UNUSED ############################
forum='http://www.spiegel.de/forum/'
##########################################################

def prepare_single_page(site,address,string):
    start = timeit.default_timer()
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
    stop = timeit.default_timer()
    print(str(stop - start))
    for t in links:
        print(t)
    return links

def search_next_page(url_item): #similar to the click_next function in process_saved_links.py, but here once accessed the Forum section  at 'http://www.spiegel.de/forum/' I look for all links to discussions under a certain section
    site = 'http://www.spiegel.de'
    related=[]
    for t in prepare_single_page(site,url_item,'thread-content'):
        related.append(t)
    temp = prepare_single_page(site,url_item,'page-next')
    while(len(temp)):
        for t in temp:
            #print(type(t))
            for l in prepare_single_page(site,t,'thread-content'):
                related.append(l)
            #print(type(related[0]))
        temp = prepare_single_page(site,t,'page-next')
    print(len(related))
    print(type(related[0]))
    return related

###################### TO USE TO UPDATE FILES OF LINKS LIST FOR FORUM TOPICS ###################################################
###################### links are currently saved in the forum folder into pickle files: they been retrieved on March 19th-20th

def save_links(**map):  #to pass map_topicfilename to retrieve all article links in each forum section and save them in their respective file
    for item in map.keys(): #for each link to forum section s --> they all save in 'map_topicfilename': url:file
        start=timeit.default_timer()
        all_links=search_next_page(item)   #search all links to articles
        stop=timeit.default_timer()
        print(str(stop-start))
        #with open(map[item], 'wb') as fp:   #save them
            #pickle.dump(all_links,fp)
        #fp.close()

def check_saved(file_name):     #to open a saved pickle file and check what is in there
    with open(file_name,'rb') as fp:
        read=pickle.load(fp)
    print(read[:10])
    fp.close()

def saving():
    with open('links/map_topicfilename','rb') as fi:
        m=pickle.load(fi)
        print(m)   #?? use pprint
    fi.close()
    save_links(**m)
    #for t in m.values():
        #check_saved(t)

saving()