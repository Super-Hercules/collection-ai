from data import pro_url
from data import application_pdf_url
from data import href
from bs4 import BeautifulSoup
import requests
import json

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

        json_data = []
        for item in projects:
            pro_name = item["programName"]
            pro_difficulty = item["difficulty"]
            tech_tag = item["techTag"]
            pro_num = ["programCode"]
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
            for i in range(1, 4):
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

        return json_data
        
    except Exception as exp:
        print(exp)