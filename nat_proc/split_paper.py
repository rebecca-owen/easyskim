def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False

    return True

def split_paper(text):

	from nltk.tokenize import sent_tokenize,word_tokenize


	"""
	Takes raw text file and splits into a list of strings 
	at each occurence of three or more carriage returns

	Needs heading-less fallback!!!
	"""
	introText =[]
	methText =[]
	discText = []
	chunk =[]
	paras = []
	sects = []
	spl = "\n\n"
	new = text.split(spl)

	for i in new:
		chunk.append(i)

	""" Strip out identical chunks which may 
	be remnant footer or header and fig captions"""

	for i in chunk:
		wordList = word_tokenize(i.lower())
		if wordList:
			if i not in paras and wordList[0] != 'fig':
				paras.append(i)



	""" Limit first sentence word length to define new section,
	look for sections beginning with an integer
	"""
	lim = 10
	cont = []

	for i in paras:
		sents = sent_tokenize(i)
		if sents:
			word_tk = word_tokenize(sents[0])
			if len(word_tk)>lim or not word_tk[0].istitle() and not is_number(sents[0]):
				cont.append(i)
			elif len(word_tk)<=lim:
				sects.append(' '.join(cont))
				cont = [i]

	# for i in sects:
	# 	print i + "\n\n"

	# print len(sects)


	""" 
	Split based on header terms by word tokens 
	in first 10 words only
	"""

	for text in sects:
		wordList = word_tokenize(text.lower())

		for i in wordList[0:10]:
			if i == 'introduction':
				introText.append(text)
			elif i=='method' or i=='methods':
				methText.append(text)
			elif i=='discussion' or i=='conclusions':
				discText.append(text)



	if introText:
		introOut = introText[0].encode('ascii', errors='backslashreplace')
	else:
		introOut = []
	if methText:
		methOut = methText[0].encode('ascii', errors='backslashreplace')
	else:
		methOut = []
	if discText:
		discOut = discText[0].encode('ascii', errors='backslashreplace')
	else:
		discOut = []

	return  introOut, methOut, discOut

