# 필요한 패키지 불러오기


from selenium import webdriver
import time as time
import getpass
from time import sleep
import re

driver = webdriver.Chrome("C:\Caba2015\chromedriver.exe")  # Chromedriver PATH
driver.get("https://www.instagram.com/accounts/login/")
driver.maximize_window()

# 인스타그램 자동 로그인하기

username = getpass.getpass("Input ID : ")  # crawling_ex_
password = getpass.getpass("Input PWD : ")  # crawlingsample

# 특히 getpass를 통해서 비밀번호 정보를 숨길 수도 있다. 잘 배워두자.

hashTag = input("Input HashTag # : ")  # Search #

element_id = driver.find_element_by_name("username")
element_id.send_keys(username)
element_password = driver.find_element_by_name("password")
element_password.send_keys(password)

sleep(3)

##로그인버튼 클릭
driver.find_element_by_css_selector('.sqdOP.L3NKy.y3zKF').click()
sleep(3)
driver.get("https://www.instagram.com/explore/tags/" + hashTag)

# 첫 번째 게시물 클릭
sleep(6)
first_post = driver.find_element_by_class_name('eLAPa')
first_post.click()

time.sleep(4)

tags = driver.find_elements_by_css_selector('.xil3i')

tag_list = []
tag_n = 10000  # 불러올 해시태그의 개수
n = 1

# for i in tags:
#     store_tag = i.text
#     store_tag = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9]", "", store_tag)
#     print(store_tag)
#     tag_list.append(store_tag)
#     n += 1

while True:
    try:
        if int(tag_n) > n:
            driver.find_element_by_link_text('다음').click()
            time.sleep(4)
            tags = driver.find_elements_by_css_selector('.xil3i')
            for i in tags:
                print(n)
                store_tag = i.text
                store_tag = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9]", "", store_tag)
                print(store_tag)
                tag_list.append(store_tag)
                n += 1
        else:
            if n >= int(tag_n):
                break
            else:
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

    except:
        if n >= int(tag_n):
            break

print(len(tag_list))