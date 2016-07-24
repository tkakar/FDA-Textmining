import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DrugnameElement import DrugnameElement


class DrugnameRegExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Tokens = preprocess.wordTokenizeText()
        
    def findDrugnames(self):
	
	with open("/work/tkakar/git-repos/FDA-Textmining/Drugslist.txt") as myfile:
    		drugnames= myfile.read().splitlines()
		#print( drugnames) 
	#break;

	for tokens in self.Tokens:
		for token in tokens:
			if token in drugnames:
				print token
				break
	#return DrugnameElement("".join(output), 0, "DrugnameMetamapExtractor")
	return True
