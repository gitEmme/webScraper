import pickle
import requests
import re
from bs4 import BeautifulSoup
from datetime import date,timedelta

############################# the following  look for links in a spiegel's html page, under a specified html class tag, reconstructing the absolute url if necessary ########################
############################# catching connection exceptions because sometimes the comment space under an article can be closed, starting at a certain day  #################################
def find_links(site,address,string):
    links = []
    try:
        main_page = requests.get(address)
        soup = BeautifulSoup(main_page.text, 'html.parser')
        res = []
        for item in soup.find_all(class_=string):
            res.append(str(item))
        for e in res:
            found = re.findall(r'(?<=href=").*?(?=")', e)  # 'href=[\'"]?([^\'" >]+)'  or '(?<=href=").*?(?=")'
            for i in found:
                if 'http' not in i:
                    links.append(site + i)
                else:
                    links.append(i)
        #for t in links:
         #   print(t)
    except requests.exceptions.HTTPError as err:
        print("Http Error:", err)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as errf:
        print("OOps: Something Else", errf)
    return links

######## comments in spiegel.de are organised in a forum divided into sections: ################################################################################################
############ each section has links to each comments space of its articles; These links are divided into pages, sometimes several: 2484 pages under politik on 19th March ######
############ the following is my black cat clicking next in each forum until he has copied-pasted every link to next and next of next page (and so on) in a forum section ######
def click_next(url_item):
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

####################### this, given a comments' space, looks in every page of that space for comments ########################################
def get_comments_box(address):
    string='postbit clearfix' # name of html class containing each comment in http://www.spiegel.de/forum/'
    res = []
    for p in click_next(address):
        try:
            main_page = requests.get(p)
            soup = BeautifulSoup(main_page.text, 'html.parser')
            for item in soup.find_all(class_=string):
                res.append(str(item))
            #for t in res:
            #    print(t)
        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as errf:
            print("OOps: Something Else", errf)
    return res

####################### the following get functions are used to retrieve info from the html of extracted comments #############
def get_post_id(html_comment):
    postid=re.findall(r'id="(postbit.*)">',html_comment)[0] #this way the postid is returned inside a list
    return postid

def get_member_ref(html_comment):
    site = 'http://www.spiegel.de'
    temp=re.findall(r'(/forum/member.*)">',html_comment)
    if len(temp)>0:
        member_ref=site+temp[0]
    else:
        member_ref=''
    return member_ref

def get_member_nick(html_comment):
    temp=re.findall(r'<b>(.*\S)</b>',html_comment)
    if len(temp)>0:
        member_nick=temp[0]
    else:
        member_nick=''    #usually there's always a nickname if not ''
    return member_nick

def get_c_title(html_comment):
    title=re.findall(r'<a class="postcounter" href=.*>[0-9]+.\s*(.*\S)<',html_comment)
    if(len(title)>0):
        comment_title=title[0]
    else:
        comment_title=''
    return comment_title

def get_c_body(html_comment):
    c=re.findall(r'<span class="postContent">(.*)</span>\s*</p>',html_comment,re.DOTALL)
    comment=''
    if (len(c) > 0):    #there are comments with just title and a quote of another comment :o
        comment=''
        for stringa in c:
            stringa=re.sub(r'<br?/?>',r' ',stringa)   #resolve problem of having <br/> between text and/or <b/>
            stringa=re.sub(r'\n',r' ',stringa)  #remove empty lines and sub with a space
            stringa=re.sub(r'</?q>',r' ',stringa) #remove quotes tag and sub with  space
            stringa=re.sub(r'&amp;',r'&',stringa) # ---!!!!!!!!!!!! I realize at file politik_10 that i didnt check this :(
            comment=comment+stringa
    return comment
def get_quote(html_comment):
    quote_f=re.findall(r'<q>(.*)</q>\s*</span>',html_comment,re.DOTALL)
    if(len(quote_f))>0:
        quote=[]
        for q in quote_f:
            temp=q
            temp=re.sub(r'<b?r?/?>',r'',temp)
            temp=re.sub(r'\n',r' ',temp)
            temp=re.sub(r'</?q>',r'',temp)
            temp=re.sub(r'&amp;',r'&',temp)
            quote.append(temp)
    else:
        quote=[]
    return quote

