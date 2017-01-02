"""EntityAssembler Class

This module is an implementation of the Assembler class described in the architecture. It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS. When Assemblers are created for other DataElements, simply copy this class, but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""
from Preprocessing.Preprocessor import Preprocessor
import xml.etree.ElementTree as ET
# from test import Compare
from pprint import pprint


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
            #	    pprint (vars(ev_dataElem))
            # pprint (vars(ev_dataElem._extractedField))
            hasCharOffsetFlag = True
            if isinstance(ev_dataElem, (list, tuple)):
                #	print ("ev_Data")
                for entity in ev_dataElem:
                    #	    print ev_dataElem.charOffset, ev_dataElem , "Testing in Isinstane()"
                    if not ev_dataElem and not ev_dataElem.charOffset:
                        #		  print "Reached: "
                        hasCharOffsetFlag = False

                if hasCharOffsetFlag:
                    self.dataElementList.append(ev_dataElem)

            elif ev_dataElem and hasattr(ev_dataElem, 'charOffset'):
                self.dataElementList.append(ev_dataElem)


            # def main():
            #     extractorHandler = EventDateExtractorHandler('../test_cases/fda001.txt')

    def writeToSemiFinalXML(self):

        filename = self.filename
        filename = filename[:filename.rfind('.txt')]
        testCaseName = filename[filename.rfind(r'/') + 1:]

        outputXMLFN = 'Test_Suite/Eval_Env/semifinal/' + testCaseName + '_' + self.entityName + '_Semifinal.xml'

        defXML = open('Test_Suite/XML/XML.xml')
        etree = ET.parse(defXML)
        root = etree.getroot()

        root.attrib['textSource'] = filename
        root.attrib['annotator'] = 'Project MEFA Program'

        for dataelements in self.dataElementList:
            # print dataelements
            if isinstance(dataelements, list):
                #	print "dataeleemet is instance of list"
                for dataelement in dataelements:
                    #	    print "dataelement extracted: ", dataelement.extractedField
                    #	    print "dataelement extracted2: ", dataelement.charOffset
                    root = self.xmlWriterHelper(dataelement, root)
            else:
                #	print "dataleemnt extracted3: ", dataelements.charOffset
                root = self.xmlWriterHelper(dataelements, root)

        # We had to remove this and not use self.entityName because each returned element in self.dataElementList has more than one dataElement (each extractor returns more than one item)
        # edElem = root.find(self.entityName)
        etree._setroot(root)
        etree.write(outputXMLFN)

    def xmlWriterHelper(self, element, root):
        elem = ET.Element(element.entityName)
        # print elem, element.entityName, element.charOffset ,"000000000"
        # should be reading in a list of lists
        # print "Element extracted field: ", element.extractedField
        # print "THIS IS THE OFFSET WE ARE ERRORING ON: ", element.charOffset
        # TODO: Figure out if this is the best way, ideally each extractor should make this check, but don't have time right now.
        # By this, I mean checking if the offset exists should be done in each extractor properly.
        if element.charOffset[0]:
            start = str(element.charOffset[0][0])
            end = str(element.charOffset[-1][1])

            elem.attrib['start'] = str(start)
            elem.attrib['end'] = str(end)
            elem.attrib['extractor'] = str(element.extractorName)
            elem.text = str(element.extractedField)

            # print 'element.entityName: ', element.entityName
            entityParent = root.find('.//' + element.entityName + '/..')
            # print "This is the element: ", ET.dump(elem)
            entityParent.append(elem)

        return root

    def launchTestSuite(self):
        self.filename
        # # we need the annotation file and the program output file: Test_Suite/Eval_Env/xml/fda001.xml
        # # and Test_Suite/Eval_Env/semifinal/fda001_EVENT_DT_Semifinal.xml
        # comp = Compare('Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', 'Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        # #comp = Compare('../Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', '../Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        # for elements in self.dataElementList:
        #     if isinstance(elements, list):
        #         for dataelement in elements:
        #             comp.run_compare(dataelement.entityName, dataelement.extractorName)
        #     else:
        #         comp.run_compare(elements.entityName, elements.extractorName)
