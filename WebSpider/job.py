import requests
from lxml import etree
from fake_useragent import UserAgent

# class Job(Object):
#     def __init__(self):
#         self.url = ""
#
# print("test")

url = 'https://sh.58.com/job/'
ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent': ua.random,
}

params = {
    "key": "档案",
    "cmcskey": "档案",
    "final": "1",
    "jump": "1",
    "specialtype": "gls",
    "classpolicy": "LBGguide_A,main_B,job_B,hitword_true",
    "6": "",
    "0,uuid_32362bedde8c4542add45612acbf6488,displocalid_2,from_main,to_jump":"",
    "PGTID": "0d302408-0000-2e5f-eae9-d5b4dace2621",
    "ClickID": "3",
}

# page_html = requests.get(url=url,headers=headers,params=params).text

# with open('data/job.html','w',encoding='utf-8') as fp:
#     fp.write(page_html)

#html = etree.parse('data/job.html',etree.HTMLParser(),decode="utf-8")
fp = open("data/job.html",encoding='utf-8')
html = fp.read()
parse_html = etree.HTML(html)
li_list = parse_html.xpath('//div[@class="main clearfix"]//div[@class="leftCon"]/ul/li')#
link_list = []
name_list = []
locas_lsit = []
salary_list = []
for li in li_list:
    link = li.xpath('.//div[@class="job_name clearfix"]/a/@href')[0]
    link_list.append(link)
    job_text = li.xpath('.//div[@class="job_name clearfix"]/a//text()')
    job_name = job_text[1]
    job_local = job_text[3]
    name_list.append(job_name)
    locas_lsit.append(job_local)
    job_slary = li.xpath('.//p[@class="job_salary"]/text()')[0]
    salary_list.append(job_slary)
    #print(job_slary)


    #print(job_text[1],job_text[3])

print(link_list[0])

detail_respons = requests.get(url=link_list[0],headers=headers).text
detail_parase = etree.HTML(detail_respons)
print(detail_respons)
search = detail_parase.xpath('//i[@id="totalcount"]')
print(search)
#print(link)
#html = etree.tostring(html,encoding='utf-8',pretty_print=True,method='html')
#print(li_list)
print("finished!!")
