# -*- coding: UTF-8 -*-


class MultilingualTokenizer(object):
	
	def __init__(self, tokenizers, default_tokenizer):
		self.tokenizers = tokenizers
		self.default_tokenizer = default_tokenizer
	
	def tokenize_tagged(self, tagged_texts, **kwargs):
		for text, tag in tagged_texts:
			word_tokenizer, sentence_tokenizer = self.tokenizers.get(tag, self.default_tokenizer)
			tokens = []
			for sentence in sentence_tokenizer.tokenize(text):
				tokens.append(word_tokenizer.tokenize(sentence, **kwargs))
			yield (tokens, tag)
