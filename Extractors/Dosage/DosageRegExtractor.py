import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DosageElement import DosageElement

class DosageRegExtractor(object):
    
    def __init__(self,rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findDosages(self):

	 dosage ={'dos_unit':'','dos_amt': '', 'dos_freq':''}

	 freq = '(week|day|month)'
	 Freq = '(once|twice|everyday|weekly|every other day|one|two|three|four|five)'
	 dose = '(po|mg|miligram|miligrams|mgs|kg|ug|ml|ul|mililitre|mls|milititres|tabs|tablets|tablet)'
	 freq_code= '(1X|BID|BIW|HS|PRN|Q12H|Q2H|Q3H|Q3W|Q4H|Q5H|Q6H|Q8H|QD|QH|QID|QM|QOD|QOW|TID|TIW|UNK|QHS)'
	
	 regex = re.compile(r'((\d{1,3}(\.[0-9]{1})?).?'+dose+ '.?'
                   '(.?([0-9].every.[0-9].'+freq+ ')|(.?[0-9].times.a.' +freq+ ')|(.?([0-9].?-.?[0-9].?times.?(per|a).?'+freq+'))|(.?'+Freq+'.?(a|per).?'+freq+')|(.?'+freq_code+'))?)'
                   '',re.IGNORECASE)

	 it = re.finditer(regex, self.Text)
	 dosage_all = []
	 for match in it:
    		record = match.groups()
    		# print (record)
    		dosage['dos_amt'] = record[1]
    		dosage['dos_unit']= record[3]
    		dosage['dos_freq']= record[4]
    		dosage_all.append(dosage.copy())

	 print(dosage_all)
	 # return DosageElement(" ".join(dosage_all), 0, "DosageRegExtractor")
         return True
