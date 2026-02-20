from headers_and_payload import projects_headers_and_payload
from data_process import requests_and_parse_data
from output import output_json_data
from data import url

def main():
    json_payload, headers = projects_headers_and_payload()
    json_data = requests_and_parse_data(url, json_payload, headers)
    output_json_data(json_data)

if __name__ == "__main__":
    main()