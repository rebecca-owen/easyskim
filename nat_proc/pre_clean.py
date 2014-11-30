def pre_clean(text):

	text = re.sub(r'\[.*?\]\s*', '', text)
	text = re.sub(r'\(.*?\)\s*', '', text)
	text = re.sub('- ', '', text)
	text = re.sub(', ,', ',', text)

	sents = sent_tokenize(text)
	out = []

	for s in sents:
		if s.find('E-mail') == -1 and s.find('http') == -1 and s.find("Current\ address") == -1 and s.find("Corresponding\ author") == -1 and s.find("Published\ by") == -1:
			out.append(s)

	return ' '.join(out).encode('ascii', errors='backslashreplace')

		

print pre_clean(text_split)