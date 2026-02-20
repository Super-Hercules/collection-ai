from headers_and_payload import application_headers
from data import application_pdf_url
import requests
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
subdir_path = os.path.join(script_dir, "application_pdf")
file_path = os.path.join(script_dir, "data.json")
os.makedirs(subdir_path, exist_ok = True)

def output_application_pdf(application_id):
    try:
        filepath = os.path.join(subdir_path, application_id + ".pdf")

        application_pdf_id_url = application_pdf_url + application_id
        url = "https://summer-ospp.ac.cn/api/publicApplication"
        headers = application_headers(application_pdf_id_url)
        payload = {"proId": f"{application_id}"}
        download_response = requests.post(url = url, headers = headers, json = payload)
        print(f"download_response: {download_response.content}")
        with open(filepath, "wb") as file:
            file.write(download_response.content)
    except Exception as e:
        print(f"下载失败：{e}")

def output_json_data(json_data):
    json_str = json.dumps(json_data, ensure_ascii = False, indent = 2)#ensure_ascii不将汉文字符转化为ascii码，确保正确输出；indent空格缩进
    with open(file_path, "w", encoding = "utf-8") as json_file:
        json_file.write(json_str)