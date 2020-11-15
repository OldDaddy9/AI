'''
Author: can.chang
Date: 2020-11-15
'''
import jieba
import csv
from snownlp import SnowNLP
#import pandas

def conbinate(FilePathList):
    all_contents = []
    for filepath in FilePathList:
        contents = [line.strip() for line in open(filepath,'r',encoding='gbk').readlines()]
        for content in contents:
            all_contents.append(content)
    return all_contents

negtive_coment = [line.strip() for line in open('data/sentment/negtive_coment.txt','r',encoding='gbk').readlines()]
negtive_sent = [line.strip() for line in open('data/sentment/negtive_sent.txt','r',encoding='gbk').readlines()]
postive_coment = [line.strip() for line in open('data/sentment/postive_coment.txt','r',encoding='gbk').readlines()]
postive_sent = [line.strip() for line in open('data/sentment/postive_sent.txt','r',encoding='gbk').readlines()]

degree_most = [line.strip() for line in open('data/sentment/most.txt','r',encoding='utf-8').readlines()]
degree_very = [line.strip() for line in open('data/sentment/very.txt','r',encoding='utf-8').readlines()]
degree_over = [line.strip() for line in open('data/sentment/over.txt','r',encoding='utf-8').readlines()]
degree_more = [line.strip() for line in open('data/sentment/more.txt','r',encoding='utf-8').readlines()]
degree_ish = [line.strip() for line in open('data/sentment/ish.txt','r',encoding='utf-8').readlines()]
degree_insufficiently = [line.strip() for line in open('data/sentment/insufficiently.txt','r',encoding='utf-8').readlines()]

#计算nlp 得分
nlp_emotion_dic = {}
with open('data/BosonNLP_sentiment_score.txt','r',encoding='utf-8') as nlp:
    while True:
        try:
            sentlist = nlp.readline()
            sentlist = sentlist[:-1]
            sentlist = sentlist.split(' ')
            nlp_emotion_dic[sentlist[0]] = float(sentlist[1])
        except IndexError:
            break
def nlp_emotion_score(comment):
    seg_words = jieba.lcut(comment)
    nlp_score = 0
    for word in seg_words:
        if word in nlp_emotion_dic:
            nlp_score += nlp_emotion_dic[word]
    return nlp_score



#创建情感词表
def sent_words_list(sentfilepath):
    sent_words = [line.strip() for line in open(sentfilepath,encoding='utf-8').readlines()]
    return  sent_words
sent_words = sent_words_list('data/all_sentment.txt')

#创建程度词表
def degree_words_list(degreefilepath):
    degree_words = [line.strip() for line in open(degreefilepath, encoding='gbk').readlines()]
    return degree_words
degree_words = sent_words_list('data/sentment/degree1.txt')

#计算知网情感得分
def emotion_zhiwang_score(comment,sent_words,degree_words):
    seg_words = jieba.lcut(comment)
#    print(seg_words)
    comment_sent_words = []
    score = 0
    local = 0
    sent_word_local = []
    if seg_words:
        for word in seg_words:
            local += 1
            if word in sent_words:
                comment_sent_words.append(word)
                sent_word_local.append(local)

    # print("==========0========")
    # print(score)
    #判断情感词词性，并加权
    if comment_sent_words:
        word = comment_sent_words[0]
        if (word in negtive_sent) or (word in negtive_coment):
            score -= 1
        elif (word in postive_sent) or (word in postive_coment):
            score += 1
        for i in range(1,len(comment_sent_words)):
            word  = comment_sent_words[i]
            if (word in negtive_sent) or (word in negtive_coment):
                score -= 1
            elif (word in postive_sent) or (word in postive_coment):
                score += 1
            word_befor = comment_sent_words[i-1]
            if word_befor in degree_most:
                score = score + 2
            elif word_befor in degree_very:
                score = score + 1.5
            elif (word_befor in degree_more) or ():
                score = score + 1.25
            elif word_befor in degree_ish:
                score = score + 0.75
            elif word_befor in degree_insufficiently:
                score =  score + 0.5
            elif word_befor in degree_over:
                score = score + (-1)
    # if comment_sent_words:
    #     for word in comment_sent_words:
    #         if (word in negtive_coment):
    #             score  = score + (-2)
    #         elif word in negtive_sent:
    #             score = score - 1
    #         elif word in postive_coment:
    #             score = score + 2
    #         elif word in postive_sent:
    #             score = score + 1
    # # print("==========1========")
    # # print(comment_sent_words)
    # # print(score)
    # #判断程度词并加权
    # comment_degree_words= []
    # if seg_words:
    #     for word in seg_words:
    #         if word in degree_words:
    #             comment_degree_words.append(word)
    # if comment_degree_words:
    #     for word in comment_degree_words:
    #         if word in degree_most:
    #             score = score * 2
    #         elif word in degree_very:
    #             score = score * 1.5
    #         elif (word in degree_more) or ():
    #             score = score * 1.25
    #         elif word in degree_ish:
    #             score = score * 0.75
    #         elif word in degree_insufficiently:
    #             score =  score * 0.5
    #         elif word in degree_over:
    #             score = score * (-1)
    #score = score -1
    # print("==========2========")
    # print(comment_degree_words)
    # print(score)
    return  score

# comment = '具有这个时代纪录片的学术性、艺术性和人文情怀，虽然有些文案已经有舌尖后纪录片时代的无逻辑瞎jb矫情感，但瑕不掩瑜。'
# score = emotin_score(comment,sent_words,degree_words)
# print(score)
# print('评论： ' + comment)
# print('得分： ' + str(score))


file = 'data/douban.csv'
new_fp = open('data/douban_new.csv','w',newline='',encoding='utf_8_sig')
writer = csv.writer(new_fp)
with open(file,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    #column = [row[2] for row in reader ]
    for row in reader:
        score = emotion_zhiwang_score(row[2],sent_words,degree_words)
        row.append(str(score))
        writer.writerow(row)
new_fp.close()

# file = 'data/douban_new.csv'
# new_fp = open('data/douban_nlp_zhiwang.csv','w',newline='',encoding='utf_8_sig')
# writer = csv.writer(new_fp)
# with open(file,'r',encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     #column = [row[2] for row in reader ]
#     for row in reader:
#         score = nlp_emotion_score(row[2])
#         row.append(str(score))
#         print(score)
#         writer.writerow(row)
# new_fp.close()


# with open('data/all_sentment.txt','w',encoding='utf-8') as fp:
#     for sent in all_contents:
#         fp.write(sent)
#         fp.write('\n')