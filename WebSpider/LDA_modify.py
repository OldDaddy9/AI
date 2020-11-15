'''
Author: can.chang
Date: 2020-11-15
'''

from gensim import corpora,models,similarities
import gensim
import time
import numpy as np
import csv
import jieba

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

file = 'data/douban.csv'
with open(file,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    column = [row[2] for row in reader ]

#获取所有分词结果
seg_words = []
for content in column:
    words = jieba.lcut(content)
    delte_stop_sent = []
    for sub_word in words:
        if (sub_word not in stop_words) and (sub_word not in sent_words):
         delte_stop_sent.append(sub_word)
    seg_words.append(delte_stop_sent)

M = len(seg_words)

#建立字典
dictionary = corpora.Dictionary(seg_words)
V = len(dictionary)

#使用上面的词典，将转换文档（预料）变成DT 矩阵
doc_term_matrix = [dictionary.doc2bow(words) for words in seg_words]

#使用gensim 来创建LDA模型对象
Lda = gensim.models.ldamodel.LdaModel

#在DT矩阵上运行和训练LDA模型
ldamodel = Lda(doc_term_matrix,num_topics=10,id2word=dictionary,passes=50)
#输出结果
for i in range(len(ldamodel.print_topics(num_topics=10,num_words=20))):
    print(ldamodel.print_topics(num_topics=10,num_words=20)[i])




# #转换文本数据为索引，并计数
# corpus = [dictionary.doc2bow(words) for words in seg_words]
#
# #计算tf-idf值
# corpus_tfidf = models.TfidfModel(corpus)[corpus]
#
# #训练模型
# topics_num = 30
# lda = models.LdaModel(corpus_tfidf,num_topics=topics_num,id2word=dictionary,
#                       alpha=0.01, eta=0.01,minimum_probability=0.001,
#                       update_every=1,chunksize=100,passes=1)
#
# show_topic_num = 10
# doc_topics = lda.get_document_topics(corpus_tfidf) #所有文档的主题分布
# idx = np.arange(M)
# np.random.shuffle(idx)
# idx = idx[:30]
# for i in idx:
#     topic = np.array(doc_topics[i])
#     topic_distribute = np.array(topic[:,1])
#     topic_idx = topic_distribute.argsort()[:(-show_topic_num-1):-1]
#     print('第%d个文档的前%d个主题：'%(i,show_topic_num))
#     print(topic_distribute[topic_idx])
#
# num_show_term = 7 #每个主题显示几个词
# print('结果：每个主题的词分布：------')
# for topic_id in range(topics_num):
#     print('主题#%d: \t'%topic_id)
#     term_distribute_all = lda.get_topic_terms(topicid=topic_id)
#     term_distribute = term_distribute_all[:num_show_term]
#     term_distribute = np.array(term_distribute)
#     term_id = term_distribute[:,0].astype(np.int)
#     print('词：\t')
#     for t in term_id:
#         print(dictionary.id2token[t])
#     print('\n概率：\t',term_distribute[:,1])