
def split_paper(text):
  """
  Takes raw text file and splits into a list of strings 
  at each occurence of three or more carriage returns
  """

  chunk =[]
  spl = "\n\n\n"
  new = text.split(spl)
  for i in new:
    chunk.append(i)

  for item in chunk:
  	print item[1:10]

  return chunk