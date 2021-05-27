from selenium import webdriver
import time as time
import getpass
from time import sleep
import re
from bs4 import BeautifulSoup
from collections import Counter

driver = webdriver.Chrome("D:\chrome_download\chromedriver.exe")  # Chromedriver PATH
driver.get("https://www.instagram.com/accounts/login/")
driver.maximize_window()

# 인스타그램 자동 로그인하기

# username = input("Input ID : ")  # crawling_ex_
# password = input("Input PWD : ")  # crawlingsample

username = 'junjungjae1996@gmail.com'
password = 'cnlgcsglcngu1996'

# 특히 getpass를 통해서 비밀번호 정보를 숨길 수도 있다. 잘 배워두자.

# hashTag = input("Input HashTag # : ")  # Search #
# hashTag = '운동'
time.sleep(3)

element_id = driver.find_element_by_name("username")
element_id.send_keys(username)
element_password = driver.find_element_by_name("password")
element_password.send_keys(password)

sleep(3)

##로그인버튼 클릭
driver.find_element_by_css_selector('.sqdOP.L3NKy.y3zKF').click()
sleep(3)

element_id = driver.find_element_by_name("username")
search_list = ['일러스트', 'digitalart', 'doodle', '손그림']
# search_tag = '그림'
write_n = 1500  # 불러올 해시태그의 개수
for tagcnt, search_tag in enumerate(search_list):
    n = 0

    driver.get("https://www.instagram.com/explore/tags/" + search_tag)

    # 첫 번째 게시물 클릭
    sleep(6)
    first_post = driver.find_element_by_class_name('eLAPa')
    first_post.click()

    time.sleep(4)

    with open("{}_태그.txt".format(search_tag), "w", encoding="utf-8-sig") as f:
        f.write('태그내용\t좋아요수\n')

    tag_word_n = []

    while True:
        try:
            tag_str = ''

            if int(write_n) > n:
                driver.find_element_by_link_text('다음').click()
                n = n + 1
                print(n)
                time.sleep(16)

                # 좋아요 수 수집하는 영역
                likes = driver.find_elements_by_css_selector('.zV_Nj')
                likes_text = likes[0].text
                likes_n = likes_text[4:-1]

                # 태그 이어붙이는 영역
                tags = driver.find_elements_by_css_selector('.xil3i')
                if tags is None:
                    print('태그 내용이 없습니다')
                    time.sleep(5)

                for i in tags:
                    store_tag = i.text
                    store_tag = re.sub(r"[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣|A-Z|a-z|0-9]", "", store_tag)
                    print(store_tag)
                    if store_tag != "#":
                        tag_word_n.append(store_tag)
                        tag_str = tag_str + store_tag + ' '
                print('---------------------------')

                # 수집한 내용 텍스트파일에 작성하는 영역
                with open("{}_태그.txt".format(search_tag), "a", encoding="utf-8-sig") as f:
                    f.write(
                        '{}\t{}\n'.format(tag_str, likes_n))

            else:
                if n >= int(write_n):
                    cnt = Counter(tag_word_n)
                    tagword_items = cnt.items()
                    with open("{}_카운터.txt".format(search_tag), "a", encoding="utf-8-sig") as c:
                        for words, cnt_n in tagword_items:
                            c.write("'{}': {}, ".format(words, cnt_n))
                    break
                else:
                    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

        except:
            if n >= int(write_n):
                break

