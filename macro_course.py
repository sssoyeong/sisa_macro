from util import *


driver = driver_start()
login(driver, 'soyeongp', 'q1w2e3^@!@')
course_list = load_csv_all()
soup = load_studying_list(driver)


"""
c = 349, [2023 휴넷공인중개사-2차] 부동산공시법-기본이론

c = 363, 2020 재경관리사 한 번에 착 붙는 재무회계 문제풀이

"""
c = 349
# for c in course_list.index:
frame_type = course_list['frame'][c]
course_name = course_list['과정명'][c]
course_row = soup.find(string=course_name).parent.parent.parent.parent
course_key =  soup.find(string=course_name).parent.parent

if course_row.find(string='학습중') is not None:
    url_keys = course_row.findAll('a')[1]['onclick']
    url_keys = re.findall('"([^"]*)"', url_keys)
    url_study = f'http://study.hunet.co.kr/StudyLoadingCheck.aspx?processType={url_keys[0]}&courseType={url_keys[1]}&processCd={url_keys[2]}&studyProcessYear={url_keys[3]}&studyProcessTerm={url_keys[4]}&courseCd={url_keys[5]}&userId={url_keys[6]}&companySeq={url_keys[7]}&adminYn={url_keys[8]}&nextUrl={url_keys[9]}&returnUrl={url_keys[10]}'
    driver.get(url_study)
    print(f'[{time.strftime("%m/%d %H:%M:%S")}]:    START, "{course_name}"')

    keep_course = True
    while keep_course is True:
        if frame_type == 'frame':
            keep_course = studying_frame(driver, url_study)
        elif frame_type == 'iframe':
            keep_course = studying_iframe(driver, url_study)
        else:
            pass

# driver.switch_to.window(driver.window_handles[1])