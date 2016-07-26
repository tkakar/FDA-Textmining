import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from Preprocessing.Preprocessor import Preprocessor
from DataElements.WeightElement import WeightElement

class WeightNltkExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findEntity(self):
	sentences = sent_tokenize(self.Text)
	filtered_sentences = []
	for s in sentences:
    		s=re.sub('-', ' ', s)   ## Replace "-" with " " in the sentences, especially useful for extracting age
    		filtered_sentences.append(s)

	## Word Tokenization
	tokenized = [word_tokenize(s) for s in filtered_sentences]

	final_tags = []
	year = []

	for i in tokenized:
    		#words = nltk.word_tokenize(i)
    		tagged = nltk.pos_tag(i)

		chunkGram = r"""numberChunks: {<CD><NN.?><JJ>?<CD>?}"""
		chunkParser = nltk.RegexpParser(chunkGram)
		chunked = chunkParser.parse(tagged)
            	#print("chunked:")
            	#print(chunked)

    		for n in chunked:
			if isinstance(n, nltk.tree.Tree):
				if n.label() == 'numberChunks':
					if len(n) == 3:
						if n[2][1] == 'CD':
							tag = n[0][0]+" "+n[1][0]+" "+n[2][0]
			                     		year.append(tag)
						else:
                        				tag = n[0][0]+" "+n[1][0]
                			else:
                    				tag = n[0][0]+" "+n[1][0]
                			final_tags.append(tag)
                			#else:
                    			#print(2)

			#print(final_tags)

	weight = 'unknown'
	weight_keyword_list = ["pounds", "pound", "lb", "lbs"]


	for tags in final_tags:
    		if any(word in tags for word in weight_keyword_list):
        		weight = tags


	#if not year:
    	#	dates = "Unknown"
	#else:
    	#	dates = ', '.join(year)
	#print(dates)

	print("nltk_weight:"+weight)

	return WeightElement(" ".join(weight), 0, "WeightNltkExtrator", "WT")
	#return True



