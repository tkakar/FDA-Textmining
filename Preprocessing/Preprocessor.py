"""Preprocessor Class

This module contains all of the methods to preprocess the data and pass them to the extractors. This may include tokenization, POS tagging, or tagging a specific concept with preliminary tags (temporal)

IMPORTANT:
When creating new methods, make sure to check the dictionary (textList) to see if the particular format of a test case that you want already exists before creating it. If it doesn't exist, create it and place it into textList with the key being the name of the method you write. This will help in minimizing File I/O and standardize the dictionary so people can find other versions of narratives. 

Todo:
    * Fix dictionary (textList)  key phrase, so it doesn't have to rely on programmer accuracy

"""

import sys
from nltk_contrib.nltk_contrib import timex
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import MWETokenizer
from nltk import pos_tag

class Preprocessor(object):
    def __init__(self, rawTextFileName=None):
        if rawTextFileName is not None:
            self.filename = rawTextFileName
            self.textList = {}
            #print file
        else:
            print "Need a text file!"


#TODO optimize preprocessor so it saves already created formats            
    def timexTagText(self, altText=None):
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
        if altText is not None:
            raw = altText
            altOutput = word_tokenize(raw)
            return altOutput

        else:
            self.file = open(self.filename)
            raw = self.file.read()
            if self.textList.get('wordTokenizeText') is None:
                self.textList['wordTokenizeText'] = word_tokenize(raw)

            self.file.close()

        return self.textList.get('wordTokenizeText')


    def timexTagAndTokenizeText(self, altText=None):
        """In this method, two steps are required, so if altText is specified, all steps are done inside the if statement, so incorrect dict entries aren't stored"""
        if altText is not None:
            raw = altText
            altOutputStep1 = self.timexTagText(raw)
            altOutputStep2 = self.wordTokenizeText(altOutputStep1)
            return altOutputStep2
        else:
            """Tag all temporal expressions with timex2 tags."""          
            """Don't need to open file here, because it's opened in timexTagText()"""
            tagged = self.timexTagText()
            """Word-tokenize all text above"""
            word_tagged = self.wordTokenizeText(tagged)
            
        '''consolidate all broken apart Timex2 tags into single "words"'''
        if self.textList.get('timexTagAndTokenizeText') is None:
            self.textList['timexTagAndTokenizeText'] = MWETokenizer(mwes=[('<','/TIMEX2','>'),('<','TIMEX2','>')], separator='').tokenize(word_tagged)

        return self.textList.get('timexAndTokenizedText')


    def posTaggedText(self, altText=None):
        if altText is not None:
            raw = altText
            altOutputStep1 = self.wordTokenizeText(raw)
            altOutputStep2 = pos_tag(altOutputStep1)
            return altOutputStep2
        else:
            self.file = open(self.filename)
            raw = self.file.read()
        
            word_tagged = self.wordTokenizeText(raw)
            
            pos_tagged = pos_tag(word_tagged)
            self.file.close()
        
        return pos_tagged

    def existsInFileList(self, key, value=None):
        if key in self.textList:
            return self.textList.get(key)
        else:
            self.textList[key] = value
            return value
