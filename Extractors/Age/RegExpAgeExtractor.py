import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.AgeElement import AgeElement

class RegExpExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findEntity(self):
	extract_age = re.findall(r'.*([0-9]{2}).?(yrs|years|year).*',self.Text,re.IGNORECASE)
	if not extract_age:
    		age="unknown"
	else:
    		age = extract_age[0][0]+" years"
	

	print age

	return AgeElement(" ".join(age), 0, "RegExpAgeExtrator")

	#return True
