import pandas as pd
from konlpy.tag import Okt

reviewList = pd.read_excel('./dataset/stemming_good_review(row_2774).xlsx')
reviewList.drop(reviewList.loc[reviewList.review.isna()].index, axis=0, inplace=True)
reviewList.drop(['sentiment'], axis=1, inplace=True)


def search_problem(review_data):
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

    front_search = ['빠르다', '감사', '알차다', '만족도', '성취감', '따르다', '구체적으로', '쉬다', '아주',
                    '자세하다', '알게', '좋다', '배우다', '꼼꼼하다', '쉽다', '피드백을', '가르치다', '따르다']

    back_search = ['빠르다', '감사', '알차다', '만족도', '성취감', '따르다', '구체적으로', '쉬다', '아주',
                    '자세하다', '알게', '좋다', '배우다', '꼼꼼하다', '쉽다', '피드백을', '가르치다', '따르다']

    # 긍정 댓글에서 분류하기 위한 2가지 카테고리 => 영상 설명, 결과물 만족 2가지 카테고리

    content_accord = ['댓글', '답변', '친절', '정보', '팁', '성취', '설명', '피드백', '꼼꼼', '차분', '자세', '차근차근',
                      '디테일', '기법', '상세', '강의', '이해', '자세', '쉽다', '다양', '실용', '알차다', '구체', '노하우',
                      '자세', '단계', '유익', '체계', '정리', '세심', '꿀팁', '간결', '효율', '고퀄']

    product_accord = ['결과물', '디자인', '스타일', '퀄리티', '빨리', '예쁘다', '귀염', '색감', '색상', '귀엽다', '넉넉',
                      '유니크', '실용', '조합']


    result = ''

    front_escape_cnt = 0
    backsearch_in_cnt = 0

    for fs in front_search:
        if front_escape_cnt == 0:
            if fs in review_data:
                fs_list = review_data.split(fs)
                nouns = okt.nouns(str(fs_list[0]))
                # print(nouns[-1])
                if nouns:
                    while len(nouns) != 0:
                        if nouns[len(nouns) - 1] in stopwords_list:
                            popword = nouns[len(nouns) - 1]
                            nouns.pop(nouns.index(popword))
                        else:
                            # return nouns[len(nouns) - 1], 'front search -> okt', 'stopwords adapted'
                            result = nouns[len(nouns) - 1]
                            front_escape_cnt = 1
                            backsearch_in_cnt = 1
                            break
                else:
                    # return fs, 'front search -> return origin'
                    result = fs

    if backsearch_in_cnt == 0:
        for back_s in back_search:
            if back_s in review_data:
                back_s_list = review_data.split(back_s)
                nouns = okt.nouns(str(back_s_list[0]))
                # print(nouns[-1])
                if nouns:
                    while len(nouns) != 0:
                        if nouns[len(nouns) - 1] in stopwords_list:
                            nouns.pop()
                        else:
                            # return nouns[len(nouns) - 1], 'back search -> okt', 'stopwords adapted'
                            result = nouns[len(nouns) - 1]
                            break
                else:
                    # return back_s, 'back search -> return origin'
                    result = back_s

    for ca in content_accord:
        if ca in review_data:
            # 강의 내용 문제
            # return ca, 'return content'
            result = ca

    for pa in product_accord:
        if pa in review_data:
            # 비디오 문제
            # return pa, 'return material'
            result = pa

    if result in content_accord:
        return 'content prefer', result

    if result in product_accord:
        return 'product prefer', result

    return 'etc prefer', result


cnt = 0
okt = Okt()

content_n = 0
product_n = 0
etc_n = 0

for i in range(len(reviewList)):
    review = reviewList.iloc[i, 1]
    prePro_review = search_problem(review)
    if prePro_review is None:
        # cnt += 1
        # print(prePro_review, i)
        continue
    else:

        if prePro_review[0] == 'product prefer':
            product_n += 1
            cnt += 1
            print(prePro_review, i)
        elif prePro_review[0] == 'content prefer':
            content_n += 1
            cnt += 1
            print(prePro_review, i)
        elif prePro_review[0] == 'etc prefer':
            if prePro_review[1] == '':
                continue
            etc_n += 1
            cnt += 1
            print(prePro_review, i)

print('---------------------------------')
print('긍정리뷰 분석 댓글 수: {}'.format(cnt))
print('컨텐츠 관련 긍정적 댓글 수: {}\n결과물 관련 긍정적 댓글 수: {}\n기타 부분 긍정적 댓글 수: {}'.format(content_n, product_n, etc_n))
