import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.AgeElement import AgeElement
from DataElements.AgeCodeElement import AgeCodeElement

class AgeRegExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findEntity(self):
        extract_age = re.search(r'.*\s([0-9]+).?(yr|yrs|years|year|yo).*',self.Text,re.IGNORECASE)
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
        	return [AgeElement(age, extract_age.span(1), "AgeRegExtrator", "AGE"), AgeCodeElement(ageCode, extract_age.span(2), "AgeRegExtrator", "AGE_COD")]
        #return True
