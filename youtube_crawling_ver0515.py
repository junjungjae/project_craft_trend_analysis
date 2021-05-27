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
import pickle

pickle_path = './exercise_URL_정재.txt'  # URL txt파일 경로

with open(pickle_path, 'rb') as lf:
    linklists = pickle.load(lf)
    print(linklists)

# column name은 그냥 나중에 제가 concat할때 붙이고 합칠게요.

browser = webdriver.Chrome(executable_path="D:\chrome_download\chromedriver.exe")
browser.maximize_window()

korean = re.compile('[ㄱ-ㅎ|가-힣]')

# 중간에 에러나면 숫자 복사해서
# for hreflink in linklists[인덱스숫자:] < 이렇게 만들어 주시고 돌리세요
for hreflink in linklists[2997:3000]:

    # 해당 print는 어느 url에서 error가 발생했는지 체크하는 포인트입니다.
    print("#####", linklists.index(hreflink), "번째 linklists 인덱스 작업 중 #####\n")

    url = "https://www.youtube.com" + hreflink
    browser.get(url)

    body = browser.find_element_by_tag_name('body')

    for i in range(2):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    height = \
    browser.find_element_by_xpath("""/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div""").size[
        'height']

    for j in range(10):
        for i in range(5):
            body.send_keys(Keys.PAGE_DOWN)

        time.sleep(0.5)
        sizecheck = browser.find_element_by_xpath(
            """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div""").size['height']

        if height == sizecheck:
            break
        height = sizecheck

    soup0 = browser.page_source
    soup = BeautifulSoup(soup0, 'html.parser')

    info1 = soup.find('div', {'id': 'info-contents'})

    # 댓글을 막아놓은 영상이 있기 때문에 예외처리를 꼭해준다.
    commentNumXpath = """//*[@id="count"]/yt-formatted-string"""
    try:
        commentNum = browser.find_element_by_xpath(commentNumXpath).text

    except NoSuchElementException as e:
        time.sleep(10)
        try:
            commentNum = browser.find_element_by_xpath(commentNumXpath).text
        except NoSuchElementException as e:
            print("댓글이 없는 동영상")
            continue

    commentNum = re.sub("[A-Z|a-z|ㄱ-ㅎ|가-힣|,| ]", "", commentNum)
    commentNum = float(commentNum)
    commentNum = int(commentNum)
    print("댓글 수: ", commentNum)

    videoName = info1.find('h1', {'class': 'title style-scope ytd-video-primary-info-renderer'}).text  # 영상제목
    if korean.search(str(videoName)):
        videoName = re.sub(r"[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣|A-Z|a-z|0-9| ]", " ", videoName)
        videoName = re.sub(" {2,}", " ", videoName)
        videoName = videoName.strip()
        print("동영상 제목: ", videoName)
    else:
        continue

    viewCountXpath = """//*[@id="count"]/ytd-video-view-count-renderer/span[1]"""
    viewCount = browser.find_element_by_xpath(viewCountXpath).text
    viewCount = re.sub(r"[가-힣|A-Z|a-z|,| ]", "", viewCount)
    viewCount = viewCount.strip()
    print("조회수: ", viewCount)

    goodCount = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[0].text  # 좋아요수
    if goodCount[-1] == '천':
        goodCount = re.sub("[천| ]", "", goodCount)
        goodCount = float(goodCount)
        goodCount *= 1000
    elif goodCount[-1] == '만':
        goodCount = re.sub("[만| ]", "", goodCount)
        goodCount = float(goodCount)
        goodCount *= 10000
    print("좋아요 수: ", goodCount)

    badCount = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[1].text  # 싫어요수
    if badCount[-1] == '천':
        badCount = re.sub("[천| ]", "", badCount)
        badCount = float(badCount)
        badCount *= 1000
    elif badCount[-1] == '만':
        badCount = re.sub("[만| ]", "", badCount)
        badCount = float(badCount)
        badCount *= 10000
    print("싫어요 수: ", badCount)

    videoDateXpath = """//*[@id="date"]/yt-formatted-string"""
    videoDate = browser.find_element_by_xpath(videoDateXpath).text
    videoDate = re.sub(" ", "", videoDate)
    print("게시일: ", videoDate)

    try:
        videoTextXpath = """//*[@id="description"]/yt-formatted-string/span[1]"""
        videoText = browser.find_element_by_xpath(videoTextXpath).text
        if korean.search(str(videoText)):
            videoText = re.sub(r"[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣|A-Z|a-z|0-9| ]", " ", videoText)
            videoText = re.sub(" {2,}", " ", videoText)
            videoText = videoText.strip()
            print("본문 내용: ", videoText)
        else:
            videoText = ''

    except:
        videoText = ''

    with open("0515운동유튜브_동영상테이블.txt", "a", encoding="utf-8-sig") as f:
        f.write(
            '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(videoName, videoDate, commentNum, viewCount, goodCount, badCount,
                                                      videoText, url))

    # 댓글이 100개가 넘는 경우, 하나의 동영상에서 최대 100개의 댓글만 가져오기

    count = 0
    for i in range(1, int(commentNum)):
        if count > 100:
            break
        try:
            commentXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{0}]/ytd-comment-renderer/div[1]/div[2]/ytd-expander/div/yt-formatted-string[2]""".format(
                i)
            comment = browser.find_element_by_xpath(commentXpath).text

            if korean.search(str(comment)):
                comment = re.sub(r"[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣|A-Z|a-z|0-9| ]", " ", comment)
                comment = re.sub(" {2,}", " ", comment)
                comment = comment.strip()
                p = re.compile(r"^[\d]{,2}[ ]{1}[\d]{,2}$")
                if p.match(comment):
                    continue
                dateXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{0}]/ytd-comment-renderer/div[1]/div[2]/div[1]/div[2]/yt-formatted-string/a""".format(
                    i)
                date = browser.find_element_by_xpath(dateXpath).text

                if comment != " ":
                    print(comment)
                    print(date)
                    with open("0515운동유튜브_댓글테이블.txt", "a", encoding="utf-8-sig") as f:
                        f.write('{}\t{}\t{}\n'.format(videoName, comment, date))
                    count += 1
            else:
                continue

        except NoSuchElementException as e:
            continue
        except:
            print("##### other error #####")
            continue