"""EventDateAssembler Class

This module is an implementation of the Assembler class described in the architecture.
It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS.
When Assemblers are created for other DataElements, simply copy this class,
but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""
from Extractors.EventDate.AERecognitionEventDateExtractor import AERecognitionEventDateExtractor
from Extractors.EventDate.SuspectRecognitionEventDateExtractor import SuspectRecognitionEventDateExtractor
from Extractors.EventDate.NaiveEventDateExtractor import NaiveEventDateExtractor
from Extractors.EventDate.SVMv1EventDateExtractor import SVMv1EventDateExtractor
from Preprocessing.Preprocessor import Preprocessor
from Assemblers.EntityAssembler import EntityAssembler
import xml.etree.ElementTree as ET


class EventDateAssembler(EntityAssembler):
    def __init__(self, rawTextFileName, intermediateXMLFileName, anExtractorList=[]):
        """
        Initializes the EventDateAssembler and returns it. All Extractors for the Event Date DataElement must be specified in the list below. 

        Args:
            anExtractorList (list): the list passed from the config file for EventDate
        
        Returns:
            EventDateAssembler Object
        """
        super(EventDateAssembler, self).__init__(rawTextFileName, intermediateXMLFileName, anExtractorList=[])

        self.AllPossibleExtractorList = {
            "AERecogExtractor": AERecognitionEventDateExtractor(rawTextFileName, intermediateXMLFileName),
            "SuspectRecogExtractor": SuspectRecognitionEventDateExtractor(rawTextFileName, intermediateXMLFileName),
            "NaiveEventDateExtractor": NaiveEventDateExtractor(rawTextFileName, intermediateXMLFileName)}
        # , "SVMv1EventDateExtractor":SVMv1EventDateExtractor(rawTextFileName, intermediateXMLFileName) }
        self.entityName = 'EVENT_DT'
        self.filename = rawTextFileName
        self.testCaseName = self.filename[self.filename.rfind(r'/') + 1:self.filename.rfind(r'.txt')]

# def main():
#     extractorHandler = EventDateExtractorHandler('../test_cases/fda001.txt')
