import requests
from random_headers_pool import get_random_headers

JWC_base_url = "https://jwch.fzu.edu.cn"

#爬取通知列表页面代码
def extract_the_first_notice_page():
    headers = get_random_headers()
    response = requests.get(JWC_base_url + "/jxtz.htm", headers = headers)
    return response.content

#翻页,页面上有一个"下一页"按钮哦
def get_next_page(soup):
    next_page_button = soup.find("span", class_ = "p_next p_fun")
    if next_page_button:
        next_page_href = next_page_button.find("a")
        if next_page_href:
            href = next_page_href.get("href")
            return JWC_base_url + href
    else:
        return None