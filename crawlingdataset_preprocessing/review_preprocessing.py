class string_preprocessing:
    """
    파일 전처리를 위한 사용자 함수가 포함된 클래스

    cleanName(title_data) => C사이트 전용. 강좌명 맨 앞에 대괄호로 홍보 문구가 적혀있는 경우, 그 대괄호 문구를 제거
    stemming(string_data) => 문자열을 형태소에 따라 변환함으로서 분석에 용이하도록 함
    cleansingEmoticon(string_data) => 정규표현식을 이용해 문자열에 포함된 각종 특수기호 제거
    return_year(date_data) => C사이트 전용. 댓글 작성날짜로부터 연도 추출
    return_month(date_data) => C사이트 전용. 댓글 작성날짜로부터 월 추출
    """
    def cleanName(title_data):
        """
        :param: review_data => 강좌명 입력
        :return: 강좌명 맨 처음에 대괄호로 둘러쌓인 홍보 문구가 있을 경우 해당 대괄호 문구를 제거한 강좌명
        """
        import re
        title_data = re.sub('\[{1}.+\] ', '', title_data)
        title_data = title_data.strip()
        return title_data

    def stemming(string_data):
        """
        :param: string_data: 문자열 데이터
        :return: 입력받은 문자열 데이터를 형태소 원형으로 변환하여 출력
        """
        from konlpy.tag import Okt
        okt = Okt()
        malist5 = okt.pos(string_data, norm=False, stem=True)
        return_review = ''
        last = ''
        for pos in malist5:
            if pos[1] in ['Verb', 'Punctuation', 'Adverb']:
                return_review = return_review + pos[0] + ' '
            elif last == pos[1]:
                return_review = return_review + ' ' + pos[0]
            elif pos[1] == 'Josa':
                return_review = return_review + pos[0] + ' '
            else:
                return_review = return_review + pos[0]
            last = pos[1]
        return return_review

    def cleansingEmoticon(string_data):
        """
        :param: string_data: 문자열 데이터
        :return: 입력받은 문자열 데이터에서 글자, 숫자 및 공백을 제외한 모든 특수문자가 제거된 문자열
        """
        import re

        string_data = re.sub('[^\w ]', '', string_data)
        return string_data

    def return_year(date_data):
        split_date = date_data.split('.')
        return int(split_date[0])

    def return_month(date_data):
        split_date = date_data.split('.')
        return int(split_date[1])


class sentiment_preprocessing:
    """
    감정분석과 관련된 사용자 함수들을 포함하는 클래스

    stopwords_list => 불용어들이 포함된 리스트.
    neg_counter(data) => 리뷰에 포함된 부정적인 요소들을 취합해 부정점수 산출
    pos_counter(data) => 리뷰에 포함된 긍정적인 요소들을 취합해 긍정점수 산출
    return_sentiment(review_data) => 취합한 긍/부정 점수들을 바탕으로 good/sorry 판별. 긍/부정 점수가 모두 0점이면 예외처리 통해 not enough data 출력
    apply_sentiment(df) => 입력된 데이터프레임의 결측치 제거 및 인덱스 조정 후 return_sentiment 메서드를 통해 'good', 'sorry', 'not enough data' 부여
    return_goodreview_category(review_data) => 긍정 리뷰일 경우 해당 리뷰가 컨텐츠 칭찬, 제품 칭찬 어느 카테고리에 포함될지 출력
    return_sorryreview_category(review_data) => 부정 리뷰일 경우 해당 리뷰가 영상 문제, 재료 문제, 컨텐츠 문제 어느 카테고리에 포함될지 출력
    return_review_cat(df) => 리뷰와 sentiment 칼럼을 이용해 해당 리뷰가 어느 카테고리인지 출력
    """
    global stopwords_list
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

    def neg_counter(review_data):
        negative_n = 0
        global neg_front_search, neg_back_search, neg_binary_search, \
            neg_video_accord, neg_content_accord, neg_material_accord

        neg_front_search = ['보이지', '아깝다', '충분하다않다', '더자세하다', '더좋다', '아쉽다',
                            '쓸데없다', '느리다', '빠르다', '면 좋다', '좋다것같다', '안되다',
                            '헤메다', ' 좋다듯하다', '부족하다', '더들어가다', '어렵다', '비싸', '빠르다것같다', '자주나가다', '그만',
                            '너무늦다', '부족하다', '부분', '당황', '안타깝다']

        neg_back_search = ['다만', '없다', '그런데', '충분하다않다', '조금 더', '근데', '쓸데없다', '솔직', '너무짧다']

        neg_binary_search = ['실망', '부족', '버거운', '것같다', '좋다것같다', '단점', '너무짧다', '어렵다',
                             '때문에', '보완', '섬세', '너무많다', '무리', '않다', '기다']

        # 실망 댓글에서 분류하기 위한 3가지 카테고리 => 영상 품질 실망, 컨텐츠 내용 실망, 재료 관련 실망 카테고리
        neg_video_accord = ['버퍼링', '화질', '속도', '빠르다', '짧다', '보이지않다', '놓치다', '오류', '어둡다', '어두워지다',
                            '안들리다', '보이지', '안보이', '영상', '진도', '뚝뚝', '버퍼링', '스킵', '모양', '안들리다', '세밀',
                            '사이트', '과정', '하단', '확대', '보기', '감기', '초점', '안보이', '화질', '목소리', '평가',
                            '어두워지다', '클로즈업', '안보', '가까이', '화면', '모션', '자막', '오류', '각도']

        neg_content_accord = ['힘들다', '어렵다', '구체적', '헷갈', '반복되다', '환기', '진행', '해소가', '뒤죽박죽',
                              '안나오다', '각인', '장식', '단어', '돈', '작품', '답', '답장', '설명', '방법', '듣기', '교재', '이해', '비용', '힘들다',
                              '어렵다', '깊이', '용이', '초보자', '피드백', '수업', '빠르다', '속도', '시간', '내용', '만들기', '답변', '정보', '진행',
                              '기법', '너무짧다', '강의', '반복되다', '예시', '처음', '앞']

        neg_material_accord = ['촌스럽다', '얇다', '상품', '안오다', '구슬', '준비물', '분량',
                               '패키지', '안오다', '제품', '구성', '주문', '재료', '프린터']

        neg_weight_word = ['다만', '그런데', '충분하다않다', '조금 더', '근데', '쓸데없다', '어렵다', '안타깝다', '좋다것같다',
                           '아쉽다', '더필요하다', '조금불편하다']

        neg_word_list_zip = [neg_front_search, neg_back_search, neg_binary_search,
                             neg_video_accord, neg_content_accord, neg_material_accord]

        for neg_word_list in neg_word_list_zip:
            for neg_word in neg_word_list:
                if neg_word in review_data:
                    if neg_word in neg_weight_word:
                        negative_n += 5
                    else:
                        negative_n += 1

        return negative_n

    def pos_counter(review_data):
        positive_n = 0
        global search_word_list, pos_content_accord, pos_product_accord
        search_word_list = ['빠르다', '감사', '알차다', '만족도', '성취감', '따르다', '구체적으로', '쉬다', '아주',
                            '자세하다', '알게', '좋다', '배우다', '꼼꼼하다', '쉽다', '피드백을', '가르치다', '따르다',
                            '뿌듯', '좋다']

        # 긍정 댓글에서 분류하기 위한 2가지 카테고리 => 영상 설명, 결과물 만족 2가지 카테고리

        pos_content_accord = ['댓글', '답변', '친절', '정보', '팁', '성취', '설명', '피드백', '꼼꼼', '차분', '자세히', '차근차근',
                              '디테일', '기법', '상세', '강의', '이해', '자세', '쉽다', '다양', '실용', '알차다', '구체',
                              '노하우', '알차다']

        pos_product_accord = ['결과물', '디자인', '스타일', '퀄리티', '작품']

        pos_weight_word = ['최고', '너무 좋다', '뿌듯', '꼼꼼']

        pos_word_list_zip = [search_word_list, pos_content_accord, pos_product_accord]
        for pos_word_list in pos_word_list_zip:
            for pos_word in pos_word_list:
                if pos_word in review_data:
                    if pos_word in pos_weight_word:
                        positive_n += 4
                    else:
                        positive_n += 1

        return positive_n

    def return_sentiment(review_data):
        import numpy as np

        pos_score = sentiment_preprocessing.pos_counter(review_data)
        neg_score = sentiment_preprocessing.neg_counter(review_data)
        try:
            sentiment_percent = np.round((pos_score / (neg_score + pos_score)) * 100, 2)
        except:
            return 'not enough data'

        if sentiment_percent > 40:
            return 'good'
        else:
            return 'sorry'

    def apply_sentiment(df):
        df.drop(df.loc[df.review.isna()].index, axis=0, inplace=True)
        df.reset_index(inplace=True)
        df.drop('index', axis=1, inplace=True)

        df['sentiment'] = df.review.map(sentiment_preprocessing.return_sentiment)

        return df

    def return_goodreview_category(review_data):
        from konlpy.tag import Okt
        okt = Okt()
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
        for ca in pos_content_accord:
            if ca in review_data:
                # 강의 내용 칭찬
                result = ca

        for pa in pos_product_accord:
            if pa in review_data:
                # 재료, 완성 결과물 관련 칭찬
                result = pa

        if result in pos_content_accord:
            return 'pos_content'

        if result in pos_product_accord:
            return 'pos_product'

        return 'pos_etc_prefer'

    def return_sorryreview_category(review_data):
        from konlpy.tag import Okt
        okt = Okt()
        result = ''

        for fs in neg_front_search:
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

        for back_s in neg_back_search:
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

        for bs in neg_binary_search:
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
        for va in neg_video_accord:
            if va in review_data:
                # 비디오 문제
                result = va

        for ca in neg_content_accord:
            if ca in review_data:
                # 강의 내용 문제
                result = ca

        for ma in neg_material_accord:
            if ma in review_data:
                # 비디오 문제
                result = ma

        if result in neg_video_accord:
            return 'neg_video'

        if result in neg_content_accord:
            return 'neg_content'

        if result in neg_material_accord:
            return 'neg_material'

    def return_review_cat(df):
        from tqdm import tqdm
        tqdm.pandas()
        df['sentiment_cat'] = df.progress_apply(
            lambda x: sentiment_preprocessing.return_goodreview_category(x['review']) \
                if x['sentiment'] == 'good' \
                else (sentiment_preprocessing.return_sorryreview_category(x['review']) if x['sentiment'] == 'sorry' else 'nan'),
            axis=1)
        return df
