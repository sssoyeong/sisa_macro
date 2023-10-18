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
course_list = pd.read_excel('시사점 과정리스트(231011)_차시.xlsx', header=3)
course_list = course_list.drop(columns='Unnamed: 0')
course_list.columns = ['대분류', '중분류', '소분류', '과정명', '학습시간']

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

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

c = 12
for c in range(course_list.shape[0]):
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

        webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()

        # video spdup
        pyautogui.moveTo(200, 250, duration=0.5)
        for i in range(10):
            pyautogui.moveTo(200+i%2, 250+i%2, duration=0.5)
            pyautogui.click()
            time.sleep(0.5)

        # 비디오 속도 올리는 버튼 위치 (200, 250)