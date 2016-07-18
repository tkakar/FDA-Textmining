"""Preprocessor Class
This module contains all of the methods to preprocess the data and pass them to the extractors. This may include tokenization, POS tagging, or tagging a specific named entity concept with preliminary tags (temporal, MetaMap).

IMPORTANT:
When creating new methods, make sure to check the dictionary (textList) to see if the particular format of a test case that you want already exists before creating it. If it doesn't exist, create it and place it into textList with the key being the name of the method you write. This will help in minimizing File I/O and standardize the dictionary so people can find other versions of narratives. 

Preprocessed Text Support (so far):

  +Word Tokenization
  +Sentence and Paragraph tokenization (in XML only)
  +Timex2 tagging
  +tokenization after timex2 tagging
  +Part-of-speech tagging (POS)
  +Parse tree creation
  +MetaMap concept recognition

Todo:
    * Fix dictionary (textList)  key phrase, so it doesn't have to rely on programmer accuracy
    * Update timexTagText and wordTokenizeText methods (possibly also wordTokenizeAndTagMethod)
    * Add method to allow choice of tokenization method (BLIIP or NLTK)
    * There is an issue with the sent_tokenize() method for nltk when spaces are added in front (issue tracked)
"""

import sys, re
from nltk_contrib import timex
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import MWETokenizer
from nltk import pos_tag
import xml.etree.ElementTree as ET
from bllipparser import RerankingParser
from pymetamap import MetaMap

"""The class below (taken from http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html) is an implementation of the Singleton design pattern that allows for all instances created of the preprocessor to refer to the same namespace, allowing usage of the textList dictionary
"""
class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class Preprocessor(Borg):
    _firstInitialization = True
    def __init__(self, rawTextFileName=None, intermediateXMLFileName=None):
        """Initializes the Preprocessor and returns it. This includes loading any models that will be used in multiple preprocessing methods (e.g. RerankingParser)

        Args:
            rawTextFileName (str): The name of the raw string narrative file
            intermediateXMLFileName (str): The name of the BLANK file to contain the intermediate output XML

        Returns:
            Preprocessor object

        """

        Borg.__init__(self)
        if Preprocessor._firstInitialization:
                self.rrp = RerankingParser.fetch_and_load('GENIA+PubMed')
                Preprocessor._firstInitialization = False

                if rawTextFileName is not None:
                    self.filename = rawTextFileName
                    """IMPORTANT: The list below stores multiple different forms of text, to minimize the amount of computation""" 
                    self.textList = {}

#Initialize the XML file (minimizes XML I/O)
                    self.xmlname = intermediateXMLFileName
                    self.parseText()

            #print file
                else:
                    print "Need a text file!"
                    return
    def getList(self):
        return self.textList

    def parseText(self):
        """Creates the XML object and parses the raw narrative into the ElementTree python object. This method parses paragraphs, sentences,
        and tokenizes the text. Any additional features that need to be added into the XML file must have their own methods. 
           
        Args:
            None
        
        Returns:
            None
            It does write the parsed text to the file specified in the initializer

        """
        self.file = open(self.filename)
        raw = self.file.read()
        rawOffsetIntermed = raw
        offsetIter = 0
        offsetIterSent = 0
        self.tree = ET.ElementTree(ET.Element('StartOutput'))
        self.root = self.tree.getroot()
        paraParent = ET.SubElement(self.root,'Paragraphs')
        globalIDIndex = 0
        """Now we are breaking up by paragraph"""
        paraSplit = re.compile('\n').split(raw)
        #Originally, we were using RegEx to remove all the empty space elements in the list, but they are all '', so we are just going to compare directly for that. Use this again if you find that that is no longer the case. 
#        paragraphPattern = re.compile('[^\s*]')
#        paragraphs = [i for i in paraSplit if not paragraphPattern.match(i)]
        paragraphs = [i for i in paraSplit if not i is '']

        paraParent.set('Count', str(len(paragraphs)))
        
        for index, paragraph in enumerate(paragraphs):
            tempParaElement = ET.Element('Paragraph', attrib={'id':str(index)})

