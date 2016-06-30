import sys, re
from nltk_contrib.nltk_contrib import timex
from Preprocessor import Preprocessor
from AERecognitionEventDateExtractor import AERecogExtractor 
from SuspectRecognitionEventDateExtractor import SuspectRecogExtractor
import nltk
from nltk import data
nltk.data.path.append('/work/vsocrates/nltk_data')

def main():

    sysArgs = sys.argv[1:]
    if len(sysArgs) >= 2:
        preprocessOne = Preprocessor(rawTextFileName=sysArgs[0], outputXMLFileName=sysArgs[1])
        print 'done preprocess!'
    else:
        print "Need a file name!" 
        return

#    test = preprocessOne.parseText()
#    pattern = re.compile("\s?\n\s?")
#    print test
#    test2 = pattern.split(test)
    # test2 = [i for i in test if i is not '']
    # print test2
    # print test2[1]
    # tagged_text = preprocessOne.timexTagAndTokenizeText()
    #print test
    print 'done tagging!'
#    tagged_text2 = preprocessOne.timexTagAndTokenizeText()
#    recogEx = AERecogExtractor(tagged_text)
#    recogEx2 = SuspectRecogExtractor(tagged_text)

    posTagged = preprocessOne.posTaggedText()
    preprocessOne.getParseTree()
#    print posTagged

#    isFoundDate = recogEx.findDates()
#    isFoundDate2 = recogEx2.findDates()
    # if not isFoundDate:
    #     print "AE Extractor didn't find a date  :(" 
    #     return
    # if not isFoundDate2:
    #     print "Suspect Extractor didn't find a date :("
    #     return

    # print 'date found!'


if __name__ == "__main__":
    main()
