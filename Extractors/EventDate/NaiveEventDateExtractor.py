from nltk_contrib import timex
import re
import nltk
from Preprocessing.Preprocessor import Preprocessor
from DataElements.EventDateElement import EventDateElement


class NaiveEventDateExtractor(object):
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.text = self.preprocess.timexTagText()

    def findEntity(self):
        s = re.search(r'(<TIMEX2>)(.*?)(</TIMEX2>)', self.text)
        #    print(tagged_raw[s.start():s.end()])
        if s:
            print('Event date: {}'.format(s.group(2)))
            return EventDateElement(s.group(2), [[s.start(2), s.end(2)]], "NaiveEventDateExtractory", "EVENT_DT")
