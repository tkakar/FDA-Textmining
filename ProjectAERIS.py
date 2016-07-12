import sys, re
import nltk
sys.path.append('/home/vsocrates/My_Documents/fda_textmining/FDA-Textmining/')
nltk.data.path.append('/work/vsocrates/nltk_data')
from nltk_contrib import timex
from Preprocessing.Preprocessor import Preprocessor
from Extractors.EventDate.AERecognitionEventDateExtractor import AERecogExtractor 
from Extractors.EventDate.SuspectRecognitionEventDateExtractor import SuspectRecogExtractor
from Assemblers.EventDateAssembler import EventDateAssembler

import json

def main():
    assemblerList = []
    sysArgs = sys.argv[1:]
    if len(sysArgs) >= 3:
        """when calling ProjectAeris, it should be done with a raw text file and an output xml file location as the first and second arguments respectively"""
        preprocessOne = Preprocessor(rawTextFileName=sysArgs[0], outputXMLFileName=sysArgs[1])
        configFile = sysArgs[2]
        allAssemblerDict = {'Event Date':EventDateAssembler()} # , 'Age':AgeAssembler()}
        print 'done preprocess!'
    else:
        print "Need a file name!" 
        return

#Place to test new preprocess methods
#    preprocessOne.getMetaMapConcepts()
#    preprocessOne.posTaggedText()
#Place to test new preprocess methods


    config = json.load(open(configFile))
    entities = config.keys()

    for entity in entities:
        if entity not in allAssemblerDict:
            raise KeyError("An entity you entered doesn't exist")
        else:
            assemblerList.append((entity,allAssemblerDict[entity]))
    
    for name, assembler in assemblerList:
        if config[name]:
            assembler.setExtractorList(config[name])
            assembler.runExtractors() 

# #Currently (as of 7-5-16), only the two following methods work. The other ones still need to be updated and integrated into the XML document
#     output = preprocessOne.wordTokenizeText()
#     posTagged = preprocessOne.posTaggedText()
#     parseTree = preprocessOne.getParseTree()
#     print 'preprocess1:' , preprocessOne.__dict__

# #    borgTestPreprocess = Preprocessor(rawTextFileName=sysArgs[0], outputXMLFileName=sysArgs[1])
#     borgTestPreprocess = Preprocessor()
    
#     print 'preprocess2:' , borgTestPreprocess.__dict__

# You can see the individual outputs, or just open the XML file that was just created!!!!    
#    print posTagged
#    print parseTree.dump()

if __name__ == "__main__":
    main()
    
