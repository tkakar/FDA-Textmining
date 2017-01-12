import re
import nltk
import nltk_contrib
import itertools
from itertools import product
from DataElements.EventDateElement import EventDateElement
from DataElements.DataElement import DataElement
from Preprocessing.Preprocessor import Preprocessor
import sys


class AERecognitionEventDateExtractor(object):
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        self.preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.tokens = self.preprocess.timexTagAndTokenizeText()

    #        print self.tokens
    def findEntity(self):
        #        print self.tokens
        # search for words (e.g. 'AE(s)' or 'Adverse Event(s)')
        pattern = r'\bAE(\s|s)'
        pattern2 = r'\bevents?\b'
        pattern3 = r'<\/?TIMEX2>'
        re_pat = re.compile(pattern, re.IGNORECASE)
        re_pat2 = re.compile(pattern2, re.IGNORECASE)
        re_pat3 = re.compile(pattern3, re.IGNORECASE)

        ae_index_list = []

        # Go through and check for all adverse event/AE keyworks
        for index in range(0, len(self.tokens)):
            if (self.tokens[index].lower() == 'Adverse'.lower() and
                    re_pat2.search(self.tokens[index + 1])) or (re_pat.search(self.tokens[index])):
                ae_index_list.append(index)

        if ae_index_list == []:
            print "There are no instances of keyword 'adverse event/AE'"
            return False

            # Get the indices for all the found tagged words
        time_index_list = [index for index in range(0, len(self.tokens)) if re_pat3.search(self.tokens[index])]

        if time_index_list == []:
            print "There are no temporal expressions in the text."
            return False
        # Minimize difference between indices for AE keywork  and dates
        diff = min(product(ae_index_list, time_index_list), key=lambda t: abs(t[0] - t[1]))

        if re_pat3.search(self.tokens[diff[0]]):
            timexTuple = (diff[0], self.tokens[diff[0]])
            aeTuple = (diff[1], self.tokens[diff[1]])
        else:
            timexTuple = (diff[1], self.tokens[diff[1]])
            aeTuple = (diff[0], self.tokens[diff[0]])

        # Figure out of timex tuple is <TIMEX2> or </TIMEX2> and act accordingly
        if timexTuple[1].lower() == '<TIMEX2>'.lower():
            date = list(
                itertools.takewhile(lambda x: x.lower() != '</TIMEX2>'.lower(), self.tokens[timexTuple[0] + 1:]))
        else:
            reversedList = self.tokens[::-1]

            date = list(itertools.takewhile(lambda x: x.lower() != '<TIMEX2>'.lower(),
                                            reversedList[(len(self.tokens) - timexTuple[0]):]))
            date = date[::-1]

        count = 0

        # the rest is to find the offset
        for idx, token in enumerate(self.tokens):
            if idx > timexTuple[0]: break
            if token.lower() == '<TIMEX2>'.lower() or token.lower() == '</TIMEX2>'.lower():
                count += 1

        # add one because tokens index starts at 0
        loc = timexTuple[0] + 1 - count
        print "this is the timexTuple: ", timexTuple[0]
        print "this is the loc: ", loc

        root = self.preprocess.getRoot()
        offsets = []
        for x in range(0, len(date)):
            elem = root.find(".//*[@globalID='" + str(loc + x) + r"']")
            if elem is not None:
                offsets.append(elem.attrib['offset'])

        print 'AERecognitionEventDateExtractor: ', " ".join(date)

        offsetList = self.preprocess.offsetParse(";".join(offsets), delimiter=";")

        print " ".join(date), offsetList
        # 
        if not offsetList:
            return EventDateElement(" ".join(date), [[]], "AERecognitionEventDateExtractor", 'EVENT_DT')
        else:
            return EventDateElement(" ".join(date), offsetList, "AERecognitionEventDateExtractor", 'EVENT_DT')
