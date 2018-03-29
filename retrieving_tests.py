import  re
import pickle
######################### FROM process_saved_links ###########################################################################
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
        comment=' '
        for stringa in c:
            stringa=re.sub(r'<br?/?>',r'',stringa)   #resolve problem of having <br/> between text and/or <b/>
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



############### DISCOVERING ERRORS, IN RETRIEVING TEXT WITH REGEX, AND CORRECTING THEM ################################################################

def test_body():
    body='<span class="postContent">1) Ich weiß, nur sind Sie mit 49% Gesamtwirkungsgrad ziemlich weit am oberen Rand des Möglichen.<br>'\
    'Ich hatte Ihnen ja die Spannbreite des Wirkungsgrades Strom --&gt; Gas genannt, je nachdem welches Gas herauskommen soll und wie dieses komprimiert wird.<br>'\
    '<br>'\
    '2) Es sind keine Meiler, es sind Kraftwerke.<br>'\
    'Desweiteren sollten Sie genauer lesen, ich hatte geschrieben das es in Deutschland nur wenige dieser hochmodernen GuD Kraftwerke mit einem Wirkungsgrad um die 60% gibt.<br>'\
    'Ihre Angabe 77 GuD ist die Menge die Siemens weltweit verkauft hat.</span> '\
    '</p>'
    res=re.findall(r'<span class="postContent">(.*?)</span>\s*</p>',body)
    body=''
    print('numero risultati: '+str(len(res)))
    for t in res:
        temp = t
        temp = re.sub(r'<b?r?/?>', r' ', temp)
        temp = re.sub(r'\n', r' ', temp)
        temp = re.sub(r'</?q>', r'', temp)
        temp = re.sub(r'&amp;', r'&', temp)
        body=body+temp
    print(body)

def test_get_nick():
    example='<b>frank-xps</b>'
    print('html: '+example)
    print('result: '+get_member_nick(example))

def test_get_title():
    example='<a class="postcounter" href="/forum/wirtschaft/bundesbank-vorstand-dann-kluengelt-mal-schoen-thread-727301-2.html#postbit_63594287" name="post63594287">18.'\
    '\n               Q.e.d.</a>'\
    '\n																	Zitat von '
    print('html: ' + example)
    print('result: ' + get_c_title(example))

def test_quote():
    example='<span class="quote">'\
    '									Zitat von <b>erwin.duesenberg</b>'\
    '           				<a href="/forum/wirtschaft/urteil-wie-anton-schlecker-seine-kinder-opferte-thread-683061-18.html#postbit_60644375" title="zum zitierten Beitrag" rel="nofollow">'\
	'							<img src="/static/forum/images/buttons/lastpost-right.png" style="position:relative;top:1px">'\
	'									</a>'\
	'									<br>'\
	'									 <q>Eine Gefängnissstrafe <q> hilft <q>niemandem</q>. Hier </q>müsste stattdessen das gesamte Privatvermögen der Beteiligten konfiziert werden um die Opfer zu entschädigen.</q>'\
	'									 </span>'
    print(get_quote(example))

def correct_quote():    # used to correct quotes in witschaft file 1-5.. the new one are already corrected
    for i in range(1,6):
        write_back=[]
        stringa='comments/wirtschaft_'
        with open(stringa+str(i),'rb') as f:
            read=pickle.load(f)
        f.close()
        for item in read:
            quote=[]
            to_check=item['quotes']
            for t in to_check:
                print('before: '+ t)
            for q in to_check:
                temp = q
                temp = re.sub(r'<b?r?/?>', r'', temp)
                temp = re.sub(r'\n', r' ', temp)
                temp = re.sub(r'</?q>', r'', temp)
                temp = re.sub(r'&amp;', r'&', temp)
                quote.append(temp)
            item['quotes']=quote
            for t in item['quotes']:
                print('after: '+t)
            write_back.append(item)
        print('WRITING IN FILE: '+stringa+str(i))
        with open(stringa+str(i),'wb') as fs:
            pickle.dump(write_back,fs)
        fs.close()



test_quote()

