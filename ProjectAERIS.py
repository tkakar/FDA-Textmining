import sys
from Preprocessor import Preprocessor
from AERecognitionEventDateExtractor import AERecogExtractor 
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
    
    isFoundDate = recogEx.findDates()
    if not isFoundDate:
        print "Didn't find a date :(" 
        return 

    print 'date found!'


if __name__ == "__main__":
    main()
