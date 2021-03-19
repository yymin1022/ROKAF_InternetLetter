from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import socket
from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__, static_url_path='/static')

name = '홍길동'
password = '1234'
title = '기본 제목'
content = '기본 본문'
friend = '친구의 친구'

@app.route('/sending', methods=['GET', 'POST'])
def sending():
    if request.method == 'GET':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(executable_path='/home/server/web/chromedriver', chrome_options=options)
        # 기본군사훈련단
        # url = 'https://www.airforce.mil.kr/user/indexSub.action?codyMenuSeq=156893223&siteId=last2&menuUIType=sub'
        # 정보통신학교
        url = 'http://airforce.mil.kr:8081/user/indexSub.action?codyMenuSeq=156894686&siteId=tong-new&menuUIType=sub'
        driver.get(url)
        driver.maximize_window()
        action = ActionChains(driver)
        driver.implicitly_wait(10)  

        # 정보 입력 창
        driver.find_element_by_css_selector('#searchName').send_keys('이규원') 
        driver.find_element_by_css_selector('#birthYear').send_keys('2000')
        driver.find_element_by_css_selector('#birthMonth').send_keys('04')
        driver.find_element_by_css_selector('#birthDay').send_keys('18')
        driver.find_element_by_css_selector('#btnNext').click()

        # 팝업에서 훈련병 선택
        driver.switch_to_window(driver.window_handles[1])
        driver.find_element_by_css_selector('.choice').click()

        # 편지쓰기
        driver.switch_to_window(driver.window_handles[0])
        driver.find_element_by_css_selector('#btnNext').click()

        # 인터넷편지 작성
        driver.find_element_by_xpath("//div[@class='UIbtn']/span[@class='wizBtn large Ngray normal btnR']").click()

        # 우편번호 및 주소(디폴트 유현욱 자취방)
        driver.find_element_by_css_selector('#senderZipcode').click()

        driver.switch_to_window(driver.window_handles[1])

        driver.find_element_by_css_selector('.popSearchInput').send_keys("상도로53길 45-6")

        driver.find_element_by_xpath("/html/body/form[2]/div/div/div[1]/div[1]/fieldset/span/input[2]").click()  # 검색 버튼
        driver.find_element_by_xpath(
            "/html/body/form[2]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/a/div/div").click()  # 첫번째 목록 선택 목록 여러개면 div[]로 선택 가능할듯

        driver.find_element_by_css_selector('#rtAddrDetail').send_keys("101호")
        driver.find_element_by_css_selector('.btn-bl').click()

        # 팝업 창에서 원래 창으로 이동
        driver.switch_to_window(driver.window_handles[0])

        driver.find_element_by_css_selector('#senderName').send_keys(name)  # 이름
        driver.find_element_by_css_selector('#relationship').send_keys(friend) # 관계
        driver.find_element_by_css_selector('#title').send_keys(title)  # 제목
        driver.find_element_by_css_selector('#contents').send_keys(content)  # 내용 #1200자
        driver.find_element_by_css_selector('#password').send_keys(password)  # 비밀번호 #비밀번호 다르게 해야될까? 아니면 master key마냥 하나로 쭉 가도 안전할까?
        driver.find_element_by_css_selector('.submit').click()  # 작성 완료

        cur_url = driver.current_url  # 현재 페이지 주소 저장
        print(driver.current_url)
        print(cur_url)  # 현재 페이지 url 출력

        if (cur_url.find('saveEmailSuccess') != -1):  # 현재 페이지 url에 saveEmailSuccess가 없다면
            return '<h1>success</h1>'
        else:
            return '<h1>ERROR... Pleas retry</h1>'

        # 근데 이게 가끔 작성 완료가 안될 때가 있거든? 그걸 어떻게 예외 처리해야할지 고민중...
        # driver.find_element_by_xpath(
        #    "/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div[2]/span/input").click()  # 목록으로
    else:
        return render_template('main.html')

@app.route('/', methods=['GET', 'POST'])
def missionComplete():
    global name
    global title
    global password
    global content
    global friend
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        password = request.form['password']
        friend = request.form['relation']
        content = request.form['content']
        return render_template('test.html')
    else:
        return render_template('main.html')

if __name__ == '__main__':
    IP = str(socket.gethostbyname(socket.gethostname()))
    print(IP)
    app.run(host='0.0.0.0', port=5000, debug=False)
    app.run()

