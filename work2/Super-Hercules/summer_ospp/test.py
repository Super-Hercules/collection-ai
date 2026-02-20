from headers_and_payload import projects_headers_and_payload
from output import output_application_pdf
from data import href
from data import url
from data import application_pdf_url
from bs4 import BeautifulSoup
import requests

payload, headers = projects_headers_and_payload()
response = requests.post(
    url = url,
    json = payload,
    headers = headers
)

text = response.text
print(f"状态码：\n{response.status_code}")

data = response.json()
projects = data["rows"]
item = projects[0]
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

application_pdf_id = str(data["orgProgramId"])
print(f"application_pdf_id: {application_pdf_id}")
output_application_pdf(application_pdf_id)

pro_data = {
    "project_name": pro_name,
    "project_difficulty": pro_difficulty,
    "technique_tag": tech_tag,
    # "project_discription": pro_discription,
    # "output_requirement": output_requirement
}
print(pro_data)