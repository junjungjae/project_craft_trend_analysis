from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import urllib.request
from bs4 import BeautifulSoup
import re


# chromedriver.exe 파일을 받아서 저장하시고, 해당 파일의 경로를 아래에 입력하세요.
browser = webdriver.Chrome(executable_path="D:\chrome_download\chromedriver.exe")

# 유튜브 브라우저로 이동
url = "https://www.youtube.com/"
browser.get(url)
browser.maximize_window()
time.sleep(5)

# 검색창에 커서클릭
elem = browser.find_element_by_xpath("""//*[@id="search"]""")  # (질문) find_element_by_xpath가 해당하는 객체의 전체 html 경로가 맞나요?

# 검색어 입력 후 검색
# 여러분이 각자 크롤링 할 부분을 나눠 놨으니, 검색어를 이곳에 입력하시면 됩니다.
elem.send_keys("악기 취미")

browser.find_element_by_xpath("""//*[@id="search-icon-legacy"]/yt-icon""").click()
time.sleep(3)
# 필터 클릭
browser.find_element_by_xpath("""//*[@id="container"]/ytd-toggle-button-renderer/a""").click()
time.sleep(3)
# '올해' 필터 클릭 - 저희는 게시한 지 1년 미만의 동영상만 사용합니다.
browser.find_element_by_xpath(
    """/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[5]/a/div/yt-formatted-string""").click()
time.sleep(3)

# --------------------------------------------------------------------------------------
# body pane을 자동 scroll해주는 코드
body = browser.find_element_by_tag_name('body')  # (질문) 해당 페이지의 처음과 끝의 body 태그를 잡는게 맞나요?

height = browser.find_element_by_xpath("""/html/body/ytd-app/div/ytd-page-manager/ytd-search""").size['height']  # (질문) .size['height'] 이 부분이 잘 이해 안가요
while True:
    for i in range(30):  # (질문) range 30까지 잡는 이유가 위에서부터 댓글 30개만 크롤링해오는게 맞나요?
        body.send_keys(Keys.PAGE_DOWN)
    sizecheck = browser.find_element_by_xpath("""/html/body/ytd-app/div/ytd-page-manager/ytd-search""").size['height']
    if height == sizecheck:
        break
    height = sizecheck

# --------------------------------------------------------------------------------------

# 스크롤이 끝까지 내려간 상태에서, video의 url 긁어오기
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# video의 url이 저장될 list
linklists = []

for element in soup.find_all("div", class_="text-wrapper style-scope ytd-video-renderer"):
    for link in element.find_all("a"):
        hreflink = link.get("href")
        if hreflink[1:6] == 'watch':  # 따온 링크에서 해당 부분을 watch로 바꿔주는 이유가 있을까요?
            linklists.append(hreflink)

print(linklists)

# 주의사항
# with open에서 "w"로 파일을 열었을 경우, 기존 파일 내용을 완전히 지우고 새로 쓴다는 의미입니다.
# 따라서 크롤링 중간에 에러가 났고, 에러부분을 건너뛴 후,
# 기존 tsv파일 밑으로 이어서 작업하고 싶으시다면
# 반드시 아래 with open ~ 부분 4줄을 지우거나, 주석처리한 후 코드를 실행해 주십시오.

# -----------------------------------------------------------------------------------------------------
with open("유튜브_댓글테이블.txt", "w", encoding="utf-8-sig") as f:
    f.write('동영상_제목\t댓글_내용\t댓글_작성시간\n')

with open("유튜브_동영상테이블.txt", "w", encoding="utf-8-sig") as f:
    f.write('동영상_제목\t동영상_게시일\t댓글_수\t조회수\t좋아요\t싫어요\t동영상_설명_본문\t동영상_URL\n')
# -----------------------------------------------------------------------------------------------------

browser = webdriver.Chrome(executable_path="D:\chrome_download\chromedriver.exe")
browser.maximize_window()

