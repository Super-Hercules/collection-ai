import requests
from bs4 import BeautifulSoup

# headers = {
#     "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
# }
# for start_num in range(0, 250, 25):
#         response = requests.get(f"https://movie.douban.com/top250?start={start_num}", headers = headers)
#         print(response.status_code)
#         html = response.text
#         soup = BeautifulSoup(html, "html.parser")
#         all_titles = soup.findAll("span", attrs = {"class": "title"})
#         for title in all_titles:
#                 title_string = title.string
#                 if "/" not in title_string:
#                         print(title_string)



#通知主页面
# response = requests.get("https://jwch.fzu.edu.cn/jxtz.htm")
# page_text = response.text
# # print(page_text)
# with open("FZU_JWC.csv", "w", encoding = "utf-8") as file:
#     file.write(page_text)


#偷附件
response = requests.get("https://jwch.fzu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=1744984858&wbfileid=16732856")
# print(response.content)
with open("2025-2026学年各学院转专业实施细则.pdf", "wb") as file:
    file.write(response.content)