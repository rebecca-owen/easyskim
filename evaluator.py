import re
"""At the moment, most of this file is not yet implemented. When it is complete,
it will be able to take input from multiple pdfs as text and evaluate the most
frequently cited authors and papers. """
def evaluator():
    """Currently does nothing. Eventually, will take in a long list of authors
    of papers, and orders by popularity. Takes in a list, and returns an
    ordered set."""
    pass
def getBibliography(pdfText):
    """Most bibliographies are marked by one of these significant words. Delete
    everything before the bibliography. Everything else in this file operates 
    on the bibliography."""
    possibilities = "(BIBLIOGRAPHY)|(Bibliography)|(References)|(REFERENCES)"
    return re.sub("".join([".*",possibilities]),"",pdfText)
def authorCounter(bibliography):
    """Returns a list of strings corresponding to the authors. """
    #Authors are assumed to be defined by a newline, followed by a capital
    #letter, followed by some combination of letters, a comma, and some number
    #of letters where the first is capitalized. This gets some false positives,
    #and some false negatives, so it could be improved, but for now this is the
    #regex we have, not the regex we want.
    return re.findall("\\n *[A-Z][\w]*, [A-Z][\w]*", bibliography)
def paperCounter(bibliography):
    """When finished, will deliver a list of all papers used. The list will be
    composed of strings, one for each file. There will not be duplicates if
    everything works properly, as a consequence of how bibliographies are
    structured."""
    pass
if __name__=="__main__":
    #Confirms that the basic functionality isn't tossing errors.
    x = authorCounter(getBibliography(open("sample.txt").read()))