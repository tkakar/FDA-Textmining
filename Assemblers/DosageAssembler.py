"""DosageAssembler Class

This module is an implementation of the Assembler class described in the architecture. It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS. When Assemblers are created for other DataElements, simply copy this class, but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""

from Extractors.Dosage.DosageRegExtractor import DosageRegExtractor 
from Preprocessing.Preprocessor import Preprocessor
from Assemblers.EntityAssembler import EntityAssembler
import xml.etree.ElementTree as ET

class DosageAssembler(object):

    def __init__(self, rawTextFileName, intermediateXMLFileName, anExtractorList=[]):
        """
        Initializes the EventDateAssembler and returns it. All Extractors for the Event Date DataElement must be specified in the list below. 

        Args:
            anExtractorList (list): the list passed from the config file for EventDate
        
        Returns:
            EventDateAssembler Object
        """
        super(DosageAssembler, self).__init__(rawTextFileName, intermediateXMLFileName, anExtractorList=[])

        self.AllPossibleExtractorList = {"DosageRegExtractor":DosageRegExtractor(rawTextFileName, intermediateXMLFileName)}
        #TODO: We need to figure out the best way to get this to work.
        self.entityName = 'DOSAGE'

    def launchTestSuite(self):
        self.filename
        # we need the annotation file and the program output file: Test_Suite/Eval_Env/xml/fda001.xml 
        # and Test_Suite/Eval_Env/semifinal/fda001_EVENT_DT_Semifinal.xml
        comp = Compare('Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', 'Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        #comp = Compare('../Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', '../Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        for element in self.dataElementList:
            comp.run_compare(self.entityName, element.extractorName) 


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

        for 
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
        