#We aren't currently including the paragraph text in the <Paragraph /> tag
#            tempParaElement.text =  paragraph
            paraParent.append(tempParaElement)            
            
            """Now we have to sentence tokenize the text"""
            sentList = sent_tokenize(paragraph)
            sentParent = ET.Element('Sentences')
            sentParent.set('Count', str(len(sentList)))
            tempParaElement.append(sentParent)
            for index, sent in enumerate(sentList):
                offsetIndexSent = rawOffsetIntermed.find(sent, offsetIterSent)
                tempSentElement = ET.Element('Sentence', attrib={'id':str(index), 'offset':str(offsetIndexSent)+':'+str(offsetIndexSent+len(sent))})
                sentTextElem = ET.Element('Text')
                sentTextElem.text = sent
                tempSentElement.append(sentTextElem)
                sentParent.append(tempSentElement)
                offsetIterSent = offsetIndexSent 
                """Now we have to break it down by token"""
                tokensList = word_tokenize(sent)
                tokenParent = ET.Element('Tokens')
                tokenParent.set('Count', str(len(tokensList)))
                tempSentElement.append(tokenParent)
                for index, word in enumerate(tokensList):
                    offsetIndex = rawOffsetIntermed.find(word, offsetIter)
                    tempWordElement = ET.Element('Token', attrib={'id':str(index), 'globalID':str(globalIDIndex),'offset':str(offsetIndex)+':'+ str(offsetIndex+len(word))})
                    textElem = ET.Element('Text')
                    textElem.text = word
                    tempWordElement.append(textElem) 
                    tokenParent.append(tempWordElement)
                    offsetIter = offsetIndex
                    globalIDIndex += 1

#        ET.dump(self.root)
        self.writeToXML()
        self.file.close()

    def rawText(self):
        """Returns the raw string (usually only used for RegEx extractors that don't want any preprocessing/XML)

        Args:
            None
            
        Returns
            The raw string from the text file (str)
        """
        if self.textList.get('rawText') is None:
            self.textList['rawText'] = open(self.filename).read()
            self.file.close()
        return self.textList.get('rawText')

    def timexTagText(self, altText=None):
        """Tags all the temporal expressions and surrounds them with <TIMEX2> XML tags in line with the text

        Args:
            altText (str) The text to be tagged, if it is not the same as the whole narrative the preprocessor was created with. This text won't be stored.
            
        Returns:
            tagged text (str)
        
        """

        """When altText is specified, the method assumes that some random text is being sent to be tagged, so doesn't save in dictionary"""
        if altText is not None:
            raw = altText
            altOutput = timex.tag(raw)
            return altOutput

        else:
            """Otherwise, we first check if it exists in the textList dict, if not, it is created and returned"""
            self.file = open(self.filename)
            raw = self.file.read()
            if self.textList.get('timexTagText') is None:
                self.textList['timexTagText'] = timex.tag(raw)

            self.file.close()

        return self.textList.get('timexTagText')

 

    def wordTokenizeText(self, altText=None):
        """Tokenizes all the words currently using the nltk TreebankTokenizer for words, and the Punkt sentence tokenizer.
        
        Args:
            altText (str) The text to be tagged, if it is not the same as the whole narrative the preprocessor was created with. This text won't be stored.

        Returns:
            tokenized text (nested list, by sentence): 
            ex. [['This', 'is', 'a', 'sentence', '.'],['And', 'maybe', 'another']]
        """
        if altText is not None:
            raw = altText
            altTokenizedText  = [word_tokenize(t) for t in sent_tokenize(raw)]
            return altTokenizedText

        else:
            self.file = open(self.filename)
            raw = self.file.read()
            if self.textList.get('wordTokenizeText') is None:
                self.textList['wordTokenizeText'] = [word_tokenize(t) for t in sent_tokenize(raw)]

            self.file.close()

        return self.textList.get('wordTokenizeText')


    def timexTagAndTokenizeText(self, altText=None):
        """Tags temporal expressions with nltk timex2, and tokenizes the resultant text.

        Args:
            altText (str) The text to be tagged, if it is not the same as the whole narrative the preprocessor was created with. This text won't be stored.
        
        Returns:
            tokenized text (nested list, by sentence): 
            ex. [['This', 'is', 'a', 'sentence', '.'],['And', 'maybe', 'another']]

        """

        """In this method, two steps are required, so if altText is specified, all steps are done inside the if statement, so incorrect dict entries aren't stored"""
        if altText is not None:
            raw = altText
            altOutputStep1 = self.timexTagText(raw)
            altOutputStep2 = self.wordTokenizeText(altOutputStep1)
            time_tagged_and_tokenizedText = MWETokenizer(mwes=[('<','/TIMEX2','>'),('<','TIMEX2','>')], separator='').tokenize(altOutputStep2)
            
            return time_tagged_and_tokenizedText
        else:
            """Tag all temporal expressions with timex2 tags."""          
            """Don't need to open file here, because it's opened in timexTagText()"""
            tagged = self.timexTagText()
            """Word-tokenize all text above"""
            word_tagged = self.wordTokenizeText(tagged)
            
        '''consolidate all broken apart Timex2 tags into single "words"'''
        if self.textList.get('timexTagAndTokenizeText') is None:
            nestedListOutput = [MWETokenizer(mwes=[('<','/TIMEX2','>'),('<','TIMEX2','>')], separator='').tokenize(x) for x in word_tagged]
            
            #We need to remove and change this line if we don't want flattened (one dimensional list). Read below comment.
            self.textList['timexTagAndTokenizeText'] = [item for sublist in nestedListOutput for item in sublist]

        """Currently, the output is a flattened list, we need to decide if we want to keep the sentence structure (making the output a list of lists.
        This throws off the AEExtractor and the SuspectExtractor, which need to then be fixed."""
