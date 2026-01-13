from bs4 import BeautifulSoup
from random_headers_pool import get_random_headers
from data import JWC_base_url
import os
import csv
import requests

#处理content中的信息
def process_notice(soup):
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
                    href = JWC_base_url + href
                else:
                    href = JWC_base_url + f"/{href}"
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

        #如果有附件则提取附件并整合信息
        attachment_data = download_attachment_file(href)

        if attachment_data and attachment_data.get("名称"):
            notice_data.append({
                "日期": date,
                "通知部门": category,
                "标题": title,
                "链接": href,
                "附件": attachment_data.get("名称", ""),
                "下载链接": attachment_data.get("下载链接", ""),
                "下载次数": attachment_data.get("下载次数", "")
            })
        else:
            notice_data.append({
                "日期": date,
                "通知部门": category,
                "标题": title,
                "链接": href,
                "附件": "",
                "下载链接": "",
                "下载次数": ""
            })

    #返回
    return notice_data

#导出为csv文件
def output_as_csv(notice_data, filename = "FZU_JWC_notices.csv"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)
    fieldnames = ["序号", "日期", "通知部门", "标题", "链接", "附件", "下载链接", "下载次数"]
    file_exists = os.path.exists(filepath)

    #获取当前最大序号
    start_index = 1
    if file_exists:
        try:
            #只读模式"r"
            with open(filepath, "r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                existing_rows = list(reader)
                if existing_rows:
                    max_index = max([int(row["序号"]) for row in existing_rows if row["序号"].isdigit()], default=0)
                    start_index = max_index + 1
        except:
            start_index = 1
    
    #追加写入"a"
    with open(filepath, "a", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        
        #如果文件不存在或为空，写入表头
        if not file_exists or csv_file.tell() == 0:
            writer.writeheader()

        #写入所有数据
        for i, notice in enumerate(notice_data, start=start_index):
            row = {
                "序号": i,
                "日期": notice.get("日期", ""),
                "通知部门": notice.get("通知部门", ""),
                "标题": notice.get("标题", ""),
                "链接": notice.get("链接", ""),
                "附件": notice.get("附件", ""),
                "下载链接": notice.get("下载链接", ""),
                "下载次数": notice.get("下载次数", "")
            }
            writer.writerow(row)

#偷走通知里的附件，返回附件信息
def download_attachment_file(href):
    try:
        headers = get_random_headers()
        response = requests.get(href, headers = headers)
        soup = BeautifulSoup(response.content, "html.parser")
        attachment = soup.find("ul", style = "list-style-type:none;")

        if attachment:
            li_items = attachment.find_all("li")

            if li_items:
                attachment_names = []
                attachment_hrefs = []
                attachment_download_times = []
                attachment_files = []

                #确保附件目录存在
                script_root = os.path.dirname(os.path.abspath(__file__))
                subdir_path = os.path.join(script_root, "attachment")
                #自动创建目录
                os.makedirs(subdir_path, exist_ok=True)

                for i, li in enumerate(li_items, 1):
                    a = li.find("a")
                    span = li.find("span")

                    if a:
                        attachment_name = a.get_text(strip = True)
                        attachment_names.append(attachment_name)

                        attachment_href = a.get("href", "")
                        if attachment_href and not attachment_href.startswith(("http://", "https://")):
                            if attachment_href.startswith("/"):
                                attachment_href = JWC_base_url + attachment_href
                            else:
                                attachment_href = JWC_base_url + f"/{attachment_href}"
                        attachment_hrefs.append(attachment_href)

                        attachment_download_time = span.get_text(strip = True) if span else "0"
                        attachment_download_times.append(attachment_download_time)

                        try:
                            filepath = os.path.join(subdir_path, attachment_name)

                            download_response = requests.get(attachment_href)
                            with open(filepath, "wb") as file:
                                file.write(download_response.content)
                            attachment_files.append("下载成功")
                        except Exception:
                            attachment_files.append("下载失败")
                
                attachment_data = {
                    "名称": "；".join(attachment_names),
                    "下载链接": "；".join(attachment_hrefs),
                    "下载次数": "；".join(attachment_download_times),
                    "状态": "；".join(attachment_files)
                }
                return attachment_data
            else:
                return {}
        else:
            return {}
    except Exception as e:
        print(f"处理附件时发生错误: {e}")

    return {}