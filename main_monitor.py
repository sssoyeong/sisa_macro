import pyautogui

# pyautogui.mouseInfo()     <-오류남
# (mac 기준) command + shift + 4 누르면 마우스 커서에 좌표 숫자 뜸.

time.sleep(1800)

# 마우스가 해상도 영역을 벗어나면 발생하는 오류를 끔 (특정 환경에서 오류 발생하는 경우 사용)
# pyautogui.FAILSAFE = False

pyautogui.moveTo(200, 200)    # 화면 해상도의 가로 200, 세로 200 픽셀 위치로 마우스 이동
pyautogui.click()    # 현재 마우스 커서 위치에서 마우스 클릭
pyautogui.click(660, 185)    # 특정 위치에 마우스 클릭 (순간이동하여 클릭함)
pyautogui.rightClick(560, 172)    # 특정 위치에 마우스 우클릭 (순간이동하여 클릭함)
pyautogui.moveTo(500, 500, duration=1)    # 이동하는 속도 1초 설정

pyautogui.typewrite('apple')    # 텍스트 입력
# 한글 입력시 pyautogui.typewrite('사과') 로 하면 unicode 한글은 입력이 안됨.
# 아래와 같이 클립보드에 복사해서 붙여넣기 하는 방식으로 진행
import pyperclip
pyperclip.copy('사과')
pyautogui.hotkey('ctrl', 'v')

pyautogui.hotkey('alt', 'f4')   # 단축키 입력 ('esc',  'enter', 'ctrl', 'tab' 등 한 개 또는 복수 키 입력)
pyautogui.typewrite(['enter'])    # 이렇게 키 입력할 수도 있음

# 윈도우키를 누르고 있는 상태에서 왼쪽 방향키 짧게 누르고 윈도우키를 뗌
pyautogui.keyDown('win')
pyautogui.press('left')
time.sleep(1.5)
pyautogui.keyUp('win')
time.sleep(0.5)

time.sleep(10)    # 10초 대기 (클릭 후 화면이 뜨기까지 등 반응시간 대기)

fw = pyautogui.getActiveWindow()
fw.close()   # 현재 활성화 상태인 창 닫기
