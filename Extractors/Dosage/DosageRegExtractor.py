import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DosageElement import DosageElement

class DosageRegExtractor(object):
    
    def __init__(self,rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findEntity(self):

	 dosage_amount ={'dos_amt': '', 'a_offset':[]}
	 dosage_unit={'dos_unit': '', 'u_offset':[]}
	 dosage_freq={'dos_freq': '', 'f_offset':[]}

	 freq = '(week|day|month)'
	 Freq = '(once|twice|everyday|weekly|every other day|one|two|three|four|five)'
	 dose = '(mg|miligram|miligrams|mgs|kg|ug|ml|ul|mililitre|mls|milititres|tabs|tablets|tablet)'
	 freq_code= '(1X|BID|BIW|HS|PRN|Q12H|Q2H|Q3H|Q3W|Q4H|Q5H|Q6H|Q8H|QD|QH|QID|QM|QOD|QOW|TID|TIW|UNK|QHS)'
	 
	 regex = re.compile(r'((\d{1,3}(\.[0-9]{1})?).?'+dose+ '.?'
                   '(.?([0-9].every.[0-9].'+freq+ ')|(.?[0-9].times.a.' +freq+ ')|(.?([0-9].?-.?[0-9].?times.?(per|a).?'+freq+'))|(.?'+Freq+'.?(a|per).?'+freq+')|(.?'+freq_code+'))?)'
                   '',re.IGNORECASE)

	 it = re.finditer(regex, self.Text)
	 dosage_all = []
	 for match in it:
    		 record = match.groups()
    
   	 	 dosage_amount['dos_amt'] = record[1]
  		 dosage_amount['a_offset']=match.span(2)
   		 dosage_unit['dos_unit']= record[3]
   		 dosage_unit['u_offset']=match.span(4)
   		 dosage_freq['dos_freq']= record[4]
   		 dosage_freq['f_offset']=match.span(5)
	 	 print(dosage_amount, dosage_freq, dosage_unit)
		 if dosage_amount:
	 		 return [DosageElement(dosage_amount['dos_amt'], dosage_amount['a_offset'], "DosageRegExtractor" , "DOSE_AMT"), DosageElement(dosage_freq['dos_freq'], dosage_freq['f_offset'], "DosageRegExtractor" , "DOSE_FREQ"), DosageElement(dosage_unit['dos_unit'], dosage_unit['u_offset'], "DosageRegExtractor" , "DOSE_UNIT")]
        # return True
