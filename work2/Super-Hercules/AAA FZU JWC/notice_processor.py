import requests
from bs4 import BeautifulSoup

def extract_notice(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    notice_data = []
    notice_items = soup.select("ul.list-gl > li")
    for item in notice_items:
        #日期
        date_span = item.find("span", class_ = "doclist_time")
        if date_span:
            font_tag = date_span.find("font")    #有些日期写在font标签内，也许跟通知类型有关系？
            if font_tag:
                date = font_tag.text.strip()
            else:
                date = date_span.text.strip()
        else:
            date = ""

        #标题与链接
        link_tag = item.find("a")
        if link_tag:
            title = link_tag.get("title", "").strip()
            if not title:
                title = link_tag.text.strip()

            href = link_tag.get("href", "").strip()
            if href and not href.startswith(("http://", "https://")):
                if href.startswith("/"):
                    href = f"https://jwch.fzu.edu.cn{href}"
                else:
                    href = f"https://jwch.fzu.edu.cn/{href}"
        else:
            title = ""
            href = ""

        #通知部门
        full_text = item.get_text(strip = True)
        if date and title:
            category_text = full_text.replace(date, "").replace(title, "").strip()
            category = category_text.strip("【】")
        else:
            category = ""

        #整合
        notice_data.append({
            "date": date,
            "category": category,
            "title": title,
            "link": href
        })
    
    #返回
    return notice_data