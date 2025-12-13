from extractor import extract_the_first_notice_page
from notice_processor import process_notice

def main():
    current_page_content = extract_the_first_notice_page()
    processed_content = process_notice(current_page_content)
