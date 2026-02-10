from random_headers_pool import get_random_headers
from data_process import requests_and_parse_data
from data import url
import json
import os

def main():
    payload, headers = get_random_headers()
    requests_and_parse_data(url, payload, headers)

if __name__ == "__main__":
    main()