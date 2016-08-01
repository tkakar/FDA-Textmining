import re
import xml.etree.ElementTree as ET
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DrugnameElement import DrugnameElement


class DrugnameRegExtractor(object):
    

    def __init__(self, rawTextFileName, intermediateXMLFileName):
        self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Tokens = self.preprocess.wordTokenizeText()
        self.intermediate = intermediateXMLFileName

    def findEntity(self):

        tree = ET.parse(self.intermediate)
        with open("/work/tkakar/git-repos/FDA-Textmining/Drugslist.txt") as myfile:
            drugnames= myfile.read().splitlines()

        Drug_list=[]
        postags = []
        drugname_offset = []
        elementList =[]
        for paragraphs in tree.getroot()[0]: 
            for paragraph in paragraphs:    
                for sentence in paragraph:
                    #print sentence
                    Tokens = sentence.find("Tokens")
                    tokens = Tokens.findall("Token")
            
                            
                for index, token in enumerate(tokens):
                    postags.append((str(token[0].text)+";"+str(tokens[index].get('offset'))))
       
        for tokens in postags:
            d_offset = []
            # print tokens
            drug = tokens.split(";")[0]
            offset = tokens.split(";")[1]
            drug= drug.lower()
            # print drug#, offset
            if drug in [item.lower() for item in drugnames]:
                 Drug_list.append(drug)
                 #print offset, type(offset),  offset.split(':')[1] ,  type(offset.split(':')[1])
                 d_offset.append(int(offset.split(':')[0]))
                 d_offset.append(int(offset.split(':')[1]))
                 drugname_offset.append (d_offset)   
                 d_offset= []
        #print drugname_offset, Drug_list 
        if not Drug_list:
            print ("Drugname not found: \n")
            return False
        else:
            print "Drugs from Regex\n"
            for i in range (0,len(Drug_list)):
                ##### THe offset cannot be same number or empty, so assigning random numbers
                print Drug_list[i], [drugname_offset[i]]
                elementList.append(DrugnameElement(Drug_list[i],[drugname_offset[i]],"DrugnameRegExtractor","DRUGNAME"))
            return elementList
       
