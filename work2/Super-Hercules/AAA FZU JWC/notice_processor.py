from bs4 import BeautifulSoup
from random_headers_pool import get_random_headers
from extractor import JWC_base_url
import os
import csv
import requests

#处理content中的信息
def process_notice(html_content):
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
            "日期": date,
            "通知部门": category,
            "标题": title,
            "链接": href
        })
    
    #返回
    return notice_data

#导出为csv文件
def output_as_csv(notices, attachment_name, filename = "FZU_JWC_notices.csv"):
    fieldnames = ["序号", "日期", "通知部门", "标题", "链接", "附件"]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)
    with open(filepath, "w",encoding = "utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()

        for i, notice in enumerate(notices, 1):
            writer.writerow({
                "序号": i,
                "日期": notice["date"],
                "通知部门": notice["category"],
                "标题": notice["title"],
                "链接": notice["link"],
                "附件": attachment_name
            })

#偷走通知里的附件，返回附件信息
def download_attachment_file(href):
    headers = get_random_headers()
    response = requests.get(href, headers = headers)
    soup = BeautifulSoup(response.content, "html.parser")
    attachment = soup.find("ul", style = "list-style-type:none;")

    if attachment:
        li = attachment.get("li", "")
        a = li.find("a")
        attachment_name = a.get_text(strip = True)
        attachment_href = JWC_base_url + a.get("href", "")
        span = li.find("span", "")
        attachment_download_time = span.get_text(strip = True)

        download_file = requests.get(attachment_href)
        script_root = os.path.dirname(os.path.abspath(__file__))
        subdir_path = os.path.join(script_root, "attachment")
        filepath = os.path.join(subdir_path, attachment_name)
        with open(filepath, "wb") as file:
            file.write(download_file.content)
        
        attachment_data = {
            "名称": attachment_name,
            "下载链接": attachment_href,
            "下载次数": attachment_download_time,
            "地址": filepath
        }
        return attachment_data
    else:
        return None