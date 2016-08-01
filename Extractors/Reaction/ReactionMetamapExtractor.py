import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.ReactionElement import ReactionElement
from pymetamap import MetaMap

class ReactionMetamapExtractor(object):
    

    def __init__(self, rawTextFileName, intermediateXMLFileName):
        self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = self.preprocess.rawText()
        
    def findEntity(self):

    # the server installed on your machine
        mm = MetaMap.get_instance('/work/tkakar/public_mm/bin/metamap14')

        #sample_Text = '/work/tkakar/FDAfirstNarrative.txt'
        rawText = self.Text
        #sents= self.Text
        concepts,error = mm.extract_concepts([rawText], word_sense_disambiguation=True)
        offset_list = []
        Reactions_list =[]

        for concept in concepts:
            if not hasattr(concept, 'aa'):
                c= concept.semtypes
                c =c.replace("[", "")
                c = c.replace("]","")
                semTypes= c.strip().split(",")
                #print semTypes, type(semTypes)
                for semType in semTypes:
                    
                    if semType in ['dsyn' , 'sosy']:
                        token = concept.trigger.strip().split("-")[0]
                        token = token.replace("[","")
                        #print concept.pos_info, "pos_info"
                        offset = self.preprocess.offsetParse(concept.pos_info,';')
                        #print offset , "offset" , len(offset)
                        for item in offset:
                            #print item ,item[1]
                            item[1] = item[0]+item[1]

                            
                            #print ("offsetMetamap"  ,  item )
                            if item not in offset_list:
                                offset_list.append(item)
                                Reactions_list.append(token)
        Reactions_list= [reaction.replace('"',"") for reaction in Reactions_list]
        #print len(drugs_list)
        elementList = []
        if not Reactions_list:
            print "Reaction not found"
            return False
        else:
            for reaction,offset in zip(Reactions_list,offset_list):
                print reaction, [offset]

                elementList.append(ReactionElement(reaction, [offset], "ReactionMetamapExtractor", "PT"))

            #print len(elementList)
            return elementList
