"""EventDateAssembler Class

This module is an implementation of the Assembler class described in the architecture.

"""

from Extractors.EventDate.AERecognitionEventDateExtractor import AERecogExtractor
from Extractors.EventDate.SuspectRecognitionEventDateExtractor import SuspectRecogExtractor
from Extractors.EventDate.NaiveEventDateExtractor import NaiveExtractor 

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
