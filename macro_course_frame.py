import os
import sys
import time
import re

import pyautogui
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

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

driver.find_element(By.ID, 'Pop_14626').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_14602').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_14171').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_11243').find_element(By.CLASS_NAME, 'iCheckbox').click()
time.sleep(1)

driver.find_element(By.NAME, 'ID').send_keys('cloudfishh')
driver.find_element(By.NAME, 'PW').send_keys('q1w2e3^@!@')
driver.find_element(By.CLASS_NAME, 'btn-login').click()
time.sleep(1)


# # 어디까지 완료됐는지 체크
# found = False
# n_c = 0
# while found is False:
#     if course_list['수료여부'][n_c] == '수료':
#         n_c += 1
#     else:
#         found = True
# course_name = course_list['과정명'][n_c]
# c = 468

# 과정리스트 로드
course_list = pd.read_csv(f'course_list_{time.strftime("%y%m%d")}.csv', index_col=0)
# frame만 남기기
idx_drop = [i for i in course_list.index if (course_list['frame'][i] != 'frame')|(course_list['수료여부'][i] != 'FALSE')]
course_list = course_list.drop(index=idx_drop)
print(course_list.head(5))

# 마이페이지 리스트 긁어오기
url_studying = 'https://gie.hunet.co.kr/Classroom/Studying'
driver.get(url_studying)
driver.implicitly_wait(50)

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.set_window_size(1000, 1100)
driver.set_window_position(800, 50)

"""
c = 349, [2023 휴넷공인중개사-2차] 부동산공시법-기본이론

c = 363, 2020 재경관리사 한 번에 착 붙는 재무회계 문제풀이

"""
c = 349
for c in course_list.index:
    course_row = soup.find(string=course_list['과정명'][c]).parent.parent.parent.parent
    if course_row.find(string='학습중') is not None:
        keep_course = True
        course_key =  soup.find(string=course_list['과정명'][c]).parent.parent
        url_keys = course_row.findAll('a')[1]['onclick']
        url_keys = re.findall('"([^"]*)"', url_keys)
        url_study = f'http://study.hunet.co.kr/StudyLoadingCheck.aspx?processType={url_keys[0]}&courseType={url_keys[1]}&processCd={url_keys[2]}&studyProcessYear={url_keys[3]}&studyProcessTerm={url_keys[4]}&courseCd={url_keys[5]}&userId={url_keys[6]}&companySeq={url_keys[7]}&adminYn={url_keys[8]}&nextUrl={url_keys[9]}&returnUrl={url_keys[10]}'
        driver.get(url_study)
        print(f'[{time.strftime("%m/%d %H:%M:%S")}]:    START, "{course_list["과정명"][c]}"')

        while keep_course is True:
            if len(driver.window_handles) == 1:
                driver.find_element(By.CLASS_NAME, 'btn.btn-study-sm.btn-primary').click()
            time.sleep(5)

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
            time.sleep(2)

            # video spdup
            player_frame = driver.find_element(By.CSS_SELECTOR, 'html > frameset > frame:nth-child(1)')
            driver.switch_to.frame(player_frame)
            btn_div = driver.find_element(By.XPATH, '/html/body/form[1]/div[7]/div[1]/div[1]')
            driver.execute_script("arguments[0].setAttribute('style', 'display: block;')", btn_div)
            driver.execute_script("document.getElementsByTagName(\"video\")[0].playbackRate = 2;")
            try:
                spd = driver.find_element(By.XPATH, '/html/body/form[1]/div[7]/div[1]/div[1]/div[1]/span').text
                spd = float(re.sub(r'[^0-9]', '', spd))
                if spd < 2.0:
                    for i in range(10):
                        driver.find_element(By.XPATH, '//*[@id="movieSpdUp"]').click()
                        time.sleep(0.005)
            except:
                pass
            finally:
                driver.switch_to.default_content()

            # <다음 차시 바로가기> 화면 기다림
            wait_alert = WebDriverWait(driver, 1800)      # 30mins = 1800secs = 2배속이니까 1시간 분량 wait
            try:
                keep_going = True
                while keep_going:
                    driver.switch_to.window(driver.window_handles[1])
                    try:
                        player_frame = driver.find_element(By.CSS_SELECTOR, 'html > frameset > frame:nth-child(1)')
                        driver.switch_to.frame(player_frame)
                        driver.find_element(By.XPATH, '//*[@id="divNextInfoBox"]/div[2]/a').click()
                        keep_going = False
                    except:
                        pass

                # '다음 차시 바로가기' 누르면 '넘어가시겠습니까?' alert뜸
                wait_alert.until(expected_conditions.alert_is_present())
                driver.switch_to.alert.accept()     # window[1]에서 다음 차시 강의 진행됨
                try: 
                    driver.switch_to.alert.accept()   # 다 학습해야 넘어갈 수 있다 alert 뜨는 경우가 있음
                except:
                    pass

                # 진도율 체크
                driver.switch_to.window(driver.window_handles[0])
                driver.get(url_study)
                try:              # <학습을 모두 완료하셨습니다> 창 있으면 끄기
                    driver.find_element(By.XPATH, '//*[@id="div_survey_alarm_Contents"]/a').click()
                except:
                    pass
                score_ing = driver.find_element(By.CLASS_NAME, 'text-warning.number').text
                score_fin = driver.find_element(By.CLASS_NAME, 'text-legend').text
                score_ing = int(re.sub(r'[^0-9]', '', score_ing))
                score_fin = int(re.sub(r'[^0-9]', '', score_fin))
                if score_ing >= score_fin:
                    driver.switch_to.window(driver.window_handles[1])
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    keep_course = False 
                    print(f'[{time.strftime("%m/%d %H:%M:%S")}]: FINISHED, "{course_list["과정명"][c]}"')
                else:
                    print(f'       [{time.strftime("%H:%M:%S")}]: keep going')
            except:      # 30분 기다렸는데 alert 안 뜨면? 뭔가 영상 창에 문제가 생겼다거나? 일단 창을 끈다
                try:
                    driver.switch_to.alert.accept()     # alert 있으면 accept 해주기
                except:
                    pass
                w_list = driver.window_handles
                if len(w_list) > 1:                       # 영상 창이 그대로 남아있으면 (창 개수가 2개면)
                    driver.switch_to.window(w_list[1])    # 영상 창으로 switch
                    driver.close()                        # 영상 창 close
                driver.switch_to.window(window_list[0])
                driver.get(url_study)    # <학습하기> 창 돌아와서 새로고침

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
                    print(f'[{time.strftime("%m/%d %H:%M:%S")}]: FINISHED, "{course_list["과정명"][c]}"')
                else:
                    print(f'       [{time.strftime("%H:%M:%S")}]: keep going')

