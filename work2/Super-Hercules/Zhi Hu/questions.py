from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from save import save_to_csv
from data import Base_url
import time

def extract_href_content(driver, href):
    try:
        driver.get(href)
        time.sleep(5)

        try:
            content_button = driver.find_element(By.XPATH, "//button[@type='button' and contains(text(),'显示全部')]")
            content_button.click()
            time.sleep(5)
        except:
            pass

        page_source_code = driver.page_source
        soup = BeautifulSoup(page_source_code, "html.parser")

        # span = soup.find("span", class_ = "RichText ztext css-10o75c2")
        # span = soup.select_one("span.RichText.ztext")
        selectors = [
            "span.RichText.ztext.css-10o75c2",
            "span.RichText.ztext",
            "div.QuestionRichText",
            "div.QuestionHeader-detail"
        ]
        span = None
        for selector in selectors:
            span = soup.select_one(selector)
            if span:
                content = span.get_text(strip = True)

        #提取回答，从整个容器依次到回答文本和操作（即评论按钮），鉴于只需要提取十条回答，就注释掉滚动了
        #记得做评论
        answer = []
        # answer_container = soup.select("div.List-item > div.RichContent RichContent--unescapable", limit = 10)
        answer_container = soup.find_all("div", class_  = "ContentItem AnswerItem", limit = 10)
        for i, container in enumerate(answer_container):
            answer_body = container.find("span", class_ = "RichText ztext CopyrightRichText-richText css-10o75c2")
            # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", answer_item)
            answer_data = {
                "answer_index": i,
                "answer_content": "",
                # "comment": []
            }
            text = answer_body.text.strip()
            #text[:200]可以只取前两百字符
            answer_data["answer_content"] = text
            answer.append(answer_data)

            #提取评论
            # comment_button = answer_container.find("button", class_ = "Button ContentItem-action FEfUrdfMIKpQDJDqkjte Button--plain Button--withIcon Button--withLabel fEPKGkUK5jyc4fUuT0QP B46v1Ak6Gj5sL2JTS4PY RuuQ6TOh2cRzJr6WlyQp")
            # extract_comment(driver, comment_button)

        driver.back()
        return content, answer
    except Exception as exp:
        print(f"提取页面 {href} 时出错: {exp}")

#提取评论
def extract_comment(driver, comment_button):
    #滚动页面到元素处，block参数表示视窗对齐位置，此处为元素与视窗中部对齐
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_button)
    time.sleep(3)
    comment_button.click()
    pass

def extract_and_process_question(driver):
    try:
        #等待页面加载完成
        # WebDriverWait(driver, 10).until(
        #     expected_conditions.presence_of_element_located((By.CLASS_NAME, "ContentItem-title"))
        # )

        #获取页面源代码
        page_source_code = driver.page_source
        soup = BeautifulSoup(page_source_code, "html.parser")
        question_items = soup.find_all("div", class_ = "List-item TopicFeedItem", limit = 20)

        question = []
        for item in question_items:
            div = item.find("div", class_ = "QuestionItem-title")
            if div:
                a = div.find("a")
                if a:
                    href = a.get("href", "").strip()
                    href = Base_url + href
                    title = a.text.strip()
                else:
                    href = ""
                    title = ""
            else:
                continue

            question_content, answer = extract_href_content(driver, href)
            question_data = {
                "title": title,
                "content": question_content,
                "answer": answer
            }
            question.append(question_data)

        save_to_csv(question)
    except Exception as exp:
        print(f"处理问题时出错: {exp}")