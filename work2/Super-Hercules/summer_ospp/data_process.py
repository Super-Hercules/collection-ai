from data import application_pdf_url
from data import href
from output import output_application_pdf
from bs4 import BeautifulSoup
import requests

def requests_and_parse_data(url, json_payload, headers):
    try:
        response = requests.post(
            url = url,
            json = json_payload,
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
            pro_num = item["programCode"]
            
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

            application_pdf_id = data["orgProgramId"]
            str_id = str(application_pdf_id)
            pdf_url = application_pdf_url + str_id
            output_application_pdf(str_id, pdf_url)

            # output_requirement = []
            output_requirement = ""
            for i in range(1, len(outputrequirement)):
                # output_requirement.append(outputrequirement[i]["title"])
                output_requirement += outputrequirement[i]["title"]

            pro_data = {
                "项目名": pro_name,
                "项目难度": pro_difficulty,
                "技术领域标签": tech_tag,
                "项目简述": pro_discription,
                "项目产出要求": output_requirement
            }

            json_data.append(pro_data)

        return json_data
        
    except Exception as exp:
        print(exp)