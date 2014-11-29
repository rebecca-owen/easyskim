from extract import extract
from evaluator import evaluator, authorCounter, paperCounter
def textChanger(pdfText, mostAuthor="", mostPaper="",extractOptions="nltkalchemy",devMode=false):
	""""Takes the semi-cleaned text of a pdf and extracts the desired portions. Output in markdown suitable for display on the website."""
	if mostAuthor:
        mostAuthor = evaluator(authorCounter(pdfText))
    if mostPaper:
        mostPaper = evaluator(paperCounter(pdfText))
    ex = extract(pdfText)
    #return ''.join([mostAuthor,mostPaper,ex])
    return pdfText
if __name__=="__main__":
	import codecs
	cleanText=codecs.open("sample.txt",encoding="utf-8").read()
	textChanger()