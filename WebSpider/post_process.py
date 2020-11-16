'''
Author: can.chang
Date: 2020-11-14
'''
import jieba
import wordcloud
import matplotlib.pyplot as plt
import csv
import numpy as np
#from PIL import Image
from imageio import imread

#创建停词表
def stop_words_list(stopfilepath):
    stop_words = [line.strip() for line in open(stopfilepath,encoding='utf-8').readlines()]
    return  stop_words

stop_words = stop_words_list('data/allstopwords.txt')

#创建情感词表
def sent_words_list(sentfilepath):
    sent_words = [line.strip() for line in open(sentfilepath,encoding='utf-8').readlines()]
    return  sent_words
sent_words = sent_words_list('data/all_sentment.txt')

file = 'guobao/all_comment.csv'
with open(file,'r',encoding='gbk') as csvfile:
    reader = csv.reader(csvfile)
    column = [row[2] for row in reader ]




#获取所有分词结果
seg_words = []
for content in column:
    words = jieba.lcut(content)
    for sub_word in words:
        seg_words.append(sub_word)

#去除停用词
seg_words_deleted = []
for word in seg_words:
    if word not in stop_words:
        if word != '\t':
            seg_words_deleted.append(word)

all_words_without_stopword_num = len(seg_words_deleted)

#去除情感词
seg_words_deleted_sent = []
coment_sent_words = []
for word in seg_words_deleted:
    if word not in sent_words:
        if word != '\t':
            seg_words_deleted_sent.append(word)
    else:
        coment_sent_words.append(word)
all_sent_num = len(coment_sent_words)
#统计词频
word_num = {}
afte_delete = []
for word in seg_words_deleted_sent:
    if len(word) == 1:
        continue
    else:
        word_num[word] = word_num.get(word,0) + 1
        afte_delete.append(word)

sent_num = {}
for word in coment_sent_words:
    sent_num[word] = sent_num.get(word,0) + 1

#按词频排序
items =  list(word_num.items())
items.sort(key=lambda  x:x[1], reverse=True)
sent_items = list(sent_num.items())
sent_items.sort(key=lambda x:x[1],reverse=True)

#存储词频
with open('guobao/result/word_num_delete_sent.txt','w',encoding='utf-8') as fp:
    for item in items:
        fp.write(str(item[0]) + '   '+str(item[1]))
        #fp.write(item[1])
        fp.write('\n')

with open('guobao/result/coment_sent_num.txt','w',encoding='utf-8') as fp:
    for item in sent_items:
        fp.write(str(item[0]) + '   '+str(item[1]))
        #fp.write(item[1])
        fp.write('\n')

for i in range(0,10):
    word ,_ =items[i]
    print(word,_)

size = int(len(items)*0.3)
mood =  set(items[:size])
mood_without_stop = list(mood)

#生成词云
sent_stop_words = ['完','玩','想','讲','中','真','说']
org_stop_words = ['真的','一名','','','','']
background = imread('data/timg.jpg')
wc = wordcloud.WordCloud(background_color="white",
                         mask=background,
                         stopwords=org_stop_words,
                         max_words=size,
                         font_path='C:\Windows\Fonts\simkai.ttf')
word_list = ",".join(seg_words_deleted_sent)
myword = wc.generate(word_list)
wc.to_file('guobao/result/coment_sent_numt.jpg')

print(all_words_without_stopword_num,all_sent_num)
#展示词云
plt.imshow(wc)
plt.axis('off')
plt.show()