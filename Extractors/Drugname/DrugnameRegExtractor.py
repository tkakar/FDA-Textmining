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
	Drug_list=[]
	for tokens in self.Tokens:
		for token in tokens:
			if token in drugnames:
				print "DrugnameRegEx: " + token
				Drug_list.append(token)
				break
	if Drug_list:
		return DrugnameElement("".join(Drug_list), 0, "DrugnameMetamapExtractor", "DRUGNAME")
	#return True
