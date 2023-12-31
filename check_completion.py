import sys
import time
from datetime import date, timedelta
import re

import pyautogui
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup


# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
if sys.platform == 'darwin':
    chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=chrome_options)

# login page
url_home = 'https://gie.hunet.co.kr/Home'
driver.get(url_home)

driver.find_element(By.ID, 'Pop_14602').find_element(By.CLASS_NAME, 'iCheckbox').click()

driver.find_element(By.NAME, 'ID').send_keys('cloudfishh')
driver.find_element(By.NAME, 'PW').send_keys('q1w2e3^@!@')
driver.find_element(By.CLASS_NAME, 'btn-login').click()
time.sleep(1)

# 과정리스트 로드
yesterday = date.today() - timedelta(1)
course_list = pd.read_csv(f'course_list_{yesterday.strftime("%y%m%d")}.csv', index_col=0)

# 어디까지 완료됐는지 체크
url_studying = 'https://gie.hunet.co.kr/Classroom/Studying'
driver.get(url_studying)
driver.implicitly_wait(10)

soup = BeautifulSoup(driver.page_source, 'html.parser')

course_table = soup.find_all('tr')
course_table.remove(course_table[0])

for c in range(len(course_table)):
    temp = course_table[c].find_all('strong')
    found = temp[1].text
    if (sum(course_list['과정명'] == found) != 0) & (temp[3].text == '수료'):
        idx = course_list[course_list['과정명'] == found].index[0]
        course_list.at[idx, '수료여부'] = True

course_list.to_csv(f'course_list_{date.today().strftime("%y%m%d")}.csv', encoding='utf-8-sig')

driver.quit()