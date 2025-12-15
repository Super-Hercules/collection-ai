from extractor import extract_the_first_notice_page
from notice_processor import process_notice
from notice_processor import output_as_csv
from extractor import get_next_page
from bs4 import BeautifulSoup
from extractor import extract_notice_page

JWC_base_url = "https://jwch.fzu.edu.cn"

def main():
    current_page_url = JWC_base_url + "/jxtz.htm"
    current_page_content = extract_notice_page()
    soup = BeautifulSoup(current_page_content, "html.parser")
    notice_data = process_notice(soup)
    output_as_csv(notice_data)

    current_page_url = get_next_page(soup)
    while current_page_url:
        current_page_content = extract_notice_page(current_page_url)
        soup = BeautifulSoup(current_page_content, "html.parser")
        notice_data = process_notice(soup)
        output_as_csv(notice_data)