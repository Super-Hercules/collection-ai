import requests

#爬取通知列表页面代码
def extract_notice_page():
    pass

#处理通知网址（翻页）
def request_notice_url():
    the_first_page = "https://jwch.fzu.edu.cn/jxtz.htm"
    response = requests.get(the_first_page)
    info = {
        "page"
    }

#翻页
def get_next_page(soup):
    page_info = {
        "current_page": 1,
        "total_pages": 1,
        "page_links": [],
        "next_page": None,
        "last_page": None
    }

    #查找翻页容器
    pagination_div = soup.find('div', class_='ecms_pag')
    if not pagination_div:
        return page_info
    
    #提取页码
    page_spans = pagination_div.find_all("span", class_ = "p_no")
    for page_span in page_spans:
        link = page_span.find("a")
        if link:
            href = link.get("href", "")
            page_num = link.text.strip()
            if href and page_num.isdigit():
                if not href.startswith(('http://', 'https://')):
                    if href.startswith('/'):
                        href = f"https://jwch.fzu.edu.cn{href}"
                    else:
                        href = f"https://jwch.fzu.edu.cn/{href}"

                page_info["page_links"].append({
                    "page_num": int(page_num)
                    "url": href
                })

    #寻找最大页码
    page_numbers = [link["page_num"] for link in page_info["page_links"]]
    if page_numbers:
        page_info["total_pages"] = max(page_numbers)