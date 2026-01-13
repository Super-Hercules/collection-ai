import time
from selenium.webdriver.common.by import By

def log_in_ZhiHu(driver):
    try:
        driver.get("https://www.zhihu.com/signin")
        time.sleep(3)

        try:
            password_login = driver.find_element(By.XPATH, "//div[contains(text(),'密码登录')]")
            password_login.click()
            time.sleep(3)
        except:
            pass

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("18977235550")
        password_input.send_keys("13633057065aA@")
        
        login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(),'登录')]")
        login_button.click()

        time.sleep(5)

        try:
            driver.find_element(By.CLASS_NAME, "Popover AppHeader-profileMenu")
            return True
        except:
            return False
            
    except Exception as exp:
        print(f"登录过程中出错: {exp}")
        return False