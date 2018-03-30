from lemma_functions import lemmatizer_funct # this function take as input a list of tokens and return a lemma list

text0 = open('comment.txt').read()
text1 = open('comment1.txt').read()


comments_lemma_list=[]
comments_lemma_list.append((lemmatizer_funct(text0),'pos'))
comments_lemma_list.append((lemmatizer_funct(text1),'neg'))
#print(comments_lemma_list)
print("\n")
def all_words(comments_list):
	words=set(word for val in comments_list for word in val[0])
	print(words)
	dictionary=[({word:(word in val[0]) for word in words},val[1])for val in comments_list]
	print("\n")	
	print(dictionary)

all_words(comments_lemma_list)
