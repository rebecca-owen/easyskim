introMarkers = ["Introduction:","Beginning","Literature Review","1."]
endMarkers = ["Results","Conclusion"]
bibMarkers = ["References", "Bibliography","Citations"]

def extract(cleanText,options):
    """Basic wrapper functions for the specific options.
options[0] specifies which analysis will be run.
options[1] is for alchemy, and specifies how many keywords will be returned.
options[2] is for sectionExtract, and specifies...
options[3] is for nltk, and specifies..."""
    product = []
    if "nltk" in options[0]:
        product.append(nlpExtract(cleanText,options))
    if "sections" in options[0]:
        product.append(sectionExtract(cleanText,options))
    if "alchemy" in options[0]:
        product.append(alchemyExtract(cleanText,options))
    if "nltk" not in options[0] and "sections" not in options[0] and "alchemy" not in options[0]:
        print(options)
        raise Exception("""No valid options selected. Please enter some 
            combination of 'nltk','sections',and 'alchemy""")
    return product

def nlpExtract(cleanText,options):
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
    return [f.summarize(te,options[3]) for te in t if te]

def alchemyExtract(cleanText,options):
    """In this case,options[1] should specify the number of keywords to be 
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
    return finalKeywords #figure out formatting for this later.

#def sectionExtract(cleanText,options):
    
def regexSeperate(cleanText,options):
    import re

def seperateSections(cleanText,options):
    """Takes in cleanText as a string, returns a list of seperated sections."""
    splits = ["\n\n","        "]
    notFails = []
    for splitter in splits:
        attempt = cleanText.split(splitter)
        attempt = [a for a in attempt if len(a)>6]
        if len(attempt)>2:
            notFails.append(attempt)
    lessFails = []
    failCount = []
    for notFail in notFails:
        fail=0
        for section in notFail:
            if len(section) < 50:
                fail+=1
            if len(section.split("/n"))>len(section)/30:
                fail+=1
        failCount.append(fail)
    vec = zip(failCount,notFails)
    for v in vec:
        for notFail in v[1]:
            print(notFail)
    sortedVec = sorted(vec,lambda k,r: (k))
    best = sortedVec[0]
    return best

if __name__ == '__main__':
    import codecs
    cleanText=codecs.open("sample.txt",encoding="utf-8").read()
    ex = extract(cleanText,['alchemy',5])
    #print(seperateSections(cleanText,""))
    #print(extract(cleanText,['nltk','','',3]))