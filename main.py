import requests
from urllib.parse import unquote
import json
import math
Code By XieSiYu
# 校招官网 https://xskydata.jobs.feishu.cn/school
BaseUrl = "https://xskydata.jobs.feishu.cn/api/v1/search/job/posts"

def get_Cookies():
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Origin': 'https://xskydata.jobs.feishu.cn',
        'Referer': f'https://xskydata.jobs.feishu.cn/school'
    }
    data = {
        "portal_entrance": 1
    }
    url = "https://xskydata.jobs.feishu.cn/api/v1/csrf/token"
    r = session.post(url, headers=headers, data=data)
    cookies = session.cookies.get_dict()
    return cookies,session

def get_Page(page):
    cookies,session=get_Cookies()
    headers = {
        "accept": "application/json, text/plain, */*",
        # "host": "xskydata.jobs.feishu.cn",
        "origin": "https://xskydata.jobs.feishu.cn",
        'referer': 'https://xskydata.jobs.feishu.cn/school',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'website-path': 'school',
        "x-csrf-token": unquote(cookies['atsx-csrf-token']),
    }
    params = {
        "job_category_id_list": [],
        "keyword": "",
        "limit": 10,
        "location_code_list": [],
        "offset": page*10,
        "portal_entrance": 1,
        "portal_type": 6,
        "recruitment_id_list": [],
        "subject_id_list": [],
        '_signature': 'tYuESAAgEAKVizrYLrEnPrWLhFAANQW',
    }
    r = session.post(BaseUrl, headers=headers, data=json.dumps(params))
    return r.json()

def parse_data(data):
    res={}
    res["职位名称"]=data["title"]
    res["职位类别"]=data["job_category"]["parent"]["name"]+"-"+data["job_category"]["name"]
    res["工作城市"]=data["city_info"]["name"]
    res["职位描述"]=data["description"]
    res["职位要求"]=data["requirement"]

    return res

if __name__ == '__main__':
    index=get_Page(0)
    json_result=[]
    count=index['data']['count']
    page=math.ceil(count/10)
    for i in range(page):
        print("正在爬取第",i+1,"页数据......")
        result=get_Page(i)
        PageData = result['data']['job_post_list']
        for per in PageData:
            json_result.append(parse_data(per))

    print("爬取完成!")
    print("保存文件中......")
    with open("Xsky_Jobs.json","w",encoding="utf-8") as file:
        file.write(json.dumps(json_result,indent=2,ensure_ascii=False))
    print("任务完成!")
