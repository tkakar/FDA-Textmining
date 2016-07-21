import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.GenderElement import GenderElement

class GenderRegExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findGender(self):
	extract_gender_m = []
	extract_gender_f = []
	extract_gender_m = re.findall(r'.(\bmale\b)',self.Text,re.IGNORECASE)
	extract_gender_f = re.findall(r'.(\bfemale\b)',self.Text,re.IGNORECASE)
	if not extract_gender_f:
		if not extract_gender_m:
			gender = "unknown"
    		else:
        		gender = extract_gender_m[0]
	else:
		gender = extract_gender_f[0]
	

	print("regEx_gender:" + gender)

	return GenderElement(" ".join(gender), 0, "GenderRegExtrator")

	#return True
