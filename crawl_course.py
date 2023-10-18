import time
import re

import pyautogui
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup


# 과정리스트 로드
course_list = pd.read_csv('course_list_231018.csv', index_col=0)

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
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


# 어디까지 완료됐는지 체크
found = False
n_c = 0
while found is False:
    if course_list['수료여부'][n_c] == '수료':
        n_c += 1
    else:
        found = True
course_name = course_list['과정명'][n_c]

for c in range(course_list.shape[0]-n_c):
    c += n_c
    url_studying = 'https://gie.hunet.co.kr/Classroom/Studying'
    driver.get(url_studying)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # course_table = soup.select('tr')
    # course_table.remove(course_table[0])

    course_row = soup.find(string=course_list['과정명'][c]).parent.parent.parent.parent
    if course_row.find(string='학습중') is not None:
        course_key =  soup.find(string=course_list['과정명'][c]).parent.parent
        url_keys = course_row.findAll('a')[1]['onclick']
        url_keys = re.findall('"([^"]*)"', url_keys)
        url_study = f'http://study.hunet.co.kr/StudyLoadingCheck.aspx?processType={url_keys[0]}&courseType={url_keys[1]}&processCd={url_keys[2]}&studyProcessYear={url_keys[3]}&studyProcessTerm={url_keys[4]}&courseCd={url_keys[5]}&userId={url_keys[6]}&companySeq={url_keys[7]}&adminYn={url_keys[8]}&nextUrl={url_keys[9]}&returnUrl={url_keys[10]}'
        driver.get(url_study)
        driver.find_element(By.CLASS_NAME, 'btn.btn-study-sm.btn-primary').click()
        time.sleep(10)

        # switch window & continue studying
        window_list = driver.window_handles
        driver.switch_to.window(window_list[1])

        # webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
        try:
            driver.switch_to.alert.accept()
        except:
            pass
        driver.switch_to.window(window_list[1])

        # video spdup
        pyautogui.moveTo(200, 250, duration=0.5)
        for i in range(10):
            pyautogui.moveTo(200+i%2, 250+i%2, duration=0.5)
            pyautogui.click()
            time.sleep(0.5)

        # 비디오 속도 올리는 버튼 위치 (200, 250)