linklists_count = -1
for hreflink in linklists:

    linklists_count += 1

    # 해당 print는 어느 url에서 error가 발생했는지 체크하는 포인트입니다.
    print("#####" + str(linklists_count) + "번째 linklists 인덱스 작업 중 #####\n")

    url = "https://www.youtube.com" + hreflink
    browser.get(url)
    time.sleep(5)

    body = browser.find_element_by_tag_name('body')

    height = \
    browser.find_element_by_xpath("""/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div""").size[
        'height']
    while True:
        for i in range(1000):
            body.send_keys(Keys.PAGE_DOWN)

        time.sleep(1)
        sizecheck = browser.find_element_by_xpath(
            """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div""").size['height']

        if height == sizecheck:
            break
        height = sizecheck

    videoNameXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/h1/yt-formatted-string"""
    videoName = browser.find_element_by_xpath(videoNameXpath).text
    videoName = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9 ]", " ", videoName)
    videoName = re.sub(" {2,}", " ", videoName)  # 위에 부분은 정규표현식 써서 제거하는건 알겠는이 이 줄은 잘 이해가 안가요
    print("동영상 제목: " + videoName)

    videoDateXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[2]/yt-formatted-string"""
    videoDate = browser.find_element_by_xpath(videoDateXpath).text
    print("게시일: " + videoDate)

    commentNumXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[2]"""

    try:
        commentNum = browser.find_element_by_xpath(commentNumXpath).text

    except NoSuchElementException as e:  # 이 except 과정이 댓글이 없을 경우 다시 스크롤을 올려서 기록하는? 그런 과정이 맞나요?
        for i in range(1000):
            body.send_keys(Keys.PAGE_UP)
        time.sleep(1)
        commentNum = browser.find_element_by_xpath(commentNumXpath).text

    print("댓글 수: " + commentNum)

    viewCountXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[1]/ytd-video-view-count-renderer/span[1]"""
    viewCount = browser.find_element_by_xpath(viewCountXpath).text
    viewCount = re.sub(r"[가-힣, ]", "", viewCount)
    print("조회수: " + viewCount)

    goodCountXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a/yt-formatted-string"""
    goodCount = browser.find_element_by_xpath(goodCountXpath).text
    print("좋아요 수: " + goodCount)

    badCountXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[2]/a/yt-formatted-string"""
    badCount = browser.find_element_by_xpath(badCountXpath).text
    print("싫어요 수: " + badCount)

    videoTextXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[3]/ytd-video-secondary-info-renderer/div/ytd-expander/div/div/yt-formatted-string"""
    videoText = browser.find_element_by_xpath(videoTextXpath).text
    videoText = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9 ]", " ", videoText)
    videoText = re.sub(" {2,}", " ", videoText)
    print("본문 내용: " + videoText)

    with open("유튜브_동영상테이블.txt", "a", encoding="utf-8-sig") as f:
        f.write(
            '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(videoName, videoDate, commentNum, viewCount, goodCount, badCount,
                                                      videoText, url))

    i = 1
    for i in range(1, int(commentNum)):
        try:
            commentXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{0}]/ytd-comment-renderer/div[1]/div[2]/ytd-expander/div/yt-formatted-string[2]""".format(
                i)
            comment = browser.find_element_by_xpath(commentXpath).text
            comment = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9 ]", " ", comment)
            comment = re.sub(" {2,}", " ", comment)
            dateXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{0}]/ytd-comment-renderer/div[1]/div[2]/div[1]/div[2]/yt-formatted-string/a""".format(
                i)
            date = browser.find_element_by_xpath(dateXpath).text
            print(comment)
            print(date)

            if comment != " ":
                with open("유튜브_댓글테이블.txt", "a", encoding="utf-8-sig") as f:
                    f.write('{}\t{}\t{}\n'.format(videoName, comment, date))

        except NoSuchElementException as e:
            continue
        except:
            print("other error")