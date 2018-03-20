import chardet
chardet.detect(open('annotated_posts_v2.csv','rb').read())

print(chardet.detect(open('annotated_posts_v2.csv','rb').read()))
