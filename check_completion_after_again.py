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
# yesterday = date.today() - timedelta(1)
# course_list = pd.read_csv(f'course_list_{yesterday.strftime("%y%m%d")}.csv', index_col=0)
course_list = pd.read_csv('course_list_231121.csv', index_col=0)
check = []
for i in range(course_list.shape[0]):
    check.append(False)
course_list['수료여부'] = check
course_list['수료여부'] = course_list['수료여부'].convert_dtypes('boolean')

# 완료한 것 체크
url_studyafter = 'https://gie.hunet.co.kr/Classroom/StudyAfter'
driver.get(url_studyafter)
driver.implicitly_wait(10)

for p in range(20):
    list_temp = driver.find_elements(By.CLASS_NAME, 'left')
    for c in range(len(list_temp)):
        found_name = list_temp[c].text
        if sum(course_list['과정명'] == found_name) == 0:
            pass
        else:
            idx = course_list[course_list['과정명'] == found_name].index[0]
            course_list.at[idx, '수료여부'] = True
            print(f'{idx:0>3} :  {found_name}')
    if p < 20:
        driver.find_element(By.CLASS_NAME, 'next').click()
        driver.implicitly_wait(10)
        time.sleep(10)


course_list.to_csv(f'course_list_{date.today().strftime("%y%m%d")}_new.csv', encoding='utf-8-sig')

driver.quit()