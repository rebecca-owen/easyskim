from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import re

"""
Modified from http://glowingpython.blogspot.co.uk/2014/09/text-summarization-with-nltk.html
"""


class FrequencySummarizer:
  def __init__(self, low_thresh=0.1, high_thresh=0.9):
    """
     Initialize the text summarizer.
     Words that have a frequency term lower than low_thresh 
     or higer than high_thresh will be ignored.
    """
    ignore = ['fig','figure','ibid', 'et al','cf','NB','N.B.']
    
    self._low_thresh = low_thresh
    self._high_thresh = high_thresh 
    self._stopwords = set(stopwords.words('english') + list(punctuation) + list(ignore))


  def _compute_frequencies(self, word_tk):

    freq = defaultdict(int)
    for s in word_tk:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in freq.keys():
      freq[w] = freq[w]/m
      if freq[w] >= self._high_thresh or freq[w] <= self._low_thresh:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """
      Return a list of n sentences 
      which represent the summary of text.
    """
    text = "".join([unicode(x) for x in text])
    sents = sent_tokenize(text)
    if n > len(sents):
      n = len(sents)
    word_tk = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_tk)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_tk):
      for w in sent:
        if w in self._freq and len(w)>4:  #Only count words of length>4 as significant
          ranking[i] += self._freq[w]
    sentsindx = self._rank(ranking, n)    
    return [sents[j].encode('ascii', errors='backslashreplace')  for j in sentsindx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)
