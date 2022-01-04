from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.set_headless(True)
assert opts.headless
browser = Firefox(options=opts)
browser.get('https://baidu.com')