"""ProjectAERIS module

This is the main class for the entire system, for any particular narrative text file. This program will take in a text narrative, and output an XML file with tagged components, based on various customizatoins. The program takes three inputs:

python ProjectAERIS.py [raw text narrative] [output xml file location] [configuration file]

The first two are self-explanatory. The third is the configuration file, in JSON format in the form: 

{"Event Date" : ["AERecogExtractor", "SuspectRecogExtractor"],
 "Age" : ["AgeExtractor1", "AgeExtractor2"]}

Todo:
  +Cleanup the bottom of the file, make sure we don't need that code. 
"""


import sys, re
import nltk
sys.path.append('/work/tkakar/FDA-Textmining/')
nltk.data.path.append('/work/tkakar/nltk_data')
from nltk_contrib import timex
from Preprocessing.Preprocessor import Preprocessor
from Extractors.EventDate.AERecognitionEventDateExtractor import AERecogExtractor 
from Extractors.EventDate.SuspectRecognitionEventDateExtractor import SuspectRecogExtractor
from Assemblers.EventDateAssembler import EventDateAssembler
from Extractors.Dosage.DosageRegExtractor import DosageRegExtractor 
from Assemblers.DosageAssembler import DosageAssembler 
from Extractors.Age.AgeRegExtractor import AgeRegExtractor 
from Extractors.Age.AgeNltkExtractor import AgeNltkExtractor 
from Assemblers.AgeAssembler import AgeAssembler
from Extractors.Weight.WeightRegExtractor import WeightRegExtractor 
from Extractors.Weight.WeightNltkExtractor import WeightNltkExtractor 
from Assemblers.WeightAssembler import WeightAssembler
from Extractors.Gender.GenderRegExtractor import GenderRegExtractor 
from Assemblers.GenderAssembler import GenderAssembler


import json

def main():
    """Takes in the input three files, and creates a Preprocessor object, runs each extractor, and compiles the results."""
    assemblerList = []
    sysArgs = sys.argv[1:]
    if len(sysArgs) >= 3:
        """when calling ProjectAeris, it should be done with a raw text file and an output xml file location as the first and second arguments respectively"""
        preprocessOne = Preprocessor(rawTextFileName=sysArgs[0], outputXMLFileName=sysArgs[1])
        configFile = sysArgs[2]
        allAssemblerDict = {'Event Date':EventDateAssembler(), 'Dosage':DosageAssembler(), 'Age':AgeAssembler(), 'Weight':WeightAssembler(), 'Gender':GenderAssembler()}
        print 'done preprocess!'
    else:
        print "Need a file name!" 
        return

#Place to test new preprocess methods
#    preprocessOne.getMetaMapConcepts()
#    preprocessOne.posTaggedText()
    print preprocessOne.rawText()
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
    