#        print self.textList.get('timexTagAndTokenizeText')
        return self.textList.get('timexTagAndTokenizeText')

    def posTaggedText(self, altText=None):
        """Tags the text with parts-of-speech (POS) using the Charniak-Johnson parser after nltk tokenizes the words using the Penn Treebank tokenizer. 

        Args:
            altText (str) The text to be tagged, if it is not the same as the whole narrative the preprocessor was created with. This text won't be stored.
        
        Returns:
            the POS-tagged text (nested list)
            ex. [[('A', 'DT'), ('female', 'JJ'), ('patient', 'NN'), ('died', 'VBD'), ('while', 'IN'), ('receiving', 'VBG'), ('Taxol', 'NN'), ('therapy', 'NN'), ('.', '.')], [('She', 'PRP'), ('did', 'VBD'), ("n't", 'RB'), ('surive', 'VB'), ('.', '.')]]
        
        """
        self.parseXML()

        if altText is not None:
            raw = altText
            altOutputStep1 = self.wordTokenizeText(raw)
            altOutputStep2 = [self.rrp.tag(sent) for sent in altOutputStep1]
            return altOutputStep2
        else:

            posTaggedSents = []
            paragraphs = self.root.find('Paragraphs')
            for paragraph in paragraphs.findall('Paragraph'):
                sentences = paragraph.find('Sentences')
                for sentence in sentences.findall('Sentence'):
                    tokens = sentence.find('Tokens')
#We have to take the first element, because for some reason, wordTokenizeText outputs a nested list, even with only one sentence
                    posTagList = self.rrp.tag(self.wordTokenizeText(sentence.find('Text').text)[0])
                    posTaggedSents.append(posTagList)
                    for index, token in enumerate(tokens.findall('Token')):
                        token.attrib['POSTag'] = posTagList[index][1]

                        
        self.writeToXML()
        return posTaggedSents
    
    def getParseTree(self, altText=None):
        """
        Creates a parse tree using the POS tags in the intermediate XML (the method above) and the Charniak-Johnson parser. 
        
        Args:
            altText (str) The text to be tagged, if it is not the same as the whole narrative the preprocessor was created with. This text won't be stored.
        
        Returns:
            The parse tree created (str)
        """

        self.parseXML()
        """In order to use the BLLIP parser (Charniak-Johnson parser) we must tokenize by sentence first. When using the alternate text option
        you have to only pass it individual sentences, like other methods (TODO: make sure this is the case for other methods)
        """
        if altText is not None:
            raw = altText
            altOutputStep1 = self.wordTokenizeText(raw)
            altParseTree = self.rrp.simple_parse(altOutputStep1)
            return altParseTree
        else:
#            self.file = open(self.filename)
#            raw = self.file.read()
#            root = ET.fromstring(open(self.xmlname).read())

