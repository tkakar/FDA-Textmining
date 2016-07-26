import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DrugnameElement import DrugnameElement


class DrugnameRegExtractor(object):
    

    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Tokens = preprocess.wordTokenizeText()
        
    def findEntity(self):
	
	with open("/work/tkakar/git-repos/FDA-Textmining/Drugslist.txt") as myfile:
    		drugnames= myfile.read().splitlines()
		#print( drugnames) 
	#break;
	#Drug_list=[]
	for tokens in self.Tokens:
		
		for token in tokens:
			#print token
			#regex = re.compile(r'' +token, re.IGNORECASE)
			#[m.group(0) for l in drugnames for m in [regex.search(l)] if m]
			
			#if token in [x.lower() for x in tokens]:
			#	print "DrugnameRegEx: " + token
			#	#break
			#	#Drug_list.append(token)
				
			#else:
			#	print ("Drugname not found by RegExtractor")
			#	break
				#return DrugnameElement("".join(token),[[]], "DrugnameMetamapExtractor", "DRUGNAME")
			return True
