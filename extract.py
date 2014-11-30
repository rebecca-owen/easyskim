introMarkers = ["Introduction:","Beginning","Literature Review","1."]
endMarkers = ["Results","Conclusion"]
bibMarkers = ["References", "Bibliography","Citations"]

def extract(cleanText,options):
    """Basic wrapper functions for the specific options.
options[0] specifies which analysis will be run.
options[1] is for alchemy, and specifies how many keywords will be returned.
options[2] is for sectionExtract, and specifies...
options[3] is for nltk, and specifies..."""
    newstring=""
    if "nltk" in options[0]:
        newstring="".join([newstring,nlpExtract(cleanText,options)])
    if "alchemy" in options[0]:
        newstring="".join([newstring,alchemyExtract(cleanText,options)])
    if "nltk" not in options[0] and "sections" not in options[0] and "alchemy" not in options[0]:
        print(options)
        raise Exception("""No valid options selected. Please enter some 
            combination of 'nltk','sections',and 'alchemy""")
    return newstring

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


    """
    Instead of looping through output, fill empty sections with EMPTY and test for this
    when constructing newstring
    """
    final = []
    for te in t:
        if te:
            final.append(f.summarize(te,options[3])) 
        elif not te:
            final.append("EMPTY")

    newstring = ""

    if  "EMPTY" not in final[0]:
        newstring= "".join([newstring,"\n\n","Introduction\n\n","\n".join(final[0])])
    if  "EMPTY" not in final[1]:
        newstring = "".join([newstring,"\n\n","Methods\n\n","\n".join(final[1])])
    if  "EMPTY" not in final[2]:
        newstring = "".join([newstring,"\n\n","Results\n\n","\n".join(final[2])])
    if  "EMPTY" not in final[3]:
        newstring = "".join([newstring,"\n\n","Conclusions\n\n","\n".join(final[3])])

    return newstring

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
    return "".join(["Keywords: ",finalKeywords]) #figure out formatting for this later.

if __name__ == '__main__':
    import codecs
    cleanText=codecs.open("test.pdf.txt",encoding="utf-8").read()
    ex = extract(cleanText,['alchemy',5])
    print(ex)
    ex = extract(cleanText,['nltk','','',3])
    print(ex)