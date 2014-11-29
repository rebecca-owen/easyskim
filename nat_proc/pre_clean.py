

def pre_clean(text):
	sents = sent_tokenize(text)

	for s in sents:
		print s