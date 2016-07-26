import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DrugnameElement import DrugnameElement
from pymetamap import MetaMap

class DrugnameMetamapExtractor(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()
        
    def findEntity(self):

	# the server installed on your machine
	mm = MetaMap.get_instance('/work/tkakar/public_mm/bin/metamap14')

	sample_Text = '/work/tkakar/FDAfirstNarrative.txt'
	#sents= self.Text
	concepts,error = mm.extract_concepts(filename= sample_Text, word_sense_disambiguation=True)


	for concept in concepts:
		c= concept.semtypes
		c =c.replace("[", "")
		c = c.replace("]","")
		semTypes= c.strip().split(",")
		#print semTypes, type(semTypes)
		for semType in semTypes:

			if semType in ['phsu' , 'orch']:
				token = concept.trigger.strip().split("-")[0]
				token = token.replace("[","")
				offset = concept.pos_info
				output = "token= "+ token + ", SemType= " +semType + ", Offset= "+offset
				print ("token= "+token, " SemType= " +semType, " Offset= "+offset)
			break;

	return DrugnameElement("".join(output), 0, "DrugnameMetamapExtractor", "DRUGNAME")
	#return True
