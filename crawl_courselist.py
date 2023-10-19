import sys
import time
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
if sys.platform == 'darwin':
    chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=chrome_options)

# login page
url_home = 'https://gie.hunet.co.kr/Home'
driver.get(url_home)

driver.find_element(By.ID, 'Pop_14626').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_14602').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_14171').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_11243').find_element(By.CLASS_NAME, 'iCheckbox').click()
time.sleep(1)

driver.find_element(By.NAME, 'ID').send_keys('cloudfishh')
driver.find_element(By.NAME, 'PW').send_keys('q1w2e3^@!@')
driver.find_element(By.CLASS_NAME, 'btn-login').click()
time.sleep(1)

# 과정리스트 로드
course_list = pd.read_csv('course_list_231018.csv', index_col=0)

# 어디까지 완료됐는지 체크
url_studying = 'https://gie.hunet.co.kr/Classroom/Studying'
driver.get(url_studying)
soup = BeautifulSoup(driver.page_source, 'html.parser')
course_table = soup.select('tr')
course_table.remove(course_table[0])

for n_l in range(course_list.shape[0]):
    for n_t in range(len(course_table)):
        found = course_table[n_t].find(string=course_list['과정명'][n_l])
        if found is not None:
            print(course_table[n_t].find(string=course_list['과정명'][n_l]), n_t)
            comp = course_table[n_t].find(string=course_list['과정명'][n_l]).parent.parent.parent.parent.findAll('strong')[-1]
            course_list['수료여부'][n_l] = comp.string

course_list.to_csv(f'course_list_{time.strftime("%y%m%d")}.csv')

