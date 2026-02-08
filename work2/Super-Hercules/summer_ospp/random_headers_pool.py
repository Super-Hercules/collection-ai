import random

def get_random_headers():
    #User-Agent 浏览器标识
    user_agents = [
        #Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        #Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    ]

    Accept_Language = [
        "zh-CN,zh;q=0.9",
        "en;q=0.8",
        "en-GB;q=0.7",
        "en-US;q=0.6"
    ]

    body = {
        "difficulty": [],
        "lang": "zh",
        "orgName": [],
        "pageNum": "1",
        "pageSize": "500",
        "programName": "",
        "programmingLanguageTag": [],
        "supportLanguage": [],
        "techTag": []
    }

    headers = { #对于post请求更改了一些内容
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json, */*", #接受的数据类型
        "Content-Type": "application/json",
        "Accept-Language": random.choice(Accept_Language),
        "Accept-Encoding": "gzip, deflate, br",  #告知服务器支持压缩
        "Referer": "https://summer-ospp.ac.cn/org/projectlist?lang=zh&pageNum=1&pageSize=50",
        "Origin": "https://summer-ospp.ac.cn",
        "Connection": "keep-alive",  #保持连接，模拟浏览器行为
        "Sec-Fetch-Dest": "empty", #表示请求的资源将如何被使用
        "Sec-Fetch-Mode": "cors", #请求模式，cors用于API调用
        "Sec-Fetch-Site": "same-origin", #发起方与资源的联系，同源意为请求的发起方和目标资源在同一源，即协议、域名和端口三者完全相同
    }

    return body, headers