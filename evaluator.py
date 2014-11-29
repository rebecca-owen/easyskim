def evaluator():
    pass
def getBibliography(pdfText):
    possibilities = "(BIBLIOGRAPHY)|(Bibliography)|(References)|(REFERENCES)"
    from re import sub
    #bibliography = re.sub("".join([".*",possibilities]),"",pdfText))
    return sub("".join([".*",possibilities]),"",pdfText))
def authorCounter(pdfText):
    pass
def paperCounter(pdfText):
    pass