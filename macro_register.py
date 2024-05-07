import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# login page
url_home = 'https://gie.hunet.co.kr/Home'
driver.get(url_home)

driver.find_element(By.ID, 'Pop_15848').find_element(By.CLASS_NAME, 'iCheckbox').click()
time.sleep(1)

driver.find_element(By.NAME, 'ID').send_keys('sunghyun316')
driver.find_element(By.NAME, 'PW').send_keys('878737')
driver.find_element(By.CLASS_NAME, 'btn-login').click()
time.sleep(1)

# course list page
pagenum_normal = 16
pagenum_theme = 4

# page = 17
for page in range(pagenum_normal):
    # page += 17
    # (위) 정규강좌, (아래) 테마강좌
    # url_courselist = f'https://gie.hunet.co.kr/Lecture/OnlineUX?category1=2&customNotIncategory=3#processLevel=&requiredType=&refundType=&contentsTime=&credit=&price=&sortColumn=best&sortDirection=desc&sortDefautlDirection=desc&shape=0&targetTypeNo=&categoryNo=0&ProcessType2=&onlyCpCdCategory=&category1=2&category2=&category3=&invitationType=&notInProcessType2=&customInCategory=&customNotInCategory=3&isGroup=Y&pageIndex={page}&totalCount=0&searchText=&PageSize=20'
    url_courselist = f'https://gie.hunet.co.kr/Lecture/OnlineUX?category1=3&customNotIncategory=2#processLevel=&requiredType=&refundType=&contentsTime=&credit=&price=&sortColumn=recent&sortDirection=desc&sortDefautlDirection=desc&shape=0&targetTypeNo=&categoryNo=0&ProcessType2=&onlyCpCdCategory=&category1=3&category2=&category3=&invitationType=&notInProcessType2=&customInCategory=&customNotInCategory=2&isGroup=Y&pageIndex={page}&totalCount=0&searchText=&PageSize=20'

    driver.get(url_courselist)
    time.sleep(1)

    html_courselist = driver.page_source
    soup = BeautifulSoup(html_courselist, 'html.parser')

    num_course_page = len(soup.findAll(string='수강신청하기'))

    if num_course_page != 0:
        # num_course_page = 20
        for course in range(num_course_page):

            html_courselist = driver.page_source
            soup = BeautifulSoup(html_courselist, 'html.parser')
            url_keys = soup.body.find(string='수강신청하기').parent['onclick']
            url_keys = re.findall("'([^']*)'", url_keys)

            # register course page
            url_course_register = f'https://gie.hunet.co.kr/Lecture/Detail?menuCategoryNo=2&processCd={url_keys[0]}&processYear={url_keys[1]}&processTerm={url_keys[2]}&cpCd={url_keys[3]}&categoryNo={url_keys[4]}'
            driver.get(url_course_register)

            driver.find_element(By.CLASS_NAME, 'button-big.b-orange').click()
            time.sleep(1)
            try:
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(1)
            except:
                pass
            try:
                driver.find_element(By.ID, 'chkConsentToThirdPartySharingAgree1').click()
                time.sleep(1)
            except:
                pass
            driver.find_element(By.CLASS_NAME, 'button-big.b-black').click()
            time.sleep(2)

            driver.get(url_courselist)
            time.sleep(1)

