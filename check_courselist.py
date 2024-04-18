import sys
import time
from datetime import date, timedelta
import re

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import requests
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

driver.find_element(By.ID, 'Pop_15848').find_element(By.CLASS_NAME, 'iCheckbox').click()

driver.find_element(By.NAME, 'ID').send_keys('cloudfishh')
driver.find_element(By.NAME, 'PW').send_keys('q1w2e3^@!@')
driver.find_element(By.CLASS_NAME, 'btn-login').click()
time.sleep(1)

course_list = pd.DataFrame([], columns=['type', 'title', 'class', 'time (h)'])

pagenum_list = [16, 4]  # [normal, theme]
# url_courselist = [f'https://gie.hunet.co.kr/Lecture/OnlineUX?category1=2&customNotIncategory=3#processLevel=&requiredType=&refundType=&contentsTime=&credit=&price=&sortColumn=best&sortDirection=desc&sortDefautlDirection=desc&shape=0&targetTypeNo=&categoryNo=0&ProcessType2=&onlyCpCdCategory=&category1=2&category2=&category3=&invitationType=&notInProcessType2=&customInCategory=&customNotInCategory=3&isGroup=Y&pageIndex={page}&totalCount=0&searchText=&PageSize=20',
#                   f'https://gie.hunet.co.kr/Lecture/OnlineUX?category1=3&customNotIncategory=2#processLevel=&requiredType=&refundType=&contentsTime=&credit=&price=&sortColumn=recent&sortDirection=desc&sortDefautlDirection=desc&shape=0&targetTypeNo=&categoryNo=0&ProcessType2=&onlyCpCdCategory=&category1=3&category2=&category3=&invitationType=&notInProcessType2=&customInCategory=&customNotInCategory=2&isGroup=Y&pageIndex={page}&totalCount=0&searchText=&PageSize=20']
page = 0

# 정규강좌
for page in range(pagenum_list[0]):
    url = f'https://gie.hunet.co.kr/Lecture/OnlineUX?category1=2&customNotIncategory=3#processLevel=&requiredType=&refundType=&contentsTime=&credit=&price=&sortColumn=best&sortDirection=desc&sortDefautlDirection=desc&shape=0&targetTypeNo=&categoryNo=0&ProcessType2=&onlyCpCdCategory=&category1=2&category2=&category3=&invitationType=&notInProcessType2=&customInCategory=&customNotInCategory=3&isGroup=Y&pageIndex={page}&totalCount=0&searchText=&PageSize=20'
    driver.get(url)
    time.sleep(1)

    html = requests.get(url, verify=False).text
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find('span', 'badge-subject')

    list_type, list_title, list_class, list_time = [], [], [], []
    raw_list_title = driver.find_elements(By.CLASS_NAME, 'subject')
    for r in raw_list_title:
        temp = r.get_attribute('textContent').split('\n')
        temp2 = [re.sub('  +', '', x) for x in temp]
        list_title.append(temp2[2])
        list_class.append(temp2[1])
    raw_list_time = driver.find_elements(By.CLASS_NAME, 'timeShowYn')
    for r in raw_list_time:
        list_time.append(re.sub(r'[^0-9]', '', r.text))
    for i in range(len(raw_list_title)):
        list_type.append('정규강좌')

    df_temp = pd.DataFrame({'type': list_type,
                            'title': list_title,
                            'class': list_class,
                            'time (h)': list_time})

    course_list = pd.concat([course_list, df_temp])

# 테마강좌
for page in range(pagenum_list[1]):
    url = f'https://gie.hunet.co.kr/Lecture/OnlineUX?category1=3&customNotIncategory=2#processLevel=&requiredType=&refundType=&contentsTime=&credit=&price=&sortColumn=recent&sortDirection=desc&sortDefautlDirection=desc&shape=0&targetTypeNo=&categoryNo=0&ProcessType2=&onlyCpCdCategory=&category1=3&category2=&category3=&invitationType=&notInProcessType2=&customInCategory=&customNotInCategory=2&isGroup=Y&pageIndex={page}&totalCount=0&searchText=&PageSize=20'
    driver.get(url)
    time.sleep(1)

    html = requests.get(url, verify=False).text
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find('span', 'badge-subject')

    list_type, list_title, list_class, list_time = [], [], [], []
    raw_list_title = driver.find_elements(By.CLASS_NAME, 'subject')
    for r in raw_list_title:
        temp = r.get_attribute('textContent').split('\n')
        temp2 = [re.sub('  +', '', x) for x in temp]
        list_title.append(temp2[2])
        list_class.append(temp2[1])
    raw_list_time = driver.find_elements(By.CLASS_NAME, 'timeShowYn')
    for r in raw_list_time:
        list_time.append(re.sub(r'[^0-9]', '', r.text))
    for i in range(len(raw_list_title)):
        list_type.append('테마강좌')

    df_temp = pd.DataFrame({'type': list_type,
                            'title': list_title,
                            'class': list_class,
                            'time (h)': list_time})

    course_list = pd.concat([course_list, df_temp])

course_list = course_list.reset_index(drop=True)
course_list.to_csv('course_list_240415.csv', encoding='utf-8-sig')
