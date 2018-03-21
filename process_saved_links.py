import pickle
import requests
import re
from bs4 import BeautifulSoup
from datetime import date,timedelta



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


def get_post_id(html_comment):
    postid=re.findall(r'id="(postbit.*)">',html_comment)[0] #this way the postid is returned inside a list
    print(postid)
    return postid
def get_member_ref(html_comment):
    site = 'http://www.spiegel.de'
    member_ref=site+re.findall(r'(/forum/member.*)">',html_comment)[0]
    print(member_ref)
    return member_ref
def get_member_nick(html_comment):
    member_nick=re.findall(r'<b>(.*)</b>',html_comment)[0]
    print(member_nick)
    return member_nick
def get_c_title(html_comment):
    comment_title=re.findall(r'<a class="postcounter" href=.*>[0-9]+.\s*(.*)<',html_comment)[0]
    print(comment_title)
    return comment_title
def get_c_body(html_comment):
    comment=re.findall(r'<span class="postContent">\s*(.*)<',html_comment)[0]
    print(comment)
    return comment
def get_date(html_comment):
    d=re.findall(r'span class="date-time">(.*),.*<',html_comment)[0]
    if d == 'Gestern':
        d = (date.today() - timedelta(1)).strftime('%d.%m.%y')
    elif d == 'Heute':
        d = date.today().strftime('%d.%m.%y')
    else:
        d = d
    print(d)
    return d
def get_time(html_comment):
    time=re.findall(r'span class="date-time">.*,\s*(.*)<',html_comment)[0]
    return time

def prepare_to_mongo(html_comment):
    map={}
    map['post_id']=get_post_id(html_comment)
    map['member_ref']=get_member_ref(html_comment)
    map['member_nickname']=get_member_nick(html_comment)
    map['title']=get_c_title(html_comment)
    map['body']=get_c_body(html_comment)
    map['date']=get_date(html_comment)
    map['time']=get_time(html_comment)
    #for e in map.keys():
    #    print(e,map[e])
    return map

db_entries=[]
def prepare_for_db():
    with open('forum/spiegel_forum_politik','rb') as file:
        lista=pickle.load(file)
    print(lista[:10])
    for p in lista:
        all_comments=get_comments_box(p)
        for c in all_comments:
            db_entries.append(prepare_to_mongo(c))
        print(db_entries[:3])
    print(len(db_entries))
    with open('comments/politik_comment', 'wb') as coll:
        pickle.dump(db_entries,coll)
    coll.close()

def trial():
    with open('map_topicfilename','rb') as f:
        map=pickle.load(f)
    print(type(map))
    for k in map.keys():  # check opening of saved links to forum on March 20th
        with open(map[k],'rb') as file:
            lista=pickle.load(file)
            print(lista[:10])
    html_text=get_comments_box(lista[2])
    print(lista[2])
    print(len(html_text))
    print(html_text[0])

    prepare_to_mongo(html_text[4])

lista_sections=['forum/spiegel_forum_politik','forum/spiegel_forum_wirtschaft'
,'forum/spiegel_forum_panorama','forum/spiegel_forum_sport'
,'forum/spiegel_forum_kultur','forum/spiegel_forum_netzwelt'
,'forum/spiegel_forum_wissenschaft','forum/spiegel_forum_gesundheit'
,'forum/spiegel_forum_karriere','forum/spiegel_forum_lebenundlernen'
,'forum/spiegel_forum_reise','forum/spiegel_forum_auto']

prepare_for_db()