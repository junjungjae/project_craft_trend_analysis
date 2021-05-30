from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re


# chromedrive가 있는 경로
browser = webdriver.Chrome(executable_path="../chromedriver.exe")

# 유튜브 브라우저로 이동
url = "https://www.youtube.com/"
browser.get(url)
browser.maximize_window()
time.sleep(5)

# 검색창에 커서클릭
elem = browser.find_element_by_xpath("""//*[@id="search"]""")

# 검색어 입력 후 검색버튼 클릭
elem.send_keys("검색할 단어")
browser.find_element_by_xpath("""//*[@id="search-icon-legacy"]/yt-icon""").click()
time.sleep(3)

# 필터 클릭
browser.find_element_by_xpath("""//*[@id="container"]/ytd-toggle-button-renderer/a""").click()
time.sleep(3)
# '올해' 필터 클릭
browser.find_element_by_xpath(
    """/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/
    div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/
    ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[5]/a/div/yt-formatted-string""").click()
time.sleep(3)

# --------------------------------------------------------------------------------------
# body pane을 자동 scroll해주는 코드
body = browser.find_element_by_tag_name('body')

# 현재 페이지의 높이
height = browser.find_element_by_xpath("""/html/body/ytd-app/div/ytd-page-manager/ytd-search""").size['height']
while True:
    for i in range(30):  # url 크롤링을 위해 키다운 입력을 통해 페이지 스크롤하는 과정. 너무 많아지면 버벅거려 30으로 제한
        body.send_keys(Keys.PAGE_DOWN)
    sizecheck = browser.find_element_by_xpath("""/html/body/ytd-app/div/ytd-page-manager/ytd-search""").size['height']
    if height == sizecheck: # 기존 height 입력값과 비교하여 같으면 break, 다르면 height 갱신 후 계속 진행
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
        hreflink = link.get("href") # url이 저장된 태그 검색 후 리스트에 추가
        if hreflink[1:6] == 'watch':
            linklists.append(hreflink)

print(linklists)

# ----------------------해당 형식을 가지는 메모장 저장하는 부분--------------------------------------------------
with open("../유튜브_댓글테이블.txt", "w", encoding="utf-8-sig") as f:
    f.write('동영상_제목\t댓글_내용\t댓글_작성시간\n')

with open("../유튜브_동영상테이블.txt", "w", encoding="utf-8-sig") as f:
    f.write('동영상_제목\t동영상_게시일\t댓글_수\t조회수\t좋아요\t싫어요\t동영상_설명_본문\t동영상_URL\n')
# -----------------------------------------------------------------------------------------------------

browser = webdriver.Chrome(executable_path="../chromedriver.exe")
browser.maximize_window()

linklists_count = -1
for hreflink in linklists:
    linklists_count += 1

    # 해당 print는 어느 url에서 error가 발생했는지 체크하는 포인트
    print("#####" + str(linklists_count) + "번째 linklists 인덱스 작업 중 #####\n")

    url = "https://www.youtube.com" + hreflink
    browser.get(url)
    time.sleep(5)

    body = browser.find_element_by_tag_name('body')

    height = \
    browser.find_element_by_xpath("""/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div""").size[
        'height']
    while True:
        for i in range(1000): # 1000번의 키다운을 통해 댓글 로딩
            body.send_keys(Keys.PAGE_DOWN)

        time.sleep(1)
        sizecheck = browser.find_element_by_xpath(
            """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div""").size['height']

        if height == sizecheck:
            break
        height = sizecheck

    videoNameXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/h1/yt-formatted-string"""
    videoName = browser.find_element_by_xpath(videoNameXpath).text
    videoName = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9 ]", " ", videoName) # 정규표현식 통해 제목의 특수문자나 기타 언어 제거
    videoName = re.sub(" {2,}", " ", videoName)
    print("동영상 제목: " + videoName)

    videoDateXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[2]/yt-formatted-string"""
    videoDate = browser.find_element_by_xpath(videoDateXpath).text
    print("게시일: " + videoDate)

    commentNumXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[2]"""

    try:
        commentNum = browser.find_element_by_xpath(commentNumXpath).text

    except NoSuchElementException as e: # 댓글 로딩 중 너무 오래 걸려 해당 element를 못찾은 경우로 다시 스크롤을 위로 올려 로딩 해소
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

    with open("../유튜브_동영상테이블.txt", "a", encoding="utf-8-sig") as f:
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
                with open("../유튜브_댓글테이블.txt", "a", encoding="utf-8-sig") as f:
                    f.write('{}\t{}\t{}\n'.format(videoName, comment, date))

        except NoSuchElementException as e:
            continue
        except:
            print("other error")