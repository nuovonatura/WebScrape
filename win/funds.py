from datetime import date, timedelta
from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import numpy
import math
import time

# Sleep duration after each click on the button. Depends on the internet condition and CPU power.

SLEEP_DURATION = 15

# Change string to floating point.

def toNumber(string):
    if "--" in string:
        return numpy.nan
    else:
        return float(string)

# Obtain time period of 5 years

currDate = date.today()
StartDate = currDate - timedelta(days=1826)
strStartDate = StartDate.strftime("%Y%m%d")
strEndDate = currDate.strftime("%Y%m%d")

# Browser webdriver setup

testURL = "https://fund.eastmoney.com/data/fundranking.html#tall;c0;r;s1nzf;pn10000;ddesc;qsd" + strStartDate + ";qed" + strEndDate + ";qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"

opts = Options()
opts.add_argument("--headless")     # To opearte browser headless
srvc = Service(executable_path=".\msedgedriver.exe")
browser = Edge(service=srvc, options=opts)
browser.get(testURL)
print("Browser ready.")

# Storage initialization

size = {}
data = {}
temp1 = {}
temp2 = {}

typesDiv = browser.find_element(By.ID, "types")
typesLi = typesDiv.find_elements(By.TAG_NAME, "li")
for type in typesLi:        # Loops through each type including all
    text = type.text
    key = text[:text.find("(")]
    if key == "":
        continue
    totalNum = int(text[text.find("(") + 1:-1])
    size[key] = totalNum
    data[key] = []
    type.click()
    print(f"Scraping {key} data...")
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
        val = (tdlist[2].text, tdlist[3].text, tdlist[4].text, toNumber(tdlist[5].text), toNumber(tdlist[6].text), toNumber(tdlist[7].text[:-1]), 
        toNumber(tdlist[8].text[:-1]), toNumber(tdlist[9].text[:-1]), toNumber(tdlist[10].text[:-1]), toNumber(tdlist[11].text[:-1]), toNumber(tdlist[12].text[:-1]), 
        toNumber(tdlist[13].text[:-1]), toNumber(tdlist[14].text[:-1]), toNumber(tdlist[15].text[:-1]), toNumber(tdlist[16].text[:-1]), toNumber(tdlist[17].text[:-1]))
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
        df.astype({'基金代码': 'int32', '单位净值': 'float64', '累积净值': 'float64', '日增长率': 'float64', '近1周': 'float64', '近1月': 'float64', '近3月': 'float64', 
        '近6月': 'float64', '近1年': 'float64', '近2年': 'float64', '近3年': 'float64', '今年来': 'float64', '成立来': 'float64', '近5年': 'float64'})
        df.to_excel(writer, sheet_name=k, freeze_panes=(1, 4))
        print(f"{k} sheet written.")

print("Write to file done.")