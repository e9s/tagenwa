from porter import PorterStemmer

def stem(word):
	"""Stem the word using the Porter stemmer
	
	:param text: word
	:type text: unicode
	:return: Porter stemmer's stem
	:rtype: unicode
	"""
	low = word.lower()
	p = PorterStemmer()
	return p.stem(low, 0,len(low)-1)
