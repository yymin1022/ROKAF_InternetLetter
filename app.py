from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import socket
from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__, static_url_path='/static')

name = '기본 이름'
password = 'defaultpw'
title = '기본 제목'
content = '기본 본문'
friend = '친구의 친구'

@app.route('/sending', methods=['GET', 'POST'])
def sending():
    if request.method == 'GET':
        # Initialize Web Driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()), options=options)

        # 기본군사훈련단
        url = 'https://www.airforce.mil.kr/user/indexSub.action?codyMenuSeq=156893223&siteId=last2&menuUIType=sub'
        # 정보통신학교
        # url = 'http://airforce.mil.kr:8081/user/indexSub.action?codyMenuSeq=156894686&siteId=tong-new&menuUIType=sub'
        driver.get(url)
        driver.maximize_window()
        action = ActionChains(driver)
        driver.implicitly_wait(10)  

        # Input Soldier Information
        driver.find_element_by_css_selector('#searchName').send_keys('김호규') 
        driver.find_element_by_css_selector('#birthYear').send_keys('2000')
        driver.find_element_by_css_selector('#birthMonth').send_keys('04')
        driver.find_element_by_css_selector('#birthDay').send_keys('27')
        driver.find_element_by_css_selector('#btnNext').click()

        # Click Search Soldier Button
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_css_selector('.choice').click()

        # Click Write Letter Button
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element_by_css_selector('#btnNext').click()

        # Click Input Address Button
        driver.find_element_by_xpath("//div[@class='UIbtn']/span[@class='wizBtn large Ngray normal btnR']").click()
        driver.find_element_by_css_selector('#senderZipcode').click()

        # Default Address is Soldier Himself
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_css_selector('.popSearchInput').send_keys("송백로 46")
        driver.find_element_by_xpath("/html/body/form[2]/div/div/div[1]/div[1]/fieldset/span/input[2]").click()
        driver.find_element_by_xpath("/html/body/form[2]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/a/div/div").click()
        driver.find_element_by_css_selector('#rtAddrDetail').send_keys("사서함 306-16호 3중대 3소대 17번 김호규 훈련병")
        driver.find_element_by_css_selector('.btn-bl').click()

        # Input Letter Contents
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element_by_css_selector('#senderName').send_keys(name)
        driver.find_element_by_css_selector('#relationship').send_keys(friend)
        driver.find_element_by_css_selector('#title').send_keys(title)
        driver.find_element_by_css_selector('#contents').send_keys(content)
        driver.find_element_by_css_selector('#password').send_keys(password)
        driver.find_element_by_css_selector('.submit').click()

        cur_url = driver.current_url

        if (cur_url.find('saveEmailSuccess') != -1):
            return '<h1>인편 등록이 완료되었습니다.</h1>'
        else:
            return '<h1>인편 등록에 실패하였습니다. 뒤로 이동하여 다시 시도해주세요.</h1>'
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
    app.run(host='0.0.0.0', port=8080, debug=False)
    app.run()

