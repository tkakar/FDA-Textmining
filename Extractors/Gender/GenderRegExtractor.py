import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.GenderElement import GenderElement

class GenderRegExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findEntity(self):
		extract_gender_m = []
		extract_gender_f = []
		extract_gender_m = re.search(r'.(\bmale\b)',self.Text,re.IGNORECASE)
		extract_gender_f = re.search(r'.(\bfemale\b)',self.Text,re.IGNORECASE)
		if not extract_gender_f:
			if not extract_gender_m:
				gender = "UNK"
	    		else:
	        		gender = extract_gender_m.group()
				gender_offset = "[{s},{e}]".format(s=extract_gender_m.start(), e=extract_gender_m.end())
		else:
			gender = extract_gender_f.group()
			gender_offset = "[{s},{e}]".format(s=extract_gender_f.start(), e=extract_gender_f.end())
	
		if extract_gender_m or extract_gender_f:
			print("regEx_gender:"+gender+gender_offset)
			return [GenderElement(gender, gender_offset, "GenderRegExtrator", "SEX")]
