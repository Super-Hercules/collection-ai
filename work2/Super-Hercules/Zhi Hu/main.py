from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import time

def main():
    #创建浏览器选项
    chrome_options = Options()

    #添加各种选项
    chrome_options.add_argument("--start-maximized")#启动时最大化窗口
    chrome_options.add_argument("--disable-notifications")#禁用通知
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])#禁用日志
    # chrome_options.add_argument("--disable-gpu")# 关掉显卡加速
    # chrome_options.add_argument("--no-sandbox")# 关闭沙盒
    # chrome_options.add_argument("--disable-dev-shm-usage")# 解决共享内存问题
    # chrome_options.add_argument("--headless")#无头模式（不显示浏览器界面）

    #禁用图片加载以加速
    prefs = {
        "profile.default_content_setting_values": {"images": 1}#1=允许，2=禁止
    }
    chrome_options.add_experimental_option("prefs", prefs)

    #用户代理
    #chrome_options.add_argument()


    #使用选项启动浏览器
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        service = service,
        options = chrome_options
    )
    driver.get("https://www.zhihu.com/topic/19610354/hot")

    #启动后还可以调整大小
    # driver.maximize_window()#最大化
    # driver.set_window_size(800, 600)#改成800×600

    # driver.quit()

if __name__ == "__main__":
    main()

def search_for_question(driver):
    question_div = driver.find_element(By.CLASS_NAME, " css-0")
    questions = question_div.find_elements(By.CLASS_NAME, "List-item TopicFeedItem")
    return questions

def process_questions(questions):
    question_data = []
    for item in questions:
        title = item.find_element("ContentItem AnswerItem")

def extract_and_process_page_code(driver):
    #等待页面加载完成
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "ContentItem-title"))
    )
    #获取页面源代码
    page_source_code = driver.page_source
    soup = BeautifulSoup(page_source_code, "html.parser")