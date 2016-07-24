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
from test import Compare

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

            hasCharOffsetFlag = True
            if isinstance(ev_dataElem, (list, tuple)):
                for entity in ev_dataElem:
                    if not ev_dataElem and ev_dataElem.charOffset:
                        hasCharOffsetFlag = False

                if hasCharOffsetFlag:
                    self.dataElementList.append(ev_dataElem)

            elif ev_dataElem and ev_dataElem.charOffset:
                self.dataElementList.append(ev_dataElem)
            
   
# def main():
#     extractorHandler = EventDateExtractorHandler('../test_cases/fda001.txt')

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
      
        print "this is the dataelementlist: ", self.dataElementList
        for dataelements in self.dataElementList:
            if isinstance(dataelements, list):
                for dataelement in dataelements:
                    root = self.xmlWriterHelper(dataelement, root)
            else:
                root = self.xmlWriterHelper(dataelements, root)

        #We had to remove this and not use self.entityName because each returned element in self.dataElementList has more than one dataElement (each extractor returns more than one item)
        #edElem = root.find(self.entityName)
        etree._setroot(root)
        etree.write(outputXMLFN)
        
    def xmlWriterHelper(self, element, root):
        elem = ET.Element(element.entityName)
        print "thsi is the type of the charOffset: ", element.charOffset, type(element.charOffset)
        if isinstance(element.charOffset, tuple):
            start = str(element.charOffset[0])
            end = str(element.charOffset[1])
        else:
            start = str(element.charOffset[0][0])
            end = str(element.charOffset[-1][1])

        elem.attrib['start'] = start
        elem.attrib['end'] = end
        elem.attrib['extractor'] = element.extractorName
        elem.text = element.extractedField

        print "this is the element.entityname: ", element.entityName
        entityParent = root.find('.//'+element.entityName+'/..')
        entityParent.append(elem)

        print "I;m not sure this works!!!!!:::::", ET.dump(root)
        
        return root

    def launchTestSuite(self):
        self.filename
        # we need the annotation file and the program output file: Test_Suite/Eval_Env/xml/fda001.xml 
        # and Test_Suite/Eval_Env/semifinal/fda001_EVENT_DT_Semifinal.xml
        comp = Compare('Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', 'Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        #comp = Compare('../Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', '../Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        for elements in self.dataElementList:
            if isinstance(elements, list):
                for dataelement in elements:
                    comp.run_compare(dataelement.entityName, dataelement.extractorName) 
            else:
                comp.run_compare(elements.entityName, elements.extractorName) 
            