def get_date(html_comment):
    d=re.findall(r'span class="date-time">(.*),.*<',html_comment)[0]
    if d == 'Gestern':
        d = (date.today() - timedelta(1)).strftime('%d.%m.%y')
    elif d == 'Heute':
        d = date.today().strftime('%d.%m.%y')
    else:
        d = d
    return d

def get_time(html_comment):
    time=re.findall(r'span class="date-time">.*,\s*(.*)<',html_comment)[0]
    return time
################ the following map each extracted property to its value: preparing data for the database ##############
def prepare_to_mongo(html_comment,link):
    map={}
    map['post_id']=get_post_id(html_comment)
    map['member_ref']=get_member_ref(html_comment)
    map['member_nickname']=get_member_nick(html_comment)
    map['title']=get_c_title(html_comment)
    map['body']=get_c_body(html_comment)
    map['date']=get_date(html_comment)
    map['time']=get_time(html_comment)
    map['forum_link']=link
    map['quotes']=get_quote(html_comment)
    for e in map.keys():
        print(e,map[e])
    return map

#################### the following are used to contruct lists of comments with related info and save them into pickle files ######
def prepare_for_db(*lista): #take a list of links and from that it retrieve all comments and put in a ready form for the db
    stringa='wirtschaft_'
    max_index=len(lista)//200
    for i in range(19,20):
        db_entries = []
        if i==1:
            for p in lista[(i-1)*200 :i * 200 + 1]:  # links to articles' forum are scanned 200 in 200 not to exceed maximum list size
                all_comments = get_comments_box(p)
                for c in all_comments:
                    db_entries.append(prepare_to_mongo(c, p))
            print(len(db_entries))
            print('WRITING ON FILE: ' + stringa + str(i))
            with open('comments/' + stringa + str(i),'wb') as coll:  # save comments ready to push in a db in a pickle file
                pickle.dump(db_entries, coll)
            coll.close()
        elif 1<i<max_index:
            for p in lista[(i-1)*200 + 1:i * 200 + 1]:  # links to articles' forum are scanned 200 in 200 not to exceed maximum list size
                all_comments = get_comments_box(p)
                for c in all_comments:
                    db_entries.append(prepare_to_mongo(c, p))
            print(len(db_entries))
            print('WRITING ON FILE: ' + stringa + str(i))
            with open('comments/' + stringa + str(i),'wb') as coll:  # save comments ready to push in a db in a pickle file
                pickle.dump(db_entries, coll)
            coll.close()
        else:
            for p in lista[(i-1)*200 + 1:]:  # links to articles' forum are scanned 200 in 200 not to exceed maximum list size
                all_comments = get_comments_box(p)
                for c in all_comments:
                    db_entries.append(prepare_to_mongo(c, p))
            print(len(db_entries))
            print('WRITING ON FILE: '+stringa+str(i))
            with open('comments/' + stringa + str(i),'wb') as coll:  # save comments ready to push in a db in a pickle file
                pickle.dump(db_entries, coll)
            coll.close()



def saving():
    lista_sections=['forum/spiegel_forum_politik','forum/spiegel_forum_wirtschaft'
    ,'forum/spiegel_forum_panorama','forum/spiegel_forum_sport'
    ,'forum/spiegel_forum_kultur','forum/spiegel_forum_netzwelt'
    ,'forum/spiegel_forum_wissenschaft','forum/spiegel_forum_gesundheit'
    ,'forum/spiegel_forum_karriere','forum/spiegel_forum_lebenundlernen'
    ,'forum/spiegel_forum_reise','forum/spiegel_forum_auto']

    with open(lista_sections[1], 'rb') as file: #read saved article links from politik forum section
        lista = pickle.load(file)
    #print(lista[:10])
    prepare_for_db(*lista)  #prepare file of dictionaries (one for each comment) to put in the database then
    print(len(lista))

def check_saved(file_name):     #to open a saved comments pickle file and count the total amount
    l=0
    for i in range(1,6):
        with open(file_name+str(i),'rb') as fp:
            read=pickle.load(fp)
        fp.close()
        print(read[:3])
        print('#comments in '+file_name+str(i)+': ',len(read))
        l+=len(read)
    print(l)

#at the moment saving comments from section wirstchaft : links in lista_sections[1] politik to be saved again...
saving()
#check_saved('comments/wirtschaft_')
