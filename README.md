# webScraper
Retrieving comments under articles from the site www.spiegel.de

Looking at the Spiegel online Forum (http://www.spiegel.de/forum/) one can notice that it is organized into sections.
Each section contains links to its articles forum spaces.
In each article's comments space, comments are splitted into several pages (reachable clicking the 'next page' botton).

For every section's url (e.g. http://www.spiegel.de/forum/politik), links to articles have been retrieved and saved into separate pickle files in the forum directory (on the 20th March 2018).
This has been done using BeautifulSoup and requests python packages: see script request.py.
The saved files are then processed through the process_saved_links.py: for each article's link all the comments are extracted in html format and then processed by means of regular expression to obtain the wanted information. 
Each comment results in a python's dict class containing the following keys:
comment's content (body), comment's title (title), comment's quote (quotes: that is the comment the user is referring to), comment's id (post_id), link to author's info (member_ref), comment's date (date), comment's time (time), author's nickname (member_nickname) and link to the article space the comment refers to (forum link).

A processed comment at the end looks like this:

{
  
  body : natürlich gehört israel da mit rein, weil die auf ihre eigene art entscheiden, wer atomwaffen haben darf und wer nicht.
  
  title : 
  
  quotes : Dann muesste man mindestens auch Indien und Pakistan mit auflisten. In die Reihe, die in dem Beitrag, den ich kommentierte, aufgebaut wurde, gehoerte Israel nicht rein.
  
  post_id : postbit_57714903
  
  member_ref : http://www.spiegel.de/forum/member-129309.html
  
  time : 21:24
  
  member_nickname : bloub
  
  date : 16.08.2017
  
  forum_link : http://www.spiegel.de/forum/politik/konflikt-mit-den-usa-iran-droht-mit-ende-des-atomabkommens-thread-639612-1.html
}

The processed comments are again saved into pickle files inside the directory comments: at the moment just a small (really small) part of those under articles in http://www.spiegel.de/forum/politik/ are been collected.
The section http://www.spiegel.de/forum/politik/ alone contains 49680 links to articles (on 20th March 2018, when the links have been saved into pickle files in the forum directory), each of those contain zero, one or several PAGES of comments.
The notes.txt files contains update on the current collected amount per section (sections not mentioned have not been scanned yet).
