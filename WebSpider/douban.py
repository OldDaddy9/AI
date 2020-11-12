import requests
import json
from fake_useragent import UserAgent
from lxml import etree
import csv
import random
import time
'''
抓取原始页面并保存到本地
'''

# url = 'https://movie.douban.com/subject/1439452/comments?percent_type=h&start=%d&limit=20&status=P&sort=new_score'
# ua = UserAgent(verify_ssl=False)
# headers = {
#     'User-Agent': ua.random,
#     'Cookie':'ll="108296"; bid=qAnoSiQLQjI; __utma=30149280.1742499370.1605145377.1605145377.1605145377.1; __utmc=30149280; __utmz=30149280.1605145377.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2="168008237:vg0lnErtpac"; ck=cd5p; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16800; __utma=223695111.1894707179.1605145451.1605145451.1605145451.1; __utmb=223695111.0.10.1605145451; __utmc=223695111; __utmz=223695111.1605145451.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1605145451%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __yadk_uid=X0Ceb36LlgTzn2MWK0OXuqGRJQpkS0B9; _vwo_uuid_v2=D254326FBEB17D12461DC8517DD8FAF24|e271f9a8d0c77e1219987692c9c45104; __utmb=30149280.5.10.1605145377; __gads=ID=53316d6f51c4b4ab:T=1605145496:S=ALNI_MZH6hQK7DBKBCky23fuM5Yiu4D8YA; _pk_id.100001.4cf6=af2c751b6694f560.1605145451.1.1605147358.1605145451.',
#     'Connection':'keep-alive',
# }
# for i in range(0,25):
#     page_num = i * 20
#     time.sleep(random.randint(20,30))
#     page_html = requests.get(url=url%page_num,headers=headers)
#     print(page_html.status_code)
#     page_html = page_html.text
#     with open('data/douban/douban_h_%d.html'%page_num,'w',encoding='utf-8') as fp:
#         fp.write(page_html)

'''
读取刚才爬取的页面，并解析其中的信息
'''
user_list = []
star_list = []
content_list = []
vote_list = []
time_list = []

fp = open('data/douban/douban_m_0.html',encoding='utf-8')
html = fp.read()
parse_html = etree.HTML(html)
movie_name = parse_html.xpath('//*[@id="content"]/h1/text()')
watched1 = parse_html.xpath('//ul[@class="fleft CommentTabs"]/li[1]/span/text()')[0]
watched2 = parse_html.xpath('//ul[@class="fleft CommentTabs"]/li[2]/a/text()')[0]
watched3 = parse_html.xpath('//ul[@class="fleft CommentTabs"]/li[3]/a/text()')[0]
good_juge = parse_html.xpath('//div[@class="comment-filter"]/label[2]/span[2]/text()')[0]
good_juge = "good_juge: "+good_juge
normal_juge = parse_html.xpath('//div[@class="comment-filter"]/label[3]/span[2]/text()')[0]
normal_juge = "normal_juge: "+ normal_juge
bad_juge = parse_html.xpath('//div[@class="comment-filter"]/label[4]/span[2]/text()')[0]
bad_juge = "normal_juge: "+ bad_juge
fp.close()


for i in range(0,25):
    page_num = i * 20
    fp = open('data/douban/douban_h_%d.html'%page_num,encoding='utf-8')
    html = fp.read()
    parse_html = etree.HTML(html)
    mod_db = parse_html.xpath('//*[@id="comments"]/div[@class="comment-item "]')

    print("good : %d"%page_num)
    for db in  mod_db:
        user = db.xpath('.//div[@class="comment"]/h3/span[2]/a/text()')[0]
        user_list.append(user)
        vote = db.xpath('.//div[@class="comment"]//span[@class="votes vote-count"]/text()')[0]
        vote_list.append(vote)
        time = db.xpath('.//div[@class="comment"]/h3/span[2]/span[@class="comment-time "]/@title')[0]
        time_list.append(time)
        star = db.xpath('.//div[@class="comment"]/h3/span[2]/span[2]/@title')[0]
        star_list.append(star)
        content = db.xpath('.//div[@class="comment"]/p/span[1]/text()')
        if not content :
            content = [' ']
        content_list.append(content[0])
        #page_index = parse_html.xpath('//div[@id="paginator"]/a[3]/@class')[0]
        #print(page_index)
    fp.close()

for i in range(0,5):
    page_num = i * 20
    fp = open('data/douban/douban_m_%d.html'%page_num,encoding='utf-8')
    html = fp.read()
    parse_html = etree.HTML(html)
    mod_db = parse_html.xpath('//*[@id="comments"]/div[@class="comment-item "]')

    print("soso : %d" % page_num)
    for db in  mod_db:
        user = db.xpath('.//div[@class="comment"]/h3/span[2]/a/text()')[0]
        user_list.append(user)
        vote = db.xpath('.//div[@class="comment"]//span[@class="votes vote-count"]/text()')[0]
        vote_list.append(vote)
        time = db.xpath('.//div[@class="comment"]/h3/span[2]/span[@class="comment-time "]/@title')[0]
        time_list.append(time)
        star = db.xpath('.//div[@class="comment"]/h3/span[2]/span[2]/@title')[0]
        star_list.append(star)
        content = db.xpath('.//div[@class="comment"]/p/span[1]/text()')
        if not content:
            content = [' ']
        content_list.append(content[0])
        #page_index = parse_html.xpath('//div[@id="paginator"]/a[3]/@class')[0]
        #print(page_index)
    fp.close()

list_num = len(user_list)
print("get %d datas!!"%list_num)
fp_csv = open('data/douban.csv','wt',newline='',encoding='utf_8_sig')
writer = csv.writer(fp_csv)
writer.writerow((movie_name,watched1,watched2,watched3,good_juge,normal_juge,bad_juge))
writer.writerow(("ID","星级","评论","被引用","时间"))
for i in range(0,list_num):
    writer.writerow((user_list[i],star_list[i],content_list[i],vote_list[i],time_list[i]))

fp_csv.close()
print("finish!!")