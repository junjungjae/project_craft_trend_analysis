import pandas as pd
from konlpy.tag import Okt

reviewList = pd.read_excel('./dataset/stemming_sorry_review.xlsx')
reviewList.drop(reviewList.loc[reviewList.review.isna()].index, axis=0, inplace=True)
reviewList.reset_index(inplace=True)
reviewList.drop('index', axis=1, inplace=True)


# search 기준으로 split 한 후, 앞을 찾아야 하면 맨 뒤에서 가장 가까운 Noun 을 찾고, 뒤를 찾아야 하면 맨 앞에서 가장 가까운 Noun 을 찾는다.
def search_negative_sentiment(review_data):
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
                      '안나오다', '다음', '아주', '아야', '알다', '햇던', '작가', '수도', '하니', '마치', '알기']

    # 해당 단어들은 문장의 끝에 나올 확률이 높으므로 해당 단어 기준 왼쪽을 탐색
    front_search = ['보이지', '아깝다', '충분하다않다', '더자세하다', '더좋다', '아쉽다',
                    '쓸데없다', '느리다', '빠르다', '면 좋다', '좋다것같다', '안되다',
                    '헤메다', ' 좋다듯하다', '부족하다', '더들어가다', '어렵다', '비싸', '빠르다것같다', '자주나가다', '그만',
                    '너무늦다', '부족하다', '부분', '당황', '안타깝다']

    # 해당 단어들은 문장의 중간, 초반부에 나올 확률이 높으므로 해당 단어 기준 오른쪽 탐색
    back_search = ['다만', '없다', '그런데', '충분하다않다', '조금 더', '근데', '쓸데없다', '솔직', '너무짧다']

    # 해당 단어들은 문장의 중간에 나올 확률이 높으므로 해당 단어 기준 양쪽 탐색
    binary_search = ['실망', '부족', '버거운', '것같다', '좋다것같다', '단점', '너무짧다', '어렵다',
                     '때문에', '보완', '섬세', '너무많다', '무리', '않다', '기다']

    # 실망 댓글에서 분류하기 위한 3가지 카테고리 => 영상 품질 실망, 컨텐츠 내용 실망, 재료 관련 실망 카테고리
    video_accord = ['버퍼링', '화질', '속도', '빠르다', '짧다', '보이지않다', '놓치다', '오류', '어둡다', '어두워지다',
                    '안들리다', '보이지', '안보이', '영상', '진도', '뚝뚝', '버퍼링', '스킵', '모양', '안들리다', '세밀',
                    '사이트', '과정', '하단', '확대', '보기', '감기', '초점', '안보이', '화질', '목소리', '평가',
                    '어두워지다', '클로즈업', '안보', '가까이', '화면', '모션', '자막', '오류', '각도']

    content_accord = ['힘들다', '어렵다', '구체적', '헷갈', '반복되다', '환기', '진행', '해소가', '뒤죽박죽',
                      '안나오다', '각인', '장식', '단어', '돈', '작품', '답', '답장', '설명', '방법', '듣기', '교재', '이해', '비용', '힘들다',
                      '어렵다', '깊이', '용이', '초보자', '피드백', '수업', '빠르다', '속도', '시간', '내용', '만들기', '답변', '정보', '진행',
                      '기법', '너무짧다', '강의', '반복되다', '예시', '처음', '앞']

    material_accord = ['촌스럽다', '얇다', '상품', '안오다', '구슬', '준비물', '분량',
                       '패키지', '안오다', '제품', '구성', '주문', '재료', '프린터']

    result = ''

    for fs in front_search:
        if fs in review_data:
            fs_list = review_data.split(fs)  # 해당 단어를 기준으로 split 수행. 이때 front search 에 해당하는 단어이므로 index 0 조회
            nouns = okt.nouns(str(fs_list[0]))
            if nouns:
                while len(nouns) != 0:  # 조회한 리스트의 명사에 대해 검증 수행. 불용어 리스트에 포함된 단어라면 제거하면서 가장 가까운 명사 추출
                    if nouns[len(nouns) - 1] in stopwords_list:
                        nouns.pop()
                    else:
                        result = nouns[len(nouns) - 1]
                        break
            else:
                result = fs

    for back_s in back_search:
        if back_s in review_data:
            back_s_list = review_data.split(back_s)  # 해당 단어를 기준으로 split 수행. 이때 back search 에 해당하는 단어이므로 index 1 조회
            nouns = okt.nouns(str(back_s_list[1]))
            if nouns:
                while len(nouns) != 0:
                    if nouns[len(nouns) - 1] in stopwords_list:
                        nouns.pop()
                    else:
                        result = nouns[len(nouns) - 1]
                        break
            else:
                result = back_s

    for bs in binary_search:
        if bs in review_data:
            bs_list = review_data.split(bs)
            nouns1 = okt.nouns(str(bs_list[0]))
            nouns2 = okt.nouns(str(bs_list[1]))
            while len(nouns1) != 0:
                if nouns1[len(nouns1) - 1] in stopwords_list:
                    nouns1.pop()
                else:
                    break

            while len(nouns2) != 0:
                if nouns2[len(nouns2) - 1] in stopwords_list:
                    nouns2.pop()
                else:
                    break

            # bs 에서 nouns1[-1]과 nouns2[0] 중 어느 것이 더 가까운 지 계산해서 더 가까운 것을 반환
            if len(nouns1) >= 1 and len(nouns2) == 0:
                result = nouns1[-1]
            elif len(nouns1) == 0 and len(nouns2) >= 1:
                result = nouns2[-1]
            else:
                result = bs

    # 각각의 카테고리에 단어들이 포함될 경우 해당 단어를 result로 설정
    for va in video_accord:
        if va in review_data:
            # 비디오 문제
            result = va

    for ca in content_accord:
        if ca in review_data:
            # 강의 내용 문제
            result = ca

    for ma in material_accord:
        if ma in review_data:
            # 비디오 문제
            result = ma

    if result in video_accord:
        return 'video problem', result

    if result in content_accord:
        return 'content problem', result

    if result in material_accord:
        return 'material problem', result


cnt = 0  # 감정분석 분류가 진행된 댓글 카운트
okt = Okt()  # 형태소 분석 객체
video_n = 0  # 영상 카테고리로 분류된 댓글 카운트
content_n = 0  # 컨텐츠 카테고리로 분류된 댓글 카운트
material_n = 0  # 재료 카테고리로 분류된 댓글 카운트

for i in range(len(reviewList)):
    content_title = reviewList.iloc[i, 0]  # 불러온 엑셀 파일 중 타이틀 부분 조회
    review = reviewList.iloc[i, 1]  # 불러온 엑셀 파일 중 댓글 부분 조회
    prePro_review = search_negative_sentiment(review)  # 사용자 함수를 통해 카테고리 반환
    if prePro_review is None:  # 감정분석이 불가능할 경우
        continue
    else:
        cnt += 1
        print(prePro_review, i)
        if prePro_review[0] == 'material problem':
            material_n += 1
        elif prePro_review[0] == 'content problem':
            content_n += 1
        elif prePro_review[0] == 'video problem':
            video_n += 1

print('---------------------------------')
print('부정리뷰 분석 완료 수: {}'.format(cnt))
print('영상 관련 부정적 댓글 수: {}\n컨텐츠 관련 부정적 댓글 수: {}\n재료 관련 부정적 댓글 수: {}'.format(video_n, content_n, material_n))
