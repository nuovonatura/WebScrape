from datetime import date, timedelta
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import pandas as pd
import math
import time

SLEEP_DURATION = 15

# Obtain time period of 5 years

currDate = date.today()
StartDate = currDate - timedelta(days=1826)
strStartDate = StartDate.strftime("%Y%m%d")
strEndDate = currDate.strftime("%Y%m%d")

# Browser webdriver setup

testURL = "https://fund.eastmoney.com/data/fundranking.html#tall;c0;r;s1nzf;pn10000;ddesc;qsd" + strStartDate + ";qed" + strEndDate + ";qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"

opts = Options()
opts.add_argument("--headless")     # To opearte browser headless
browser = Firefox(options=opts)
browser.get(testURL)
print("Browser ready.")

# Storage initialization

size = {}
data = {}
temp1 = {}
temp2 = {}

typesDiv = browser.find_element(By.ID, "types")
typesLi = typesDiv.find_elements(By.TAG_NAME, "li")
for type in typesLi:
    text = type.text
    key = text[:text.find("(")]
    if key == "":
        continue
    totalNum = int(text[text.find("(") + 1:-1])
    size[key] = totalNum
    data[key] = []
    type.click()
    print(f"Obtaining {key} data...")
    time.sleep(SLEEP_DURATION)

    dbtable = browser.find_element(By.ID, "dbtable")
    thead = dbtable.find_element(By.TAG_NAME, "thead")
    thlist = thead.find_elements(By.TAG_NAME, "th")

    # 5 years
    top20 = math.ceil(totalNum / 5)
    btn = thlist[17].find_element(By.TAG_NAME, "a")
    btn.click()
    print("Obtaining 5-year data...")
    time.sleep(SLEEP_DURATION)
    tbody = dbtable.find_element(By.TAG_NAME, "tbody")
    trlist = tbody.find_elements(By.TAG_NAME, "tr")
    for i in range(top20):
        tdlist = trlist[i].find_elements(By.TAG_NAME, "td")
        code = tdlist[2].text
        val = (tdlist[2].text, tdlist[3].text, tdlist[4].text, tdlist[5].text, tdlist[6].text, tdlist[7].text[:-1], 
        tdlist[8].text[:-1], tdlist[9].text[:-1], tdlist[10].text[:-1], tdlist[11].text[:-1], tdlist[12].text[:-1], 
        tdlist[13].text[:-1], tdlist[14].text[:-1], tdlist[15].text[:-1], tdlist[16].text[:-1], tdlist[17].text[:-1])
        temp1[code] = val
    print("5-year data acquired.")

    # 3 years
    top25 = math.ceil(totalNum / 4)
    btn = thlist[14].find_element(By.TAG_NAME, "a")
    btn.click()
    print("Obtaining 3-year data...")
    time.sleep(SLEEP_DURATION)
    tbody = dbtable.find_element(By.TAG_NAME, "tbody")
    trlist = tbody.find_elements(By.TAG_NAME, "tr")
    for i in range(top25):
        tdlist = trlist[i].find_elements(By.TAG_NAME, "td")
        code = tdlist[2].text
        if temp1.get(code) == None:
            continue
        temp2[code] = temp1[code]
    temp1.clear()
    print("3-year data acquired.")

    # 2 years
    top33 = math.ceil(totalNum / 3)
    btn = thlist[13].find_element(By.TAG_NAME, "a")
    btn.click()
    print("Obtaining 2-year data...")
    time.sleep(SLEEP_DURATION)
    tbody = dbtable.find_element(By.TAG_NAME, "tbody")
    trlist = tbody.find_elements(By.TAG_NAME, "tr")
    for i in range(top33):
        tdlist = trlist[i].find_elements(By.TAG_NAME, "td")
        code = tdlist[2].text
        if temp2.get(code) == None:
            continue
        temp1[code] = temp2[code]
    temp2.clear()
    print("2-year data acquired.")

    # 1 year
    top50 = math.ceil(totalNum / 2)
    btn = thlist[12].find_element(By.TAG_NAME, "a")
    btn.click()
    print("Obtaining 1-year data...")
    time.sleep(SLEEP_DURATION)
    tbody = dbtable.find_element(By.TAG_NAME, "tbody")
    trlist = tbody.find_elements(By.TAG_NAME, "tr")
    for i in range(top50):
        tdlist = trlist[i].find_elements(By.TAG_NAME, "td")
        code = tdlist[2].text
        if temp1.get(code) == None:
            continue
        data[key].append(temp1[code])
    print("1-year data acquired.")

    print(f"{key} done. Start scraping the next type...")

    # Clear temp for next round
    temp1.clear()
    temp2.clear()
browser.quit()

print("Data scraping done.")
print("Start writing to file...")

with pd.ExcelWriter("Output.xlsx", engine="xlsxwriter", engine_kwargs={'options': {'string_to_numbers': True}}) as writer:
    col = ['基金代码', '基金简称', '日期', '单位净值', '累积净值', '日增长率', '近1周', '近1月', '近3月', '近6月', '近1年', '近2年', '近3年', '今年来', '成立来', '近5年']
    for (k, v) in data.items():
        df = pd.DataFrame.from_records(v, columns=col, coerce_float=True)
        df.to_excel(writer, sheet_name=k, freeze_panes=(1, 4), float_format=True)
        print(f"{k} sheet written.")

print("Write to file done.")

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