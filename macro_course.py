import os
import sys
import time
import re
from datetime import date, timedelta

import pyautogui
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup


# 과정리스트 로드
# filename = [x for x in os.listdir() if x.startswith('course_list')]
# course_list = pd.read_csv(filename[-1], index_col=0)
# course_list = pd.read_csv('course_list_231025_frame_completion.csv', index_col=0)
course_list = pd.read_csv(f'course_list_{time.strftime("%y%m%d")}.csv', index_col=0)

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

driver.find_element(By.ID, 'Pop_14626').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_14602').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_14171').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_11243').find_element(By.CLASS_NAME, 'iCheckbox').click()
time.sleep(1)

driver.find_element(By.NAME, 'ID').send_keys('cloudfishh')
driver.find_element(By.NAME, 'PW').send_keys('q1w2e3^@!@')
driver.find_element(By.CLASS_NAME, 'btn-login').click()
time.sleep(1)

# iframe만 남기기
idx_drop = [i for i in course_list.index if (course_list['frame'][i] != 'iframe')|(course_list['수료여부'][i] == 'TRUE')]
course_list = course_list.drop(index=idx_drop)

# 마이페이지 리스트 긁어오기
url_studying = 'https://gie.hunet.co.kr/Classroom/Studying'
driver.get(url_studying)
driver.implicitly_wait(10)

soup = BeautifulSoup(driver.page_source, 'html.parser')

for c in course_list.index:
    course_row = soup.find(string=course_list['과정명'][c]).parent.parent.parent.parent
    if course_row.find(string='학습중') is not None:
        keep_course = True
        course_key =  soup.find(string=course_list['과정명'][c]).parent.parent
        url_keys = course_row.findAll('a')[1]['onclick']
        url_keys = re.findall('"([^"]*)"', url_keys)
        url_study = f'http://study.hunet.co.kr/StudyLoadingCheck.aspx?processType={url_keys[0]}&courseType={url_keys[1]}&processCd={url_keys[2]}&studyProcessYear={url_keys[3]}&studyProcessTerm={url_keys[4]}&courseCd={url_keys[5]}&userId={url_keys[6]}&companySeq={url_keys[7]}&adminYn={url_keys[8]}&nextUrl={url_keys[9]}&returnUrl={url_keys[10]}'
        driver.get(url_study)

        while keep_course is True:
            driver.find_element(By.CLASS_NAME, 'btn.btn-study-sm.btn-primary').click()
            time.sleep(5)

            # switch window
            window_list = driver.window_handles
            driver.switch_to.window(window_list[1])
            time.sleep(2)
            print('window switched')

            # alert accept (continue video)
            try:
                print('trying alert acception')
                driver.switch_to.alert.accept()
            except:
                pass
            driver.switch_to.window(window_list[1])

            # video spdup (비디오 멈추기 -> 배속버튼 생기게 한 후 배속 올리기 -> 비디오 재생 )
            driver.find_element(By.ID, 'main').click()
            driver.switch_to.frame("main")
            for i in range(10):
                driver.find_element(By.ID, 'video_dock_spdUp').click()
                time.sleep(0.05)
            driver.switch_to.default_content()
            driver.find_element(By.ID, 'main').click()  # 재생시작

            # <다음 차시로 이동하겠습니까?> alert 기다림
            wait_alert = WebDriverWait(driver, 1800)      # 30mins = 1800secs = 2배속이니까 1시간 분량 wait
            try:
                alert_switch = wait_alert.until(expected_conditions.alert_is_present())
                driver.switch_to.alert.accept()
                driver.switch_to.window(window_list[1])
                driver.close()      # 영상 창 close
                driver.switch_to.window(window_list[0])
                driver.refresh()    # <학습하기> 창 돌아와서 새로고침

                # <학습을 모두 완료하셨습니다> 창 있으면 끄기
                try:
                    driver.find_element(By.XPATH, '//*[@id="div_survey_alarm_Contents"]/a').click()
                except:
                    pass
                # <학습하기> 창에서 진도율 체크
                score_ing = driver.find_element(By.CLASS_NAME, 'text-warning.number').text
                score_fin = driver.find_element(By.CLASS_NAME, 'text-legend').text
                score_ing = int(re.sub(r'[^0-9]', '', score_ing))
                score_fin = int(re.sub(r'[^0-9]', '', score_fin))
                if score_ing >= score_fin:
                    keep_course = False
            except:     # 30분 기다렸는데 alert 안 뜨면? 뭔가 영상 창에 문제가 생겼다거나? 일단 창을 끈다
                try:
                    driver.switch_to.alert.accept()     # alert 있으면 accept 해주고
                    w_list = driver.window_handles
                    if len(w_list) > 1:                       # 영상 창이 그대로 남아있으면 (창 개수가 2개면)
                        driver.switch_to.window(w_list[1])    # 영상 창으로 switch
                        driver.close()                        # 영상 창 close 
                except:
                    driver.close()                      # alert 없으면 그냥 window[1] 닫아준다
                driver.switch_to.window(window_list[0])
                driver.refresh()    # <학습하기> 창 돌아와서 새로고침

                # <학습을 모두 완료하셨습니다> 창 있으면 끄기
                try:
                    driver.find_element(By.XPATH, '//*[@id="div_survey_alarm_Contents"]/a').click()
                except:
                    pass
                # <학습하기> 창에서 진도율 체크
                score_ing = driver.find_element(By.CLASS_NAME, 'text-warning.number').text
                score_fin = driver.find_element(By.CLASS_NAME, 'text-legend').text
                score_ing = int(re.sub(r'[^0-9]', '', score_ing))
                score_fin = int(re.sub(r'[^0-9]', '', score_fin))
                if score_ing >= score_fin:
                    keep_course = False

# driver.switch_to.window(driver.window_handles[0])