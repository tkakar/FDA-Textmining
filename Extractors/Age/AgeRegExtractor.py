import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.AgeElement import AgeElement

class AgeRegExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findAge(self):
	extract_age = re.findall(r'.*\s([0-9]+).?(yr|yrs|years|year|yo).*',self.Text,re.IGNORECASE)
	if not extract_age:
		extract_age = re.findall(r'.*\s([0-9]+).?(months|months-old|months old|month-old|month old).*',self.Text,re.IGNORECASE)
		if not extract_age:
			age="unknown"
        	else:
            		age = extract_age[0][0]+" months"
    	else:
		age = extract_age[0][0]+" years"

	print ("regEx_age:"+age)

	return AgeElement(" ".join(age), 0, "AgeRegExtrator")
	#return True