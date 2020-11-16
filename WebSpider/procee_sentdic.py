'''
Author: can.chang
Date: 2020-11-16
'''



coment_sent_num = [line.strip() for line in open('data/result/coment_sent_num.txt', 'r', encoding='utf-8').readlines()]
negtive = [line.strip() for line in open('data/dependens/negtive.txt', 'r', encoding='utf-8').readlines()]
postive = [line.strip() for line in open('data/dependens/postive.txt', 'r', encoding='utf-8').readlines()]
print(coment_sent_num)
print(postive)
print(negtive)

fp = open('data/process_sentment/negtive.txt','w',encoding='utf-8')
for word in negtive:
    if len(word) > 1:
        fp.write(word)
        fp.write('\n')
fp1 = open('data/process_sentment/postive.txt','w',encoding='utf-8')
for word in postive:
    if len(word) > 1:
        fp1.write(word)
        fp1.write('\n')