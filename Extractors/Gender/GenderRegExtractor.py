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
		gender = ""
		gender_offset = ""

		extract_gender_m = re.search(r'.(\bmale\b|\bman\b|he|his|him)',self.Text,re.IGNORECASE)
		extract_gender_f = re.search(r'.(\bfemale\b|\bwoman\b|she|her|hers)',self.Text,re.IGNORECASE)

		if not extract_gender_f:
			if not extract_gender_m:
				gender = "UNK"
	    		else:
	        		gender = extract_gender_m.group()
				#gender_offset = "[{s},{e}]".format(s=extract_gender_m.start(), e=extract_gender_m.end())
				gender_offset = [extract_gender_m.start(), extract_gender_m.end()]
                                #Change to make it from female/male to F,M
                                gender = "M"
		else:
			gender = extract_gender_f.group()
			gender_offset = [extract_gender_f.start(), extract_gender_f.end()]	
                        #Change to make it from female/male to F,M
                        gender = "F"
	
		if extract_gender_m or extract_gender_f:
			print("regEx_gender:",gender,gender_offset)
			return [GenderElement(gender, [gender_offset], "GenderRegExtrator", "SEX")]
