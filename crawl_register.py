import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument('--incognito')

driver = webdriver.Chrome(options=chrome_options)

# login
url_home = 'https://gie.hunet.co.kr/Home'
driver.get(url_home)

driver.find_element(By.ID, 'Pop_14602').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_14171').find_element(By.CLASS_NAME, 'iCheckbox').click()
driver.find_element(By.ID, 'Pop_11243').find_element(By.CLASS_NAME, 'iCheckbox').click()
time.sleep(1)

driver.find_element(By.NAME, 'ID').send_keys('cloudfishh')
driver.find_element(By.NAME, 'PW').send_keys('q1w2e3^@!@')
driver.find_element(By.CLASS_NAME, 'btn-login').click()
time.sleep(1)

# course list
url_courselist = 'https://gie.hunet.co.kr/Lecture/OnlineUX?category1=2&customNotIncategory=3#processLevel=&requiredType=&refundType=&contentsTime=&credit=&price=&sortColumn=best&sortDirection=desc&sortDefautlDirection=desc&shape=0&targetTypeNo=&categoryNo=0&ProcessType2=&onlyCpCdCategory=&category1=2&category2=&category3=&invitationType=&notInProcessType2=&customInCategory=&customNotInCategory=3&isGroup=Y&pageIndex=0&totalCount=0&searchText=&PageSize=20'
driver.get(url_courselist)
time.sleep(1)
html_courselist = driver.page_source

soup = BeautifulSoup(html_courselist, 'html.parser')
nextkeys = soup.body.find(text='수강신청하기').parent
print(type(nextkeys))
print(nextkeys.__dir__())


# onclick="fn_viewDetail('HLSP65285', '2023', '7342', 'hunet','51')
# https://gie.hunet.co.kr/Lecture/Detail?menuCategoryNo=2&processCd=HLSP65285&processYear=2023&processTerm=7342&cpCd=hunet&categoryNo=51