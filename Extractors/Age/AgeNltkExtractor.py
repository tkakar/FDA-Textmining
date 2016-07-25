import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from Preprocessing.Preprocessor import Preprocessor
from DataElements.AgeElement import AgeElement

class AgeNltkExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = self.preprocess.rawText()
        
    def findEntity(self):
    	sentences = sent_tokenize(self.Text)
    	filtered_sentences = []
    	for s in sentences:
                s=re.sub('-', ' ', s)   ## Replace "-" with " " in the sentences, especially useful for extracting age
                filtered_sentences.append(s)

    	## Word Tokenization
    	tokenized = [word_tokenize(s) for s in filtered_sentences]

    	final_tags = []

    	for i in tokenized:
            #words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(i)

            ##Assumption: Various input formats considered for age:71 year old, 39 years old, 50-year-old, 7 years, 1 year, 3-years
            chunkGram = r"""numberChunks: {<CD><NN.?><JJ>?<CD>?}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            #print("chunked:")
            #print(chunked)

            for n in chunked:
                print n
                if isinstance(n, nltk.tree.Tree):
                    if n.label() == 'numberChunks':
                        print "we need to know n[0][0]: ", n[0][0]
                        print "we need to know n[1][0]: ", n[1][0]
                        #print "we need to know n[2][0]: ", n[2][0]
                        if len(n) == 3:
                            if n[2][1] == 'CD':
                                #Vimig needs to ask Susmitha what is the point of this line, I don't ever see [2][1] having been CD.
                                # Because n[2][0] is always "old" if anything at all. 
                                print "TESTREACHED!!!!!!!!!!!!!!!!!!!"
                                tagList = [n[0][0], n[1][0], n[2][0]]
                            else:
                                tagList = [n[0][0], n[1][0]]
                        else:
                            tagList = [n[0][0], n[1][0]]
                        
                        final_tags.append(tagList)
                            #else:
                            #print(2)
                            
                    #print(final_tags)

        age = 'unknown'
        age_keyword_list = ["yrs", "years", "year", "yo"]

        print "this are the final tags::::::    ", final_tags
    	for tags in final_tags:
            print "These are cleartags of some kind: ??? ", tags
            if any(word in tags for word in age_keyword_list):
                age = tags
                #Added the below so it would take the first instance, not the last like it was doing. 
                break


        #Now to find the location of the words we got!
        self.preprocess.parseXML()
        root = self.preprocess.root 

        for elem in root.iterfind(tag='Token'):
            
        print 'this was found in the xml: ', root.find(".//[tag='"+age[0]+"'")

    	#if not year:
        	#	dates = "Unknown"
    	#else:
        	#	dates = ', '.join(year)
    	#print(dates)

    	print("nltk_age:",age)

        #[AgeElement(age, extract_age.span(1), "AgeRegExtrator", "AGE"), AgeCodeElement(ageCode, extract_age.span(2), "AgeRegExtrator", "AGE_COD")]
    	return AgeElement(" ".join(age), 0, "AgeNltkExtrator")
    	#return True
