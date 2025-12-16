from notice_processor import process_notice
from notice_processor import output_as_csv
from extractor import get_next_page
from bs4 import BeautifulSoup
from extractor import extract_notice_page
from data import JWC_base_url
import time

def main():
    current_page_url = JWC_base_url + "/jxtz.htm"
    current_page_content = extract_notice_page(current_page_url)
    soup = BeautifulSoup(current_page_content, "html.parser")
    notice_data = process_notice(soup)
    output_as_csv(notice_data)

    current_page_url = get_next_page(soup)
    counter = 1
    while current_page_url and counter < 50:
        current_page_content = extract_notice_page(current_page_url)
        soup = BeautifulSoup(current_page_content, "html.parser")
        notice_data = process_notice(soup)
        output_as_csv(notice_data)
        counter += 1
        # time.sleep(1)

if __name__ == "__main__":
    main()