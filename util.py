import os
import sys
import time
import re

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup


def driver_start():
    # 브라우저 꺼짐 방지 옵션
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if sys.platform == 'darwin':
        chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def login(driver, id='cloudfishh', pw='q1w2e3^@!@'):
    # login page
    url_home = 'https://gie.hunet.co.kr/Home'
    driver.get(url_home)

    driver.find_element(By.ID, 'Pop_14626').find_element(By.CLASS_NAME, 'iCheckbox').click()
    driver.find_element(By.ID, 'Pop_14602').find_element(By.CLASS_NAME, 'iCheckbox').click()
    driver.find_element(By.ID, 'Pop_14171').find_element(By.CLASS_NAME, 'iCheckbox').click()
    driver.find_element(By.ID, 'Pop_11243').find_element(By.CLASS_NAME, 'iCheckbox').click()
    time.sleep(1)

    driver.find_element(By.NAME, 'ID').send_keys(id)
    driver.find_element(By.NAME, 'PW').send_keys(pw)
    driver.find_element(By.CLASS_NAME, 'btn-login').click()
    time.sleep(1)


def load_csv_all():
    # 과정리스트 로드
    course_list = pd.read_csv(f'course_list_{time.strftime("%y%m%d")}.csv', index_col=0)
    # frame만 남기기
    idx_drop = [i for i in course_list.index if (course_list['수료여부'][i] != 'FALSE')]
    course_list = course_list.drop(index=idx_drop)
    print(course_list.head(5))
    return course_list


def load_csv_frame(frame_type):
    # 과정리스트 로드
    course_list = pd.read_csv(f'course_list_{time.strftime("%y%m%d")}.csv', index_col=0)
    # frame만 남기기
    idx_drop = [i for i in course_list.index if (course_list['frame'][i] != frame_type)|(course_list['수료여부'][i] != 'FALSE')]
    course_list = course_list.drop(index=idx_drop)
    print(course_list.head(5))
    return course_list


def load_studying_list(driver):
    # 마이페이지 리스트 긁어오기
    url_studying = 'https://gie.hunet.co.kr/Classroom/Studying'
    driver.get(url_studying)
    driver.implicitly_wait(50)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.set_window_size(1000, 1100)
    driver.set_window_position(800, 50)
    return soup


def shutdown_comp_window(driver):
    try:
        driver.find_element(By.XPATH, '//*[@id="div_survey_alarm_Contents"]/a').click()
    except:
        pass


def spdup_frame(driver):
    player_frame = driver.find_element(By.CSS_SELECTOR, 'html > frameset > frame:nth-child(1)')
    driver.switch_to.frame(player_frame)
    btn_div = driver.find_element(By.XPATH, '/html/body/form[1]/div[7]/div[1]/div[1]')
    driver.execute_script("arguments[0].setAttribute('style', 'display: block;')", btn_div)
    try:
        # spd = driver.find_element(By.XPATH, '//*[@id="movieSpdTxt"]').text
        # spd = float(re.sub(r'[^0-9]', '', spd))
        # if spd < 2.0:
        for i in range(10):
            driver.find_element(By.XPATH, '//*[@id="movieSpdUp"]').click()
            time.sleep(0.005)
    except:
        pass
    finally:
        driver.switch_to.default_content()


def spdup_iframe(driver):
    # video spdup (비디오 멈추기 -> 배속버튼 생기게 한 후 배속 올리기 -> 비디오 재생 )
    driver.find_element(By.ID, 'main').click()
    driver.switch_to.frame("main")
    for i in range(10):
        driver.find_element(By.ID, 'video_dock_spdUp').click()
        time.sleep(0.05)
    driver.switch_to.default_content()
    driver.find_element(By.ID, 'main').click()  # 재생시작


def check_progress(driver, url_study):
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
        keep_course = True
        print(f'       [{time.strftime("%H:%M:%S")}]: keep going')
    return keep_course


def studying_frame(driver, url_study):
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
    spdup_frame(driver) 

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
        keep_course = check_progress(driver, url_study)
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
        keep_course = check_progress(driver, url_study)
    return keep_course


def studying_iframe(driver, url_study):
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

    spdup_iframe(driver)

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
        shutdown_comp_window(driver)    
        keep_course = check_progress(driver, url_study)
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
        shutdown_comp_window(driver)
        keep_course = check_progress(driver, url_study)
    return keep_course