#Since we are doing an I/O anyway to input the new XML tags, we don't have to retokenize, and can use the information from the base XML document
#            sent_tokens = sent_tokenize(raw)
#            output = [rrp.simple_parse(sent) for sent in sent_tokens]

            paragraphs = self.root.find('Paragraphs')
            for paragraph in paragraphs.findall('Paragraph'):
                sentences = paragraph.find('Sentences')
                for sentence in sentences.findall('Sentence'):
                    tempParseTreeElement = ET.Element('ParseTree')
#We have to take the first element, because for some reason, wordTokenizeText outputs a nested list, even with only one element
                    tempParseTreeElement.text = self.rrp.simple_parse(self.wordTokenizeText(sentence.text)[0])
                    sentence.append(tempParseTreeElement)

#        ET.dump(tree.getroot())
#            print output
        self.writeToXML()
#        ET.dump(self.root)
        return self.root
        
    def getMetaMapConcepts(self, altText=None):
        """
        Returns the MetaMap concepts found using the 'pymetamap' python wrapper. 
        
        Args:
            altText (str) The text to be tagged, if it is not the same as the whole narrative the preprocessor was created with. This text won't be stored.
        
        Returns:
            the MetaMap concepts, as described in the pymetamap documentation (list)
        """
        self.parseXML()
        mm = MetaMap.get_instance('/work/tkakar/public_mm/bin/metamap14')
        rawText = self.rawText()

        concepts,error = mm.extract_concepts([rawText])
        pattern = re.compile('(\[(?:(orch|phsu|sosy|dsyn),?(orch|phsu|sosy|dsyn)?)\])')
        globalIDByConcept = {}
        testCount = 0
        for concept in concepts:


            if testCount > 1:
                break

            #TODO, see if there is any information that we are missing due to some combination not described by the Regex
            match = pattern.search(concept.semtypes)
            if match:
                posInfo = concept.pos_info
                triggerInfo = concept.trigger.split('-')
                conceptName = triggerInfo[3]
                #need to replace the quotes in the conceptName
                conceptName = conceptName.replace('"','')

                if ';' or '^' in posInfo:
                    posInfoList = self.offsetParse(posInfo, ';')
                else:
                    posInfoList = self.offsetParse(posInfo)
                #We need to change the format of the posInfos from (offset,span) to (offsetStartIndex, offsetEndIndex) here:
                posInfoList = [(offset,span + offset) for (offset,span) in posInfoList]        

                
                for listIndex, (startIndex, endIndex) in enumerate(posInfoList):
                    lfNum = rawText.count('\n',0,startIndex) 
                    lastIdx = rawText.rfind(conceptName, 0, startIndex+len(conceptName))
                    #you're going to forget this tomorrow morning, so this is the number of line feeds between the last instance of the concept name and where metamap thinks the word is.
                    lfNumSpecific = rawText.count('\n', lastIdx,startIndex)
                    
                    posInfoList[listIndex] = (startIndex - (lfNum + 1) + lfNumSpecific, endIndex - (lfNum + 1) + lfNumSpecific)
                    
                    
                
#                print 'concept: ', conceptName, 'posInfoList', posInfoList
                
                globalIDList = []
                #we have the fixed offsets for each mention of the semantic type. we now need to find their location in the xml file. 
                for newStartIdx, newEndIdx in posInfoList:
#                    print 'tokniezedword: ',  word_tokenize(conceptName), 'nestadfasd;l: ', newStartIdx
                    globalIds = self.placeOffsetInXML(conceptName, word_tokenize(conceptName), newStartIdx , newEndIdx-newStartIdx)
#                    print 'concept: ', conceptName, 'globalIDs: ', globalIds
                    globalIDList.append(globalIds)

                globalIDByConcept[concept] = globalIDList

#        print globalIDByConcept
                
