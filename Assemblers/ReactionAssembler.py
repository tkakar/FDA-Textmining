"""ReactionAssembler Class

This module is an implementation of the Assembler class described in the architecture. It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS. When Assemblers are created for other DataElements, simply copy this class, but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""

from Extractors.Reaction.ReactionMetamapExtractor import ReactionMetamapExtractor 
from Extractors.Reaction.SVMv1ReactionExtractor import SVMv1ReactionExtractor
from Assemblers.EntityAssembler import EntityAssembler
import xml.etree.ElementTree as ET
from test import Compare


class ReactionAssembler(EntityAssembler):
    
    def __init__(self, rawTextFileName, intermediateXMLFileName, anExtractorList=[]):
        """
        Initializes the ReactionAssemblerand returns it. All Extractors for the Event Date DataElement must be specified in the list below. 

        Args:
            anExtractorList (list): the list passed from the config file for EventDate
        
        Returns:

            ReactionAssembler Object

        """
        super(ReactionAssembler, self).__init__(rawTextFileName, intermediateXMLFileName, anExtractorList=[])

        self.AllPossibleExtractorList = {"ReactionMetamapExtractor":ReactionMetamapExtractor (rawTextFileName, intermediateXMLFileName), "SVMv1ReactionExtractor":SVMv1ReactionExtractor(rawTextFileName, intermediateXMLFileName)}
        self.entityName = 'PT'
        self.filename = rawTextFileName
        self.testCaseName = self.filename[self.filename.rfind(r'/') + 1:self.filename.rfind(r'.txt')]


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
      
        for dataelements in self.dataElementList:
            if isinstance(dataelements, list):
                for dataelement in dataelements:
                    root = self.xmlWriterHelper(dataelement, root)
                    # print "iffff"
            else:
                root = self.xmlWriterHelper(dataelements, root)
                # print "else"

        #We had to remove this and not use self.entityName because each returned element in self.dataElementList has more than one dataElement (each extractor returns more than one item)
        #edElem = root.find(self.entityName)
        #ET.dump(root)
        etree._setroot(root)
        etree.write(outputXMLFN)
        
    def xmlWriterHelper(self, element, root):
        elem = ET.Element(element.entityName)
        #should be reading in a list of lists
        #print "THIS IS THE OFFSET WE ARE ERRORING ON: ", element.charOffset
        #TODO: Figure out if this is the best way, ideally each extractor should make this check, but don't have time right now. 
        #By this, I mean checking if the offset exists should be done in each extractor properly.
        if element.charOffset[0]:
           # print "if charOffset ************************"
            start = str(element.charOffset[0][0])
            end = str(element.charOffset[-1][1])

            elem.attrib['start'] = str(start)
            elem.attrib['end'] = str(end)
            elem.attrib['extractor'] = str(element.extractorName)
            elem.text = str(element.extractedField)
            superE = ET.Element("INSTANCE")
            superE.append(elem)
            entitySuperParent = root.find('.//'+element.entityName+'/../..')
            entitySuperParent.append(superE)
        return root

    def launchTestSuite(self):
        self.filename
        # we need the annotation file and the program output file: Test_Suite/Eval_Env/xml/fda001.xml 
        # and Test_Suite/Eval_Env/semifinal/fda001_EVENT_DT_Semifinal.xml
        comp = Compare('Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', 'Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        #comp = Compare('../Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', '../Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        for elements in self.dataElementList:
           # print elements[0].extractedField, elements[0].extractorName, elements[0].entityName
            ## if elements is null then might get error
            comp.multi_compare(elements[0].entityName, elements[0].extractorName) 
                
