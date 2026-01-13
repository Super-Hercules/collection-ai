from selenium.webdriver.chrome.options import Options

def create_chrome_options():
    #创建浏览器选项
    chrome_options = Options()

    #添加各种选项
    chrome_options.add_argument("--start-maximized")#启动时最大化窗口
    chrome_options.add_argument("--disable-notifications")#禁用通知
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])#禁用日志
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')#禁用浏览器中的自动化控制特征
    # chrome_options.add_argument("--disable-gpu")#关掉显卡加速
    # chrome_options.add_argument("--no-sandbox")#关闭沙盒
    # chrome_options.add_argument("--disable-dev-shm-usage")#解决共享内存问题
    # chrome_options.add_argument("--headless")#无头模式（不显示浏览器界面）

    #禁用图片加载以加速
    prefs = {
        "profile.default_content_setting_values": {"images": 1}#1=允许，2=禁止
    }
    chrome_options.add_experimental_option("prefs", prefs)

    #用户代理
    #chrome_options.add_argument()

    return chrome_options

