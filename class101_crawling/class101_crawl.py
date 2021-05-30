from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

browser = webdriver.Chrome(executable_path="./chromedriver.exe")
headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ',
                          '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36')}

# 로그인 창으로 이동
browser.maximize_window()
url = "https://class101.net/login?redirect=%2F"
browser.get(url)
time.sleep(2)

# 카카오 계정으로 하기
browser.find_element_by_xpath("""/html/body/div[1]/div/div[1]/main/div/div[1]/div/div/p/button""").click()
time.sleep(3)

user_id = '####'  # 각자 카카오계정 아이디
user_password = '####'  # 각자 카카오계정 비밀번호

element_id = browser.find_element_by_name("email")
element_id.send_keys(user_id)
element_password = browser.find_element_by_name("password")
element_password.send_keys(user_password)

browser.find_element_by_xpath("""
/html/body/div[1]/div[2]/div/div/div/div/div[2]/div/form/fieldset/div[8]/button[1]""").click()
time.sleep(10)

# ---------------------------- url 수집하는 구간. 1번만 실행하면 됩니다. 크롤링할 경우는 해당 영역 주석처리 -------------------------
# browser.get("https://class101.net/search?query=공예")
# time.sleep(5)
#
# body = browser.find_element_by_tag_name('body')
#
# while True:
#     height = browser.find_element_by_xpath("""/html/body/div[1]/div/div[1]/main/div""").size[
#         'height']  # (질문) .size['height']
#     body.send_keys(Keys.PAGE_DOWN)
#     body.send_keys(Keys.PAGE_DOWN)
#     body.send_keys(Keys.PAGE_DOWN)
#     body.send_keys(Keys.PAGE_DOWN)
#     time.sleep(5)
#     sizecheck = browser.find_element_by_xpath("""/html/body/div[1]/div/div[1]/main/div""").size['height']
#     if height == sizecheck:
#         break
#     height = sizecheck
#
# html = browser.page_source
# soup = BeautifulSoup(html, 'html.parser')
#
# # video의 url이 저장될 list
# linklists = []
#
# for ul in soup.find_all("ul", class_="sc-jcVebW cvuVvr"): # 가끔씩 끼어있는 광고성 컨텐츠의 url을 따올경우 표시한 후 continue
#     for link in ul.find_all("a"):
#         hreflink = link.get("href")
#         if hreflink[1:9] != 'products':
#             print('{} => 잘못된 양식의 하이퍼링크'.format(hreflink))
#             continue
#         else:
#             res_href = 'class101.net' + hreflink
#             print(res_href)
#             with open("클래스101_클래스url.txt", "a", encoding="utf-8-sig") as f:
#                 f.write("{}\n".format(res_href))
# ---------------------------- 여기까지 주석처리 -------------------------
with open("../클래스101_강의제목_만족도_리뷰수_후기.txt", "a", encoding="utf-8-sig") as r:
    r.write('{}\t{}\t{}\t{}\t{}\n'.format('강의명', '좋아요수', '댓글수', '댓글내용', '댓글날짜'))


with open("../클래스101_클래스url.txt", "r", encoding="utf-8-sig") as f:
    linklist = f.readlines()

    for index_n, link in enumerate(linklist):
        print('{}번째 url 작업중'.format(index_n + 1))
        link = 'https://' + link[:-1]
        # 저장해둔 url을 불러화 해당 페이지로 이동
        browser.get(link)
        time.sleep(4)

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 해당 클래스의 이름과 좋아요 수 크롤링
        class_name = soup.find("h2", class_="sc-dQppl jhzFzM ProductHeader__Title-sc-4rgr4k-2 jkmuZi").text
        likes_n = int(soup.find("button", class_="sc-hKgILt eFWsxw sc-bqyKva glLlrc SalesProductInfoTable__"
                                                 "WishlistButton-sc-1cslumm-2 bUSrQo").text)


        try:  # 가끔씩 리뷰가 없는 강의 페이지가 있으므로 예외처리
            review = soup.find("a",
                               class_="LinkComponent__StyledLink-gmbdn6-1 hYxdXM sc-dlfnbm sc-gKsewC bcaJjD BzhTL").get(
                "href")
            review_link = 'https://class101.net' + review
            browser.get(review_link)
            time.sleep(2)

            # 리뷰 개수 크롤링
            review_n = browser.find_element_by_xpath("""/html/body/div[1]/div/div[1]/main/div/div[2]""").text
            review_n = int(review_n[2:-9])



            # 리뷰창 계속 스크롤링 하는 부분
            body = browser.find_element_by_tag_name('body')
            while True:
                height = browser.find_element_by_xpath("""/html/body/div[1]/div/div[1]/main/div""").size[
                    'height']  # (질문) .size['height'] 이 부분이 잘 이해 안가요 => 댓글창 div의 전체 높이
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)
                sizecheck = browser.find_element_by_xpath("""/html/body/div[1]/div/div[1]/main/div""").size['height']
                if height == sizecheck:
                    break
                height = sizecheck

            # 리뷰 개수를 기반으로 xpath 반복문 활용. {}부분 참고
            for i in range(review_n):
                review_text = browser.find_elements_by_xpath(
                    """/html/body/div[1]/div/div[1]/main/div/div[3]/div/div[{}]/div[2]""".format(i + 1))[0].text  # 리뷰 내용
                review_date = browser.find_elements_by_xpath(
                    """/html/body/div[1]/div/div[1]/main/div/div[3]/div/div[{}]/div[1]/section/div[2]/div""".format(i+1))[0].text  # 리뷰 날짜

                # 강의명, 좋아요 수, 리뷰 개수, 리뷰내용 기록
                with open("../클래스101_강의제목_만족도_리뷰수_후기.txt", "a", encoding="utf-8-sig") as r:
                    print('{}\t{}\t{}\t{}\t{}\n'.format(class_name, likes_n, review_n, review_text, review_date))
                    r.write('{}\t{}\t{}\t{}\t{}\n'.format(class_name, likes_n, review_n, review_text, review_date))
        except:  # 강의 리뷰가 없는 경우. 강의명과 좋아요 수만 기록하고 리뷰 개수 부분과 리뷰 내용 부분은 none 문자로 대체
            with open("../클래스101_강의제목_만족도_리뷰수_후기.txt", "a", encoding="utf-8-sig") as r:
                r.write('{}\t{}\t{}\t{}\n'.format(class_name, likes_n, 'none', 'none', 'none'))
                print('{}\t{}'.format(class_name, likes_n))

