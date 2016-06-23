import sys
from nltk_contrib.nltk_contrib import timex
from Preprocessor import Preprocessor
from AERecognitionEventDateExtractor import AERecogExtractor 
from SuspectRecognitionEventDateExtractor import SuspectRecogExtractor
import nltk
from nltk import data
nltk.data.path.append('/work/vsocrates/nltk_data')

def main():

    sysArgs = sys.argv[1:]
    if len(sysArgs) >= 1:
        preprocessOne = Preprocessor(rawTextFileName=sysArgs[0])
        print 'done preprocess!'
    else:
        print "Need a file name!" 
        return

    tagged_text = preprocessOne.timexTagAndTokenizeText()
    print 'done tagging!'
    recogEx = AERecogExtractor(tagged_text)
    recogEx2 = SuspectRecogExtractor(tagged_text)

    posTagged = preprocessOne.posTaggedText()
    print posTagged

    isFoundDate = recogEx.findDates()
    isFoundDate2 = recogEx2.findDates()
    if not isFoundDate:
        print "AE Extractor didn't find a date  :(" 
        return
    if not isFoundDate2:
        print "Suspect Extractor didn't find a date :("
        return

    print 'date found!'


if __name__ == "__main__":
    main()
