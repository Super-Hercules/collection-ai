from random_headers_pool import get_random_headers
from data_process import requests_and_parse_data
from output import output_json_data
from data import url

def main():
    json_payload, headers = get_random_headers()
    json_data = requests_and_parse_data(url, json_payload, headers)
    output_json_data(json_data)

if __name__ == "__main__":
    main()