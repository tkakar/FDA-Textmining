import re
import nltk
from nltk import word_tokenize, sent_tokenize, data
from nltk_contrib import timex 
from AERecognitionEventDateExtractor import AERecogExtractor
from SuspectRecognitionEventDateExtractor import SuspectRecogExtractor
import sys
sys.path.append('/home/vsocrates/My_Documents/fda_textmining/FDA-Textmining/')
nltk.data.path.append('/work/vsocrates/nltk_data/')
import ExtractorHandler

class EventDateExtractorHandler(object):
    
    def __init__(self, anExtractorList):
        self.AllPossibleExtractorList = ["AERecogExtractor":AERecogExtractor, "SuspectRecogExtractor":SuspectRecogExtractor,
                              "NaiveEventDateExtractor":NaiveExtractor]

        for extractor in anExtractorList:
            self.extractorList.append(self.AllPossibleExtractorList[extractor])
        
    def getAllPossibleExtractors(self):
        return self.AllPossibleExtractorList

    def getExtractorList(self):
        return self.extractorList
           
    def runExtractors():
        for extractor in self.extractorList:
            extractor.findDates()

def main():
    extractorHandler = EventDateExtractorHandler('../test_cases/fda001.txt')
