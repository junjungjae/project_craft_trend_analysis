import pandas as pd
from konlpy.tag import Okt

# 긍정적인 리뷰만 모인 엑셀파일 불러오기
reviewList = pd.read_excel('./dataset/stemming_good_review(row_2774).xlsx')
reviewList.drop(reviewList.loc[reviewList.review.isna()].index, axis=0, inplace=True)
reviewList.drop(['sentiment'], axis=1, inplace=True)


def search_positive_sentiment(review_data):
    # 불용어 사전. 해당 단어들이 명사로서 검출되면 다음 명사를 검색함
    stopwords_list = ['더', '보', '게', '좀', '조금', '살짝', '자주', '수', '것', '듯', '근데',
                      '걸', '거', '때', '건', '가끔', '점', '그런데', '클래스', '입장', '제', '정말', '솔직', '좀', '듯',
                      '무', '면', '조금', '느낌', '뭔가', '지다', '해', '그게', '주시', '모습', '만', '가지',
                      '위주', '생각', '추가', '마', '전혀', '쉬', '쪼금', '부족', '고', '치', '휙휙', '떼', '도움',
                      '안', '날', '사람', '료', '순간', '가격', '다채로웠으', '선택', '저', '중간', '작업', '예측', '요', '놓치다', '별로',
                      '터', '시작', '아래', '신경', '볼', '함', '흐름', '경험', '네오', '쫌', '전', '늘', '해도', '환기', '강좌', '진', '초반',
                      '보고',
                      '있엇으', '챙', '햐', '성격', '사용', '취미', '그런데', '부분', '밖', '정신', '알', '기능', '결제', '근데', '코딩',
                      '접합', '확인', '그', '예상', '해주시', '진짜', '재', '제일', '넘버', '다소', '기대', '바로', '뒤죽박죽', '해소', '개인', '더',
                      '완성',
                      '안나오다', '다음', '아주', '아야', '알다', '햇던', '작가', '수도', '하니', '마치', '알기', '대해', '통해',
                      '쉬다', '좋다', '딩하']

    # 해당 단어 기준 앞과 뒤를 두번 검증하여 유의미한 명사가 도출되도록 함.
    search_word_list = ['빠르다', '감사', '알차다', '만족도', '성취감', '따르다', '구체적으로', '쉬다', '아주',
                        '자세하다', '알게', '좋다', '배우다', '꼼꼼하다', '쉽다', '피드백을', '가르치다', '따르다']

    # 긍정 댓글에서 분류하기 위한 2가지 카테고리 => 영상 설명, 결과물 만족 2가지 카테고리

    content_accord = ['댓글', '답변', '친절', '정보', '팁', '성취', '설명', '피드백', '꼼꼼', '차분', '자세히', '차근차근',
                      '디테일', '기법', '상세', '강의', '이해', '자세', '쉽다', '다양', '실용', '알차다', '구체',
                      '노하우', '알차다']

    product_accord = ['결과물', '디자인', '스타일', '퀄리티', '작품']

    result = ''

    front_escape_chk = 0  # 앞에서 명사 단어를 찾을 경우 1로 변환하여 반복문 탈출
    backsearch_in_chk = 0  # 뒤에서 명사 단어를 찾을 경우 1로 변환하여 반복문 탈출

    for fs in search_word_list:  # 단어 리스트의 단어들을 불러오며 앞에서 검색할 경우
        if front_escape_chk == 0:  # 유의미한 단어를 찾기 못했을 경우
            if fs in review_data:  # 리뷰 데이터 안에 해당 단어가 있을 경우
                fs_list = review_data.split(fs)  # 리스트 단어를 기준으로 split
                nouns = okt.nouns(str(fs_list[0]))  # 기준 단어의 앞에서 명사를 검색하므로 index 0 을 추출
                if nouns:
                    while len(nouns) != 0:  # 추출한 split list에 대해 검증 시행
                        if nouns[len(nouns) - 1] in stopwords_list:  # split한 단어 리스트에 stopword가 포함되있을 경우 제거
                            popword = nouns[len(nouns) - 1]
                            nouns.pop(nouns.index(popword))
                        else:  # 유의미한 단어를 찾았으므로 해당 값으로 result 설정 및 chk 변수 1로 설정하여 반복문 진입 못하게 설정
                            result = nouns[len(nouns) - 1]
                            front_escape_chk = 1
                            backsearch_in_chk = 1
                            break
                else:
                    result = fs

    if backsearch_in_chk == 0:  # 앞의 front search에서 유의미한 단어를 찾지 못했을 경우 진입
        for back_s in search_word_list:
            if back_s in review_data:
                back_s_list = review_data.split(back_s)
                nouns = okt.nouns(str(back_s_list[1]))  # 해당 단어의 뒤에서 검색해야 하므로 index 1 조회
                if nouns:
                    while len(nouns) != 0:
                        if nouns[len(nouns) - 1] in stopwords_list:
                            nouns.pop()
                        else:
                            result = nouns[len(nouns) - 1]
                            break
                else:
                    result = back_s

    # 각각의 카테고리에 포함되는 단어가 검색될 경우 해당 단어로 result 설정
    for ca in content_accord:
        if ca in review_data:
            # 강의 내용 칭찬
            result = ca

    for pa in product_accord:
        if pa in review_data:
            # 재료, 완성 결과물 관련 칭찬
            result = pa

    if result in content_accord:
        return 'content prefer', result

    if result in product_accord:
        return 'product prefer', result

    return 'etc prefer', result  # 너무 세세한, 빈도가 적은 단어들로 인해 검출이 되지 못한 경우 etc 로 분류


cnt = 0  # 감정분석 분류가 진행된 댓글 카운트
okt = Okt()  # 형태소 분석 객체

content_n = 0  # 컨텐츠 카테고리로 분류된 댓글 카운트
product_n = 0  # 제품 카테고리로 분류된 댓글 카운트
etc_n = 0  # 기타(카테고리 분류가 불가능한)로 분류된 댓글 카운트

for i in range(len(reviewList)):
    content_title = reviewList.iloc[i, 0]  # 불러온 액셀 파일 중 타이틀 부분 조회
    review = reviewList.iloc[i, 1]  # 불러온 엑셀 파일 중 댓글 부분 조회
    prePro_review = search_positive_sentiment(review)  # 상단의 사용자 함수 통해 카테고리 출력
    if prePro_review is None:  # 댓글 분석이 불가능한 경우(유의미한 명사 추출 실패)
        continue
    else:  # 각각의 카테고리에 해당할 경우 카운트 증가
        cnt += 1
        if prePro_review[0] == 'product prefer':
            product_n += 1
        elif prePro_review[0] == 'content prefer':
            content_n += 1
        elif prePro_review[0] == 'etc prefer':
            etc_n += 1
            print(prePro_review, i)

print('---------------------------------')
print('긍정리뷰 분석 완료 수: {}'.format(cnt))
print('컨텐츠 관련 긍정적 댓글 수: {}\n제품 관련 긍정적 댓글 수: {}\n기타 긍정적 댓글 수: {}'.format(content_n, product_n, etc_n))
