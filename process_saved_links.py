import pickle
import requests
import re
from bs4 import BeautifulSoup


with open('map_topicfilename','rb') as f:
    map=pickle.load(f)
print(type(map))
for k in map.keys():  # check opening of saved links to forum on March 20th
    with open(map[k],'rb') as file:
        lista=pickle.load(file)
        print(lista[:10])

def find_links(site,address,string): #return links present in between a specified html tag (string);
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
    #for t in links:
     #   print(t)
    return links

def click_next(url_item): #this is used together with the find_links function to get the list of links where to take comments under a certain article
    site = 'http://www.spiegel.de'
    related=[]
    related.append(url_item)
    temp = find_links(site,url_item,'page-next')
    while(len(temp)):
        for t in temp:
            if t not in related:
                    related.append(t)
        temp = find_links(site,t,'page-next')
    print(len(related))
    print(related)
    return related


def get_comments_box(address):
    string='postbit clearfix' # name of html class containing each comment in www.spiegel.de
    res = []
    for p in click_next(address):
        main_page = requests.get(p)
        soup = BeautifulSoup(main_page.text, 'html.parser')
        for item in soup.find_all(class_=string):
            res.append(str(item))
        #for t in res:
        #    print(t)
    return res

html_text=get_comments_box(lista[2])
print(lista[2])
print(len(html_text))
print(html_text[0])

postid=re.findall(r'id="(postbit.*)">',html_text[0]) #this way the postid is returned inside a list
print(postid)
#print(type(postid[0])) #the object inside the list is a string though :) --> study better regex !!!!
member_ref=re.findall(r'(/forum/member.*)">',html_text[0])
print(member_ref)
member_nick=re.findall(r'<b>(.*)</b>',html_text[0])
print(member_nick)
comment_title=re.findall(r'<a class="postcounter" href=.*>[0-9]+.\s*(.*)<',html_text[0])
print(comment_title)
comment=re.findall(r'<span class="postContent">\s*(.*)<',html_text[0])
print(comment)
date=re.findall(r'span class="date-time">(.*),.*<',html_text[0])
print(date)
time=re.findall(r'span class="date-time">.*,\s*(.*)<',html_text[0])
print(time)
