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
course_list = pd.read_csv('course_list_231025_frame.csv', index_col=0)
# course_list = pd.read_csv('course_list_prognostics_check.csv', index_col=0)
# course_list = pd.read_csv('course_list_231018.csv', index_col=0)
# course_list = pd.read_excel('시사점 과정리스트(231011)_차시.xlsx', header=3)
# course_list = course_list.drop(columns=['Unnamed: 0'])
# course_list.columns = ['대분류', '중분류', '소분류', '과정명', '학습시간']
# check = []
# for i in range(course_list.shape[0]):
#     check.append(i)
# course_list['수료여부'] = check
# course_list['frame'] =  check

# 어디까지 완료됐는지 체크
url_studying = 'https://gie.hunet.co.kr/Classroom/Studying'
driver.get(url_studying)
driver.implicitly_wait(10)

soup = BeautifulSoup(driver.page_source, 'html.parser')
course_table = soup.select('tr')
course_table.remove(course_table[0])

# for n_l in range(course_list.shape[0]):
#     for n_t in range(len(course_table)):
#         found = course_table[n_t].find(string=course_list['과정명'][n_l])
#         if found is not None:
#             print(course_table[n_t].find(string=course_list['과정명'][n_l]), n_t)
#             comp = course_table[n_t].find(string=course_list['과정명'][n_l]).parent.parent.parent.parent.findAll('strong')[-1]
#             if comp.string == '수료':
#                 course_list['수료여부'][n_l] = True
#             else:
#                 course_list['수료여부'][n_l] = False
# 
# drop = []
# for n_l in range(course_list.shape[0]):
#     if type(course_list['수료여부'][n_l]) != type(True):
#         drop.append(n_l)
# course_list = course_list.drop(index=drop)
# course_list.tail(5)

'''
# 사전진단 체크
course_list_csv = pd.read_csv('course_list_231020.csv', index_col=0)

check_tit = []
for i in range(course_list.shape[0]):
    check_tit.append(False)
course_list['prognostics'] = check_tit

skip = 0
tit = []
for cc in range(course_list_csv.shape[0]-skip):
    cc += skip
    c = course_list_csv.index[cc]
    course_row = soup.find(string=course_list_csv['과정명'][c]).parent.parent.parent.parent
    course_key =  soup.find(string=course_list_csv['과정명'][c]).parent.parent
    url_keys = course_row.findAll('a')[1]['onclick']
    url_keys = re.findall('"([^"]*)"', url_keys)
    url_study = f'http://study.hunet.co.kr/StudyLoadingCheck.aspx?processType={url_keys[0]}&courseType={url_keys[1]}&processCd={url_keys[2]}&studyProcessYear={url_keys[3]}&studyProcessTerm={url_keys[4]}&courseCd={url_keys[5]}&userId={url_keys[6]}&companySeq={url_keys[7]}&adminYn={url_keys[8]}&nextUrl={url_keys[9]}&returnUrl={url_keys[10]}'
    driver.get(url_study)
    try:
        driver.find_element(By.CLASS_NAME, 'prognostics-state-box')
        tit.append(c)
        print(c)
    except:
        pass

for i in tit:
    course_list['prognostics'][i] = True

course_list.to_csv('course_list_prognostics_check.csv', encoding='utf-8-sig')
'''

# frame 체크
frame = []
skip = 182
# for cc in range(course_list.shape[0]-skip):
for cc in range(182-skip):
    cc += skip
    c = course_list.index[cc]
    if course_list['prognostics'][c] == False:
        course_row = soup.find(string=course_list['과정명'][c]).parent.parent.parent.parent
        course_key =  soup.find(string=course_list['과정명'][c]).parent.parent
        url_keys = course_row.findAll('a')[1]['onclick']
        url_keys = re.findall('"([^"]*)"', url_keys)
        url_study = f'http://study.hunet.co.kr/StudyLoadingCheck.aspx?processType={url_keys[0]}&courseType={url_keys[1]}&processCd={url_keys[2]}&studyProcessYear={url_keys[3]}&studyProcessTerm={url_keys[4]}&courseCd={url_keys[5]}&userId={url_keys[6]}&companySeq={url_keys[7]}&adminYn={url_keys[8]}&nextUrl={url_keys[9]}&returnUrl={url_keys[10]}'
        driver.get(url_study)

        # soup_temp = BeautifulSoup(driver.page_source, 'html.parser')
        # study_completion = soup_temp.find(string='설문/후기작성').parent.parent.parent
        # study_completion.findAll('a')[0]
        try:
            driver.find_element(By.XPATH, '//*[@id="div_survey_alarm_Contents"]/a').click()
        except:
            pass

        driver.find_element(By.CLASS_NAME, 'btn.btn-study-sm.btn-primary').click()

        # switch window
        window_list = driver.window_handles
        driver.switch_to.window(window_list[1])
        time.sleep(2)

        # alert accept (continue video)
        try:
            driver.switch_to.alert.accept()
        except:
            pass
        driver.switch_to.window(window_list[1])

        try:
            driver.find_element(By.TAG_NAME, 'iframe')
            course_list['frame'][c] = 'iframe'
        except:
            driver.find_element(By.TAG_NAME, 'frame')
            course_list['frame'][c] = 'frame'

        driver.close()
        driver.switch_to.window(window_list[0])
        print(course_list['과정명'][c], cc)

print(frame)

course_list['frame'] = frame

course_list.to_csv(f'course_list_{time.strftime("%y%m%d")}_frame_4.csv', encoding='utf-8-sig')

driver.quit()
