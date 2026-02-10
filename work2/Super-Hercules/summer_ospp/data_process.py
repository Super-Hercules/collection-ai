from data import pro_url
from data import application_pdf_url
from data import href
from bs4 import BeautifulSoup
import requests
import os

def requests_and_parse_data(url, json, headers):
    try:
        response = requests.post(
            url = url,
            json = json,
            headers = headers
        )

        text = response.text
        print(f"状态码：\n{response.status_code}")

        data = response.json()
        projects = data["rows"]

        script_dir = os.path.dirname(os.path.abspath(__file__))
        subdir_path = os.path.join(script_dir, "attachment")

        json_data = []
        for item in projects:
            pro_name = item["programName"]
            pro_difficulty = item["difficulty"]
            tech_tag = item["techTag"]
            pro_num = item["programCode"]

            attachment_id = item["orgProgramId"]
            attachment_url = application_pdf_url + attachment_id
            download_response = requests.get(attachment_url)

            try:
                filepath = os.path.join(subdir_path, pro_name)

                download_response = requests.get(attachment_url)
                with open(filepath, "wb") as file:
                    file.write(download_response.content)
            except Exception as e:
                print(f"下载失败：{e}")

            # href = pro_url + pro_num
            
            payload = {
                "programId": pro_num,
                "type": "org"
            }

            response = requests.post(
                url = href,
                json = payload,
                headers = headers
            )

            data = response.json()
            pro_discription_json = data["programDesc"]
            pro_discription = BeautifulSoup(pro_discription_json, "html.parser").text
            outputrequirement = data["outputRequirement"]

            # output_requirement = []
            output_requirement = ""
            for i in range(1, len(outputrequirement)):
                # output_requirement.append(outputrequirement[i]["title"])
                output_requirement += outputrequirement[i]["title"]

            pro_data = {
                "project_name": pro_name,
                "project_difficulty": pro_difficulty,
                "technique_tag": tech_tag,
                "project_discription": pro_discription,
                "output_requirement": output_requirement
            }

            json_data.append(pro_data)

        file_path = os.path.join(script_dir, "data.json")

        json_str = json.dumps(json_data, ensure_ascii = False, indent = 2)#ensure_ascii不将汉文字符转化为ascii码，确保正确输出；indent空格缩进
        with open(file_path, "w", encoding = "utf-8") as json_file:
            json_file.write(json_str)
        
    except Exception as exp:
        print(exp)