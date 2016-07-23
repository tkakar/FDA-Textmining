"""AgeAssembler Class

This module is an implementation of the Assembler class described in the architecture. It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS. When Assemblers are created for other DataElements, simply copy this class, but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""

from Extractors.Age.RegExpAgeExtractor import RegExpExtractor


class AgeAssembler(object):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName, anExtractorList=[]):
        """
        Initializes the EventDateAssembler and returns it. All Extractors for the Event Date DataElement must be specified in the list below. 

        Args:
            anExtractorList (list): the list passed from the config file for EventDate
        
        Returns:
            EventDateAssembler Object
        """
        super(EventDateAssembler, self).__init__(rawTextFileName, intermediateXMLFileName, anExtractorList=[])

        self.AllPossibleExtractorList = {"RegExpExtractor":RegExpExtractor(rawTextFileName, intermediateXMLFileName)}
        self.entityName = 'AGE'
        self.filename = rawTextFileName
        self.testCaseName = self.filename[self.filename.rfind(r'/') + 1:self.filename.rfind(r'.txt')]

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
#############################
    #You can do for each here and this should work maybe?... This sucks

#########################        
        for dataelements in self.dataElementList:
            if isinstance(dataelements, list):
                for dataelement in dataelements:
                    self.xmlWriterHelper(dataelement, root)
            else:
                self.xmlWriterHelper(dataelements, root)

        #We had to remove this and not use self.entityName because each returned element in self.dataElementList has more than one dataElement (each extractor returns more than one item)
        #edElem = root.find(self.entityName)

        etree.write(outputXMLFN)
        
    def xmlWriterHelper(self, element, root):
        elem = ET.Element(element.entityName)

        start = str(dataelement.charOffset[0][0])
        end = str(dataelement.charOffset[-1][1])

        elem.attrib['start'] = start
        elem.attrib['end'] = end
        elem.attrib['extractor'] = dataelement.extractorName
        elem.text = dataelement.extractedField

        entityParent = root.findall('.//'+element.entityName+'/..')
        entityParent.append(elem)

        return root
    
# def main():
#     extractorHandler = EventDateExtractorHandler('../test_cases/fda001.txt')
