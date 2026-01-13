from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
from data import Base_url
from log_in import log_in_ZhiHu
from config import create_chrome_options
from questions import extract_and_process_question
import time

def main():
    chrome_options = create_chrome_options()

    #使用选项启动浏览器
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        service = service,
        options = chrome_options
    )

    if not log_in_ZhiHu(driver):
        print("自动登录失败")
        time.sleep(5)
    #注意，自动登录存在人机验证问题，需要手动验证

    driver.get("https://www.zhihu.com/topic/19610354/unanswered")
    time.sleep(3)

    #启动后还可以调整大小
    # driver.maximize_window()#最大化
    # driver.set_window_size(800, 600)#改成800×600

    extract_and_process_question(driver)

    driver.quit()

if __name__ == "__main__":
    main()