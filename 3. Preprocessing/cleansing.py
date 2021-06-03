class cleansing_data:
	"""
	입력받은 비정형 데이터를 분석하기 쉬운 형태로 정제해주는 사용자 함수 모음
	"""

	def cleanName(name):
		"""
		c 사이트 강의명에 붙어 있는, 제목과 상관없는 정보를 지워 주는 사용자 함수 
		"""
		import re
 		name = re.sub('\[{1}.+\] ','',name)
  		name = name.strip()
  		return name

	
	def stemming(review):
		"""
		우리가 일상에서 쓰는 말투를, 원형 형태소로 바꿔 주는 사용자 함수
		해당 함수를 이용한 결과값은 어떤 텍스트가 들어 있는지 조사하기 용이하다.
		"""
		import re
  		malist5 = okt.pos(review, norm=False, stem=True)

  		comment = ''
  		last = ''
  		for pos in malist5:
    			if pos[1] in ['Verb','Punctuation','Adverb']:
      				comment = comment + pos[0] + ' '
    			elif last == pos[1]:
      				comment = comment + ' ' + pos[0]
    			elif pos[1] == 'Josa':
      				comment = comment + pos[0] + ' '
    			else:
      				comment = comment + pos[0]
    			last = pos[1]
  		return comment

	def cleansingEmoticon(review):
		"""
		한글, 영어, 숫자, 기본공백을 제외한 특수문자를 제거하는 사용자 함수
		"""
		import re
  		review = re.sub('[^\w ]','',review)
  		return review

	def countValue(list_):
		"""
		list를 parameter로 받은 후, list 안에 있는 value를 count해서
		{value : countnumber} 형태로 return
		"""
  		countDict = {}
  		values = set(list_)
  		values = list(values)
  		for value in values:
    			num = list_.count(value)
    			countDict[value] = num
    
  		return countDict
