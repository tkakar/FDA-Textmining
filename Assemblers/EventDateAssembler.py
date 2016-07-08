import re
import nltk
from nltk import word_tokenize, sent_tokenize, data
from nltk_contrib import timex 
from AERecognitionEventDateExtractor import AERecogExtractor
from SuspectRecognitionEventDateExtractor import SuspectRecogExtractor
from NaiveEventDateExtractor import NaiveExtractor 
import sys
sys.path.append('/home/vsocrates/My_Documents/fda_textmining/FDA-Textmining/')
nltk.data.path.append('/work/vsocrates/nltk_data/')

class EventDateAssembler(object):
    
    def __init__(self, anExtractorList=[]):
        self.AllPossibleExtractorList = {"AERecogExtractor":AERecogExtractor(), "SuspectRecogExtractor":SuspectRecogExtractor(), "NaiveEventDateExtractor":NaiveExtractor()}
        self.extractorList = anExtractorList
        self.extractorObjList = []
    def setExtractorList(self, aList):
        self.extractorList = aList

        for extractor in self.extractorList:
            self.extractorObjList.append(self.AllPossibleExtractorList[extractor])

    def getAllPossibleExtractors(self):
        return self.AllPossibleExtractorList

    def getExtractorObjList(self):
        return self.extractorObjList
           
    def runExtractors(self):
        for extractor in self.extractorObjList:
            extractor.findDates()

# def main():
#     extractorHandler = EventDateExtractorHandler('../test_cases/fda001.txt')
