import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DrugnameElement import DrugnameElement


class DrugnameRegExtractor(object):
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Tokens = self.preprocess.wordTokenizeText()

    def findEntity(self):

        with open("/Users/wutianyu/ISP2016/Drugslist.txt") as myfile:
            drugnames = myfile.read().splitlines()

        Drug_list = []
        for tokens in self.Tokens:
            for token in tokens:
                token = token.lower()
                ###tokens have some unicode u character which needs to be removed
                token = token.encode('utf-8')
                if token in [item.lower() for item in drugnames]:
                    Drug_list.append(token)

        elementList = []
        if not Drug_list:
            print ("Drugname not found:")
        else:
            for i in range(0, len(Drug_list)):
                ##### THe offset cannot be same number or empty, so assigning random numbers
                # print Drug_list[i], "drug", [[i*i+10,i*i+25]]
                elementList.append(
                    DrugnameElement(Drug_list[i], [[i * i + 10, i * i + 25]], "DrugnameRegExtractor", "DRUGNAME"))
            return elementList
