import requests
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
subdir_path = os.path.join(script_dir, "application_pdf")
file_path = os.path.join(script_dir, "data.json")
os.makedirs(subdir_path, exist_ok = True)

def output_application_pdf(str_id, application_pdf_url):
    try:
        filepath = os.path.join(subdir_path, str_id + ".pdf")

        download_response = requests.get(application_pdf_url)
        with open(filepath, "wb") as file:
            file.write(download_response.content)
    except Exception as e:
        print(f"下载失败：{e}")

def output_json_data(json_data):
    json_str = json.dumps(json_data, ensure_ascii = False, indent = 2)#ensure_ascii不将汉文字符转化为ascii码，确保正确输出；indent空格缩进
    with open(file_path, "w", encoding = "utf-8") as json_file:
        json_file.write(json_str)