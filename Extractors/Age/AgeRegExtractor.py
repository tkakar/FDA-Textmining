import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.AgeElement import AgeElement
from DataElements.AgeCodeElement import AgeCodeElement

class AgeRegExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findEntity(self):	

	extract_age = ""
	age = ""
	age_offset = ""
	ageCode = ""
	ageCode_offset = ""

        extract_age = re.search(r'.*\s([0-9]+).?(years-old|year-old|yr|yrs|years|year|yo|y.o.|y.o|y/o).*',self.Text,re.IGNORECASE)
        if not extract_age:
            extract_age = re.search(r'.*\s([0-9]+).?(months|months-old|months old|month-old|month old).*',self.Text,re.IGNORECASE)
            if not extract_age:
                age="UNK"
                ageCode="UNK"
            else:
                age = extract_age.group(1)
                #comes from the FAERS data extraction descriptions
                ageCode = "MON"
        else:
            age = extract_age.group(1)
            ageCode = "YR"
                        
        if extract_age: 
            age_offset = [extract_age.start(1), extract_age.end(1)]
            ageCode_offset = [extract_age.start(2), extract_age.end(2)]
      		#age_offset = "[{s},{e}]".format(s=extract_age.start(1), e=extract_age.end(1))
	      	#ageCode_offset = "[{s},{e}]".format(s=extract_age.start(2), e=extract_age.end(2))

            print ("regEx_age:",age,age_offset)
            print ("regEx_age_cod:",ageCode,ageCode_offset)
            return [AgeElement(age, [age_offset], "AgeRegExtrator", "AGE"), AgeCodeElement(ageCode, [ageCode_offset], "AgeRegExtrator", "AGE_COD")]

        #return True


