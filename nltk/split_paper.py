def split_paper(text):
  """
  Takes raw text file and splits into a list of strings 
  at each occurence of three or more carriage returns
  """
  introText =[]
  methText =[]
  discText = []
  chunk =[]
  spl = "\n\n\n"
  new = text.split(spl)
  for i in new:
    chunk.append(i)

  for text in chunk:
    wordList = word_tokenize(text.lower())
    for i in wordList[0:10]:
      if i == 'introduction':
        introText.append(text)
      if i=='method' or i=='methods':
        methText.append(text)
      if i=='discussion' or i=='conclusions':
        discText.append(text)

  return introText, methText, discText