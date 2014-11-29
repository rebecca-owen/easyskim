from extract import extract
from evaluator import evaluator, authorCounter, paperCounter
def textChanger(pdfText, mostAuthor="", mostPaper="",extractOptions):
	""""Takes the semi-cleaned text of a pdf and extracts the desired portions. Output in markdown suitable for display on the website."""
	if mostAuthor:
        mostAuthor = evaluator(authorCounter(pdfText))
    if mostPaper:
        mostPaper = evaluator(paperCounter(pdfText))
    ex = extract(pdfText)
    #return ''.join([mostAuthor,mostPaper,ex])
    return pdfText