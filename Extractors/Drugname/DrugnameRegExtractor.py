import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DrugnameElement import DrugnameElement


class DrugnameRegExtractor(object):
    

    def __init__(self, rawTextFileName, intermediateXMLFileName):
        self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Tokens = self.preprocess.wordTokenizeText()
        
    def findEntity(self):
	
	with open("/work/tkakar/git-repos/FDA-Textmining/Drugslist.txt") as myfile:
    		drugnames= myfile.read().splitlines()

	Drug_list=[]
	for tokens in self.Tokens:
		#print self.Tokens
		for token in tokens:
			token= token.lower()
			# tokens have some unicode u character which needs to be removed
			token = token.encode('utf-8')
			if token in [item.lower() for item in drugnames]:
				 #print "DrugnameRegEx: " + token
				 #start = [match.start() for match in re.finditer(re.escape(token), T)]
				 Drug_list.append(token)
				 #return DrugnameElement("".join(token),[[]], "DrugnameMetamapExtractor", "DRUGNAME")
				 #self.preprocess.parseOffset(token,":")
	if not Drug_list:
		print ("Drugname not found:")
	else:
		
		## somehow the druglist has u' charachter with each token so replacing it
		#Drug_list = [item.replace("u", "") for item in Drug_list]
		#Drug_list = [item.replace("'", "") for item in Drug_list]
		print Drug_list
		return True
