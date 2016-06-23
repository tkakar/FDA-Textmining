import sys
from nltk_contrib.nltk_contrib import timex
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import MWETokenizer
from nltk import pos_tag

class Preprocessor(object):
    def __init__(self, rawTextFileName=None):
        if rawTextFileName is not None:
            self.filename = rawTextFileName
            #print file
        else:
            print "Need a text file!"

            
    def timexTagText(self):
        
        self.file = open(self.filename)
        raw = self.file.read()
        #print raw
        #tag all temporal expressions with timex2 tags
        tagged_raw = timex.tag(raw)
 
        self.file.close()

        return word_tagged

    def tokenizeText(self):
        self.file = open(self.filename)
        raw = self.file.read()
        word_tagged = word_tokenize(tagged_raw)
        
        self.file.close()

        return word_tagged


    def timexTagAndTokenizeText(self):
        self.file = open(self.filename)
        raw = self.file.read()

        #tag all temporal expressions with timex2 tags
        tagged_raw = timex.tag(raw)
        #print tagged_raw
        #word-tokenize all tags
        word_tagged = word_tokenize(tagged_raw)

        #consolidate all broken apart Timex2 tags into single "words"
        mweTokenizer = MWETokenizer(mwes=[('<','/TIMEX2','>'),('<','TIMEX2','>')], separator='')
        word_tagged = mweTokenizer.tokenize(word_tagged)

        self.file.close()
        
        return word_tagged

    def posTaggedText(self):
        self.file = open(self.filename)
        raw = self.file.read()
        
        word_tagged = word_tokenize(raw)

        pos_tagged = pos_tag(word_tagged)
        return pos_tagged
