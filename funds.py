from datetime import date, timedelta
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import requests

# Obtain time period of 5 years

currDate = date.today()
StartDate = currDate - timedelta(days=1826)
strStartDate = StartDate.strftime("%Y%m%d")
strEndDate = currDate.strftime("%Y%m%d")

testURL = "https://fund.eastmoney.com/data/fundranking.html#tall;c0;r;s1nzf;pn10000;ddesc;qsd" + strStartDate + ";qed" + strEndDate + ";qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"

opts = Options()
opts.add_argument("--headless")     # To opearte browser headless
browser = Firefox(options=opts)
browser.get(testURL)
types = browser.find_element(By.ID, "types")
alltype = types.find_elements(By.TAG_NAME, "li")
for a in alltype:
    print(a.text)
browser.quit()

'''
# type: 全部 all，股票 gp，混合 hh，债券 zq，指数 zs，QDII qdii，LOF lof，FOF fof
# 循环8次获得每个type的数据

URL1y = "https://fund.eastmoney.com/data/fundranking.html#tall;c0;r;s1nzf;pn10000;ddesc;qsd" + strStartDate + ";qed" + strEndDate + ";qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"
URL2y = "https://fund.eastmoney.com/data/fundranking.html#tall;c0;r;s2nzf;pn10000;ddesc;qsd" + strStartDate + ";qed" + strEndDate + ";qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"
URL3y = "https://fund.eastmoney.com/data/fundranking.html#tall;c0;r;s3nzf;pn10000;ddesc;qsd" + strStartDate + ";qed" + strEndDate + ";qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"
URL5y = "https://fund.eastmoney.com/data/fundranking.html#tall;c0;r;sqjzf;pn10000;ddesc;qsd" + strStartDate + ";qed" + strEndDate + ";qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"

resp = requests.get(URL1y, stream=True)
# resp1y = requests.get(URL1y)
# resp2y = requests.get(URL2y)
# resp3y = requests.get(URL3y)
# resp5y = requests.get(URL5y)

html1y = BeautifulSoup(resp.content, "html.parser")
print("text:" + resp.text)
print("content:" + str(resp.content))
print("status code:" + str(resp.status_code))
print("encoding:" + str(resp.encoding))
print("headers:" + str(resp.headers))
print("raw:" + str(resp.raw))
print(html1y.prettify())
'''