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