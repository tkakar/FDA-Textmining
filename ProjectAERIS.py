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
        """when calling ProjectAeris, it should be done with a raw text file and an output xml file location as the first and second arguments respectively"""
        preprocessOne = Preprocessor(rawTextFileName=sysArgs[0], outputXMLFileName=sysArgs[1])
        print 'done preprocess!'
    else:
        print "Need a file name!" 
        return

#Currently (as of 7-5-16), only the two following methods work. The other ones still need to be updated and integrated into the XML document
 
    posTagged = preprocessOne.posTaggedText()
    parseTree = preprocessOne.getParseTree()

# You can see the individual outputs, or just open the XML file that was just created!!!!    
#    print posTagged
#    print parseTree.dump()

if __name__ == "__main__":
    main()
