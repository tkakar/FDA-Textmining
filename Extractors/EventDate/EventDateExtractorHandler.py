import re
import nltk
from nltk import word_tokenize, sent_tokenize, data
from nltk_contrib import timex 
from AERecognitionEventDateExtractor import AERecogExtractor
import sys
sys.path.append('/home/vsocrates/My_Documents/fda_textmining/FDA-Textmining/')
import ExtractorHandler

class EventDateExtractorHandler(ExtractorHandler):
    
    def __init__(self, filename):
        nltk.data.path.append('/work/vsocrates/nltk_data/')
        self.ExtractorList = []
        self.filename = filename

    def getExtractorList(self):
        return self.ExtractorList

    def initialTagFile():
        raw = open(filename).read()       

        #tag all temporal expressions with timex2 tags
        tagged_raw = timex.tag(raw)
        
        #word-tokenize all tags
        word_tagged = word_tokenize(tagged_raw)
        #consolidate all broken apart Timex2 tags into single "words"
        mweTokenizer = MWETokenizer(mwes=[('<','/TIMEX2','>'),('<','TIMEX2','>')], separator='')
        word_tagged = mweTokenizer.tokenize(word_tagged)

        close(filename)

        return word_tagged
    
    def useAEExtractor(tokens):
        extractor = AERecogExtractor(tokens)
        extractor.findDates()
        
        
def main():
    extractorHandler = EventDateExtractorHandler('../test_cases/fda001.txt')
    
