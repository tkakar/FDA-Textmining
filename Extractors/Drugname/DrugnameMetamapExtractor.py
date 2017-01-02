# import re
# from Preprocessing.Preprocessor import Preprocessor
# from DataElements.DrugnameElement import DrugnameElement
#
#
# # from pymetamap import MetaMap
#
# class DrugnameMetamapExtractor(object):
#     def __init__(self, rawTextFileName, intermediateXMLFileName):
#         self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
#         self.Text = self.preprocess.rawText()
#
#     def findEntity(self):
        # the server installed on your machine
        # mm = MetaMap.get_instance('/work/tkakar/public_mm/bin/metamap14')
        #
        # #sample_Text = '/work/tkakar/FDAfirstNarrative.txt'
        # rawText = self.Text
        # #sents= self.Text
        # concepts,error = mm.extract_concepts([rawText], word_sense_disambiguation=True)
        # offset_list = []
        # drugs_list =[]
        # drug_offset_pair =()
        # for concept in concepts:
        # 	c= concept.semtypes
        # 	c =c.replace("[", "")
        # 	c = c.replace("]","")
        # 	semTypes= c.strip().split(",")
        # 	#print semTypes, type(semTypes)
        # 	for semType in semTypes:
        #
        # 		if semType in ['phsu' , 'orch']:
        # 			token = concept.trigger.strip().split("-")[0]
        # 			token = token.replace("[","")
        # 			#print concept.pos_info, "pos_info"
        # 			offset = self.preprocess.offsetParse(concept.pos_info,';')
        # 			#print offset , "offset" , len(offset)
        # 			for item in offset:
        # 				#print item ,item[1]
        # 				item[1] = item[0]+item[1]
        #
        #
        # 				#print ("offsetMetamap"  ,  item )
        # 				if item not in offset_list:
        # 					offset_list.append(item)
        # 					drugs_list.append(token)
        # drugs_list= [drug.replace('"',"") for drug in drugs_list]
        # #print len(drugs_list)
        # elementList = []
        # for drug,offset in zip(drugs_list,offset_list):
        # 	#print drug, type(drug), type(offset), [offset]
        #
        # 	elementList.append(DrugnameElement(drug, [offset], "DrugnameMetamapExtractor", "DRUGNAME"))
        #
        # #print len(elementList)
        # return elementList
