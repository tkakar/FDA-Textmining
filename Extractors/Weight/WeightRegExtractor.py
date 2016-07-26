import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.WeightElement import WeightElement
from DataElements.WeightCodeElement import WeightCodeElement

class WeightRegExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findEntity(self):
        extract_weight = re.search(r'.*\s([0-9]+(\.[0-9]+)?).?(pounds|pound|lb|lbs).*',self.Text,re.IGNORECASE)

<<<<<<< HEAD
		if not extract_weight:
			extract_weight = re.search(r'.*\s([0-9]+(\.[0-9]+)?).?(kg|kgs|kilograms|kilogram).*',self.Text,re.IGNORECASE)
			if not extract_weight:
	    			weight="UNK"
			else:
	    			weight = extract_weight.group(1)
				weightCode = "KG"
		else:
			weight = extract_weight.group(1)
			weightCode = "LBS"	 
=======
        if not extract_weight:
            extract_weight = re.search(r'.*\s([0-9]+(\.[0-9]+)?).?(kg|kgs|kilograms|kilogram).*',self.Text,re.IGNORECASE)
            if not extract_weight:
                weight="UNK"
            else:
                weight = extract_weight.group(1)
                weightCode = "KG"
        else:
            weight = extract_weight.group(1)
            weightCode = "LBS"	 
>>>>>>> 4ec137cd319088066f5c750b21dc7afd4a6adae9
		
        if extract_weight:
            weight_offset = [extract_weight.start(1), extract_weight.end(1)]
            weightCode_offset = [extract_weight.start(3), extract_weight.end(3)]
            #weight_offset = "[{s},{e}]".format(s=extract_weight.start(1), e=extract_weight.end(1))
            #weightCode_offset = "[{s},{e}]".format(s=extract_weight.start(3), e=extract_weight.end(3))

            print ("regEx_weight:",weight,weight_offset)
            print ("regEx_weight_cod:",weightCode,weightCode_offset)
                    
            return [WeightElement(weight, [weight_offset], "WeightRegExtrator", "WT"), WeightCodeElement(weightCode, [weightCode_offset], "WeightRegExtrator", "WT_COD")]

	#return True
