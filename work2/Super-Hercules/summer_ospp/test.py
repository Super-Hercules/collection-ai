from random_headers_pool import get_random_headers
from data import href
from data import url
from bs4 import BeautifulSoup
import requests

payload, headers = get_random_headers()
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
pro_num = ["programCode"]
pro_data = {
    "project_name": pro_name,
    "project_difficulty": pro_difficulty,
    "technique_tag": tech_tag,
    # "project_discription": pro_discription,
    # "output_requirement": output_requirement
}
print(pro_data)