import requests
import json
from fake_useragent import UserAgent
import re
import time
import csv
import random


ua = UserAgent(verify_ssl=False)
#url = 'https://api.bilibili.com/x/v2/reply?callback=jQuery172014684506758773996_1605231659828&jsonp=jsonp&pn=2&type=1&oid=17857003&sort=2&_=1605231676416'
url = 'https://api.bilibili.com/x/v2/reply'
headers = {
    'User-Agent': ua.random,
    'Referer':'https://www.bilibili.com/bangumi/play/ss22505/?from=search&seid=1830814461731600837',
}


# page_num = 2
# page_result = requests.get(url=url, headers=headers, params=params)
# page_result = page_result.json()
# print(page_result)

# with open('data/bilibili/bili.txt','w+',encoding='utf-8') as fp:
#     for page_num in range(1,110):
#         params = {
#             "jsonp": "jsonp",
#             "pn": '%d' % page_num,
#             "type": "1",
#             "oid": "17857003",
#             "sort": "2",
#         }
#         page_result = requests.get(url=url,headers=headers,params=params)
#         print(page_num,'  ',page_result.status_code)
#         page_result=page_result.json()
#         #content = json.loads(page_result)
#         fp.write(json.dumps(page_result,ensure_ascii=False))
#         fp.write('\n')
#         time.sleep(random.randint(20, 30))

fp_csv = open('data/bilibili.csv','wt',newline='',encoding='utf_8_sig')
writer = csv.writer(fp_csv)
writer.writerow(('ID','性别','喜欢','时间','回复','评论'))

with open('data/bilibili/bili.txt','r',encoding='utf-8') as fp:
    for line in fp:
        result = json.loads(line)
        reply_dict_list = result['data']['replies']
        reply_num = len(reply_dict_list)
        #print(reply_num)
        for reply in reply_dict_list:
            like = reply['like']
            rcount = reply['rcount']
            ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(reply['ctime']))
            user_name = reply['member']['uname']
            sex = reply['member']['sex']
            content = reply['content']['message']
            writer.writerow((user_name, sex, like, ctime, rcount, content))
            sub_replies = reply['replies']
            if sub_replies:
                sub_rep_num = len(sub_replies)
                #print(like, rcount, ctime, sex, user_name)
                for sub_rep in sub_replies:
                    sub_like = sub_rep['like']
                    sub_rcount = sub_rep['rcount']
                    sub_ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sub_rep['ctime']))
                    sub_user_name = sub_rep['member']['uname']
                    sub_sex = reply['member']['sex']
                    sub_content = sub_rep['content']['message']
                    writer.writerow((sub_user_name, sub_sex, sub_like, sub_ctime, sub_rcount, sub_content))
fp_csv.close()