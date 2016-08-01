import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DrugnameElement import DrugnameElement
from pymetamap import MetaMap

class DrugnameMetamapExtractor(object):
    

    def __init__(self, rawTextFileName, intermediateXMLFileName):
        self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = self.preprocess.rawText()
        
    def findEntity(self):
        mm = MetaMap.get_instance('/work/tkakar/public_mm/bin/metamap14')
        rawText = self.Text
        concepts,error = mm.extract_concepts([rawText], word_sense_disambiguation=True)
        offset_list = []
        drugs_list =[]
        elementList = []

        if concepts:
            for concept in concepts:
                if not hasattr(concept, 'aa'):
                    c= concept.semtypes
                    c =c.replace("[", "")
                    c = c.replace("]","")
                    semTypes= c.strip().split(",")
                    for semType in semTypes:
                        if semType in ['phsu' , 'orch']:
                            token = concept.trigger.strip().split("-")[0]
                            token = token.replace("[","")
                            offset = self.preprocess.offsetParse(concept.pos_info,';')
                            for item in offset:
                                item[1] = item[0]+item[1]
                                if item not in offset_list:
                                    offset_list.append(item)
                                    drugs_list.append(token)
                
        if drugs_list:
             drugs_list= [drug.replace('"',"") for drug in drugs_list]
             for drug,offset in zip(drugs_list,offset_list):
                print "MetamapDrug:  ", drug,[offset]
                elementList.append(DrugnameElement(drug, [offset], "DrugnameMetamapExtractor", "DRUGNAME"))

             return elementList
     
        else:
            print "Drug not found!!"
            return False
   

                

                    
                    
