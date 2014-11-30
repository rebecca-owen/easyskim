from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import re
import codecs

"""
Modified from http://glowingpython.blogspot.co.uk/2014/09/text-summarization-with-nltk.html
"""


class FrequencySummarizer:
	def __init__(self, low_thresh=0.1, high_thresh=0.9):
		"""
		 Initialize the text summarizer.
		 Words that have a frequency term lower than low_thresh 
		 or higer than high_thresh will be ignored.
		"""
		ignore = ['fig','figure','ibid', 'et al','cf','NB','N.B.']
		
		self._low_thresh = low_thresh
		self._high_thresh = high_thresh 
		self._stopwords = set(stopwords.words('english') + list(punctuation) + list(ignore))


	def _compute_frequencies(self, word_tk):

		freq = defaultdict(int)
		for s in word_tk:
			for word in s:
				if word not in self._stopwords:
					freq[word] += 1
		# frequencies normalization and fitering
		m = float(max(freq.values()))
		for w in freq.keys():
			freq[w] = freq[w]/m
			if freq[w] >= self._high_thresh or freq[w] <= self._low_thresh:
				del freq[w]
		return freq

	def summarize(self, text, n):
		"""
			Return a list of n sentences 
			which represent the summary of text.
		"""
		text = unicode(text)
		sents = sent_tokenize(text)
		if n > len(sents):
			n = len(sents)
		word_tk = [word_tokenize(s.lower()) for s in sents]
		self._freq = self._compute_frequencies(word_tk)
		ranking = defaultdict(int)
		for i,sent in enumerate(word_tk):
			for w in sent:
				if w in self._freq and len(w)>4:  #Only count words of length>4 as significant
					ranking[i] += self._freq[w]
		sentsindx = self._rank(ranking, n)    
		return [sents[j].encode('ascii', errors='backslashreplace')  for j in sentsindx]

	def _rank(self, ranking, n):
		""" return the first n sentences with highest ranking """
		return nlargest(n, ranking, key=ranking.get)




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
	resText = []
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
			elif i=='results':
				resText.append(text)
			elif i=='discussion' or i=='conclusions':
				discText.append(text)

	if introText:
		introOut = introText[0].encode('ascii', errors='backslashreplace')
	else:
		introOut = sects[0:8]
	if methText:
		methOut = methText[0].encode('ascii', errors='backslashreplace')
	else:
		methOut = []
	if resText:
		resOut = resText[0].encode('ascii', errors='backslashreplace')
	else:
		resOut = []
	if discText:
		discOut = discText[0].encode('ascii', errors='backslashreplace')
	else:
		discOut = sects[-8:]

	return  introOut, methOut, resOut, discOut

def pre_clean(text):

	text = re.sub(r'\[.*?\]\s*', '', text)
	text = re.sub(r'\(.*?\)\s*', '', text)
	text = re.sub('- ', '', text)
	text = re.sub(', ,', ',', text)

	sents = sent_tokenize(text)
	out = []

	for s in sents:
		if s.find('www') == -1 and s.find('E-mail') == -1 and s.find('Email') == -1 \
		and s.find('Corresponding\ author') == -1 and s.find('Current\ address') == -1 \
		and s.find('Article\ history') == -1 and s.find('Tel.') == -1:
			out.append(s)
 
	return ' '.join(out)


""""""""""""""""""









""""""""""""""""""""




"""Apply to file"""
import codecs


# # print type(raw)
# # raw = re.sub(r'\(.*?\)\s*', '', raw)
# # raw = re.sub(r'\[.*?\]\s*', '', raw)
# # raw = re.sub('- ', '', raw)
# # raw = re.sub(', ,', ',', raw)


# fs = FrequencySummarizer()
# out = fs.summarize(raw, 3)
# for l in out:
#   print l + "\n"


text_split = codecs.open('text.txt', encoding='utf-8').read()

inp = pre_clean(text_split)
out = split_paper(inp)
fs = FrequencySummarizer()

for t in out:
	if t:
		data = fs.summarize(t,3)
		print data






		
