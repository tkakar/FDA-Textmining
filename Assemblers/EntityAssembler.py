"""EntityAssembler Class

This module is an implementation of the Assembler class described in the architecture. It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS. When Assemblers are created for other DataElements, simply copy this class, but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""

from Extractors.EventDate.AERecognitionEventDateExtractor import AERecognitionEventDateExtractor
from Extractors.EventDate.SuspectRecognitionEventDateExtractor import SuspectRecognitionEventDateExtractor
from Extractors.EventDate.NaiveEventDateExtractor import NaiveExtractor 
from Preprocessing.Preprocessor import Preprocessor
import xml.etree.ElementTree as ET

class EntityAssembler(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName, anExtractorList=[]):
        """
        Initializes the EventDateAssembler and returns it. All Extractors for the Event Date DataElement must be specified in the list below. 

        Args:
            anExtractorList (list): the list passed from the config file for EventDate
        
        Returns:
            EventDateAssembler Object
        """
        
        self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.AllPossibleExtractorList = {}
        self.extractorList = anExtractorList
        self.extractorObjList = []
        self.dataElementList = []
        self.entityName = ""
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
            list of EventDataElements (list)

        TODO:
            Actually make it return DataElement list and make sure that won't cause problems
        """
        for extractor in self.extractorObjList:
            ev_dataElem = extractor.findEntity()

            if ev_dataElem and ev_dataElem.charOffset:
                self.dataElementList.append(ev_dataElem)
            
    def writeToSemiFinalXML(self):

        filename = self.filename
        filename = filename[:filename.rfind('.txt')]
        testCaseName = filename[filename.rfind(r'/') + 1:]
        
        outputXMLFN = 'Test_Suite/Eval_Env/semifinal/'+testCaseName+'_'+self.entityName+'_Semifinal.xml'

        defXML = open('Test_Suite/XML/XML.xml')
        etree = ET.parse(defXML)
        root = etree.getroot()
        
        root.attrib['textSource'] = filename
        root.attrib['annotator'] = 'Project MEFA Program'

        edElem = root.find(self.entityName)
        
        #edElem.attrib['
        for dataelement in self.dataElementList:

            elem = ET.Element(self.entityName)
            start = str(dataelement.charOffset[0][0])
            end = str(dataelement.charOffset[-1][1])
                
            elem.attrib['start'] = start
            elem.attrib['end'] = end
            elem.attrib['extractor'] = dataelement.extractorName
            elem.text = dataelement.extractedField
                
            root.append(elem)

        etree.write(outputXMLFN)
        
# def main():
#     extractorHandler = EventDateExtractorHandler('../test_cases/fda001.txt')