#                self.root.findall(".//[@globalID="+str(
#                print 'globalIDByConcept', globalIDByConcept
        for key, value in globalIDByConcept.iteritems():
            for gIDList in value:
                for gID in gIDList:
                    # print 'key:  ', key, 'GID:  ', gID
                    conceptXMLTag = self.root.find(".//*[@globalID='"+str(gID)+"']")
                # print 'conceptXMLTAG: ', conceptXMLTag.find('Text').text
                    tempMetaMapElem = ET.Element("METAMAP")
                    tempMetaMapElem.text = key.semtypes.replace("'",'')
                    conceptXMLTag.append(tempMetaMapElem)
        self.writeToXML()
        self.file.close()
    # def getMetaMapConceptsSent(self, altText=None):
    #     mm = MetaMap.get_instance('/work/tkakar/public_mm/bin/metamap14')
    #     rawText = self.rawText()
    #     sentences = sent_tokenize(rawText)
    #     pattern = re.compile('(\[(?:(orch|phsu|sosy|dsyn),?(orch|phsu|sosy|dsyn)?)\])')

    #     for sentence in sentences:
    #         concepts,error = mm.extract_concepts(sentence)
    #         for concept in concepts:
    #         #TODO, see if there is any information that we are missing due to some combination not described by the Regex
    #             match = pattern.search(concept.semtypes)
    #             if match:
    #                 print concept
    #                 posInfo = concept.pos_info
    #                 offsetList = self.offsetParse
    #                 if ';' or '^' in posInfo:
    #                     posInfoList = self.offsetParse(posInfo, ';')
    #                 else:
    #                     posInfoList = self.offsetParse(posInfo)
    #                 posInfoList = [(offset,span + offset) for (offset,span) in posInfoList]
    #                 wordsList = word_tokenize(sentence)
    #                 for word in wordsList:
    #                     if concept.preferred_name.lower() == word.lower():
    #                         pass
    def writeToXML(self):
        """Writes the tree to the output xml specified.

        Args:
            None

        Returns:
            None
        """
        self.tree.write(self.xmlname)

    def parseXML(self):
        """Parses the XML tree in the xml file specified. This method was created to minimize file I/Os.
        
        Args:
            None

        Returns:
            None
        """
        self.tree = ET.parse(self.xmlname)
        self.root = self.tree.getroot()

    def placeOffsetInXML(self, phrase, tokenizedText,offset, span):
        """Takes a word/phrase and finds the globalIDs of the tokens in the intermediate XML that this word/phrase corresponds to. 
    
        Args:
            phrase (str) The string to be placed in XML
            tokenizedText (list) The tokenized text is used to ensure that the same tokenizer used on the rest of the document is kept consistent. 
            offset (int) The offset, in relation to the original text file
            span (int) The length of the string (currently unused)
        Returns:
            List of globalIDs (for tokens) that match the phrase (list) 
        """
        self.parseXML()
        tokenLength = len(tokenizedText)
        tokens = self.root.findall(".//Token")
        idsReturned = 0
        globalIDList = []
        foundOffsetFlag = False
        for token in tokens:
            if idsReturned >= tokenLength:
                break
#            print "token.attrib['offset']: ", self.offsetParse(token.attrib['offset'])
            #In this case, we only ever get one offset at a time, so we don't loop through them. Just take the first (and only) element.
            (tokenStart, tokenEnd) = self.offsetParse(token.attrib['offset'])[0]
            if (offset == tokenStart or foundOffsetFlag):
                foundOffsetFlag = True
                globalIDList.append(int(token.attrib['globalID']))
                idsReturned += 1

        return globalIDList

    def offsetParse(self, offsetStr,delimiter=None):
        """Finds the offset and returns a tuple of starting and ending indices based on XML Format (0:34). Support multiple offsets, with delimiter specified. Returns in list format, even with only one element to keep consistency"""
        offsetIntList = []
        if delimiter is not None:
            """For some reason, the case where offsetParse() is used in the MetaMap preprocessing, sometimes the delimiter (that is normally a colon[:]) is replaced (randomly, it seems) or by a carrot (^)
            The regex below is support for that. """
#            print 'offsetStr', offsetStr
            offsetList = re.split(delimiter.encode('string-escape')+r'|\^', offsetStr)
            for offset in offsetList:
                if ':' in offset:
                    colonLoc = offset.find(':')
                    offsetTuple = (int(offset[0:colonLoc]), int(offset[colonLoc + 1:len(offset)]))
                    offsetIntList.append(offsetTuple)            
            return offsetIntList
        else:
            colonLoc = offsetStr.find(':')
            return [(int(offsetStr[0:colonLoc]), int(offsetStr[colonLoc + 1:len(offsetStr)]))]
