import re

def extract(cleanText,options):
    """Basic wrapper functions for the specific options.
options[0] specifies which analysis will be run.
options[1] is for alchemy, and specifies how many keywords will be returned.
options[2] is for sectionExtract, and specifies...
options[3] is for nltk, and specifies..."""
    temp = []
    if "nltk" in options[0]:
        temp.append(nlpExtract(cleanText,options))
    if "alchemy" in options[0]:
        temp.append(alchemyExtract(cleanText,options))
    if "nltk" not in options[0] and "alchemy" not in options[0]:
        print(options)
        raise Exception("""No valid options selected. Please enter some 
            combination of 'nltk', and 'alchemy""")
    return "".join(temp)

def nlpExtract(cleanText,options):
    """Calls the split_paper and FrequencySummarizer programs. 
    options[3] will be interpreted as the number of sentences to print out."""
    from nat_proc import FrequencySummarizer, split_paper
    try:
        options[3]=int(options[3])
    except IndexError as e:
        options[3]=5
    except ValueError as e:
        print("You selected nltk, and options[3] was not a valid integer.")
        raise e
    t = split_paper.split_paper(cleanText)
    f = FrequencySummarizer.FrequencySummarizer()

    #Instead of looping through output, fill empty sections with EMPTY and 
    #test for this when constructing newstring
    sections = ['Introduction', 'Methods', 'Results', 'Conclusions']
    final = []
    for i, te in enumerate(t):
        if te:
            temp = [x.replace('\n', ' ') for x in f.summarize(te,options[3])]
            temp = removeUnwantedSpaces(" ".join(temp))
            final.append('<h4>%s</h4><p>%s</p>' % (sections[i], temp)) 
            
    return "".join(final)

def alchemyExtract(cleanText,options):
    """Uses alchemyAPI to find keywords in the cleaned text. 
    In this case,options[1] should specify the number of keywords to be 
    used. Default to 4."""
    try:
        options[1]=int(options[1])
    except IndexError as e:
        options[1]=4
    except ValueError as e:
        print("You selected alchemy, and options[1] was not a valid integer.")
        raise e
    from alchemyapi import AlchemyAPI
    alch = AlchemyAPI()
    response = alch.keywords('text',cleanText,{'sentiment':1})
    rKeywords = response['keywords']
    finalKeywords = []
    if options[1]<len(rKeywords):
        for i in range(options[1]):
            finalKeywords.append(rKeywords[i]['text'])
    else:
        finalKeywords = rKeywords
    return "\n\nKeywords: " + ", ".join(finalKeywords) #figure out formatting for this later.

def removeUnwantedSpaces(text):
    """A simple function that strips text of spaces and leftover symbols that
    shouldn't be there with regular expressions."""
    text = re.sub(' \.', '.', text)
    text = re.sub(' \,', ',', text)
    text = re.sub(' \;', ';', text)
    return text

if __name__ == '__main__':
    import codecs
    cleanText=codecs.open("test.pdf.txt",encoding="utf-8").read()
    ex = extract(cleanText,['alchemy',5])
    print(ex.replace('\n', ' '))
    ex = extract(cleanText,['nltk','','',3])
    print(ex.replace('\n', ' '))