"""WeightAssembler Class

This module is an implementation of the Assembler class described in the architecture. It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS. When Assemblers are created for other DataElements, simply copy this class, but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""

from Extractors.Weight.WeightRegExtractor import WeightRegExtractor
from Extractors.Weight.WeightNltkExtractor import WeightNltkExtractor
from Extractors.Weight.SVMv1WeightExtractor import SVMv1WeightExtractor

from Assemblers.EntityAssembler import EntityAssembler


class WeightAssembler(EntityAssembler):
    def __init__(self, rawTextFileName, intermediateXMLFileName, anExtractorList=[]):
        """
        Initializes the EventDateAssembler and returns it. All Extractors for the Event Date DataElement must be specified in the list below. 

        Args:
            anExtractorList (list): the list passed from the config file for EventDate
        
        Returns:
            EventDateAssembler Object
        """
        super(WeightAssembler, self).__init__(rawTextFileName, intermediateXMLFileName, anExtractorList=[])

        self.AllPossibleExtractorList = {
            "WeightRegExtractor": WeightRegExtractor(rawTextFileName, intermediateXMLFileName),
            "WeightNltkExtractor": WeightNltkExtractor(rawTextFileName, intermediateXMLFileName),
            "SVMv1WeightExtractor": SVMv1WeightExtractor(rawTextFileName, intermediateXMLFileName)}
        self.entityName = 'WT_SET'
        self.filename = rawTextFileName
        self.testCaseName = self.filename[self.filename.rfind(r'/') + 1:self.filename.rfind(r'.txt')]
