import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.WeightElement import WeightElement

class WeightRegExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findEntity(self):
	#extract_weight = re.findall(r'.*([0-9]{3}(\.[0-9]{1})?).?(pounds|pound|lb|lbs).*',self.Text,re.IGNORECASE)
	# the below rule takes care of the digits issues
	extract_weight = re.findall(r'.*\s([0-9]+(\.[0-9]+)?).?(pounds|pound|lb|lbs).*',self.Text,re.IGNORECASE)
	if not extract_weight:
    		weight="unknown"
	else:
    		weight = extract_weight[0][0]+" pounds"
	

	print ("regEx_weight:" + weight)

	return WeightElement(" ".join(weight), [[]], "WeightRegExtrator", "WT")

	#return True