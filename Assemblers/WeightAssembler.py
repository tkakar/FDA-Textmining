"""WeightAssembler Class

This module is an implementation of the Assembler class described in the architecture. It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS. When Assemblers are created for other DataElements, simply copy this class, but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""

from Extractors.Weight.WeightRegExtractor import WeightRegExtractor
from Extractors.Weight.WeightNltkExtractor import WeightNltkExtractor


class WeightAssembler(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName, anExtractorList=[]):
        """
        Initializes the WeightAssembler and returns it. All Extractors for the Weight DataElement must be specified in the list below. 

        Args:
            anExtractorList (list): the list passed from the config file for Weight
        
        Returns:
            WeightAssembler Object
        """
        self.AllPossibleExtractorList = {"WeightRegExtractor":WeightRegExtractor(rawTextFileName, intermediateXMLFileName), "WeightNltkExtractor":WeightNltkExtractor(rawTextFileName, intermediateXMLFileName)}
        self.extractorList = anExtractorList
        self.extractorObjList = []

    def setExtractorList(self, aList):
        """Sets the extractor list by searching the dictionary for corresponding python objects.

        Args:
            aList (list): the list from the config file to look up and initialize extractors
            
        Returns:
            The created object list
        """
        self.extractorList = aList

        for extractor in self.extractorList:
            self.extractorObjList.append(self.AllPossibleExtractorList[extractor])
            
        return self.extractorObjList

    def getAllPossibleExtractors(self):
        """Gets the list of all possible extractors. Should really only be used for debugging. 

        Args:
            None
            
        Returns:
            all possible extractor dictionary list
        """
        return self.AllPossibleExtractorList

    def getExtractorObjList(self):
        """Gets the list of objects created from looking up the config file strings in the dictionary

        Args:
            None
            
        Returns:
            the list of extractor python objects 
        """
        return self.extractorObjList
           
    def runExtractors(self):
        """Runs all the extractors and returns DataElements.
        
        Args:
            None
            
        Returns:
            list of WeighteElements (list)

        TODO:
            Actually make it return DataElement list and make sure that won't cause problems
        """
        for extractor in self.extractorObjList:
            extractor.findWeight()

# def main():
#     extractorHandler = EventDateExtractorHandler('../test_cases/fda001.txt')
