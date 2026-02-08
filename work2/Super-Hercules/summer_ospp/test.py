from random_headers_pool import get_random_headers
from data import href
from bs4 import BeautifulSoup
import requests

payload = {
    "programId": "255660173",
    "type": "org"
}

a, headers = get_random_headers()
response = requests.post(
    url = href,
    json = payload,
    headers = headers
)

print(f"状态码：\n{response.status_code}")

data = response.json()
pro_discription_json = data["programDesc"]
pro_discription = BeautifulSoup(pro_discription_json, "html.parser").text
print(pro_discription)
# outputrequirement = data["outputRequirement"]
# print(outputrequirement[1]["title"])