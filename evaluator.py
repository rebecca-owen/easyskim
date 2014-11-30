import re
def evaluator():
    pass
def getBibliography(pdfText):
    possibilities = "(BIBLIOGRAPHY)|(Bibliography)|(References)|(REFERENCES)"
    #bibliography = re.sub("".join([".*",possibilities]),"",pdfText))
    return re.sub("".join([".*",possibilities]),"",pdfText)
def authorCounter(bibliography):
    return re.findall("\\n *[A-Z][\w]*, [A-Z][\w]*", bibliography)
def paperCounter(bibliography):
    pass
if __name__=="__main__":
    x = authorCounter(getBibliography(open("sample.txt").read()))