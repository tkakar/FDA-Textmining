"""ProjectAERIS module

This is the main class for the entire system, for any particular narrative text file. This program will take in a text narrative, and output an XML file with tagged components, based on various customizatoins. The program takes three inputs:

python ProjectAERIS.py [raw text narrative] [output xml file location] [configuration file]

The first two are self-explanatory. The third is the configuration file, in JSON format in the form: 

{"Event Date" : ["AERecogExtractor", "SuspectRecogExtractor"],
 "Age" : ["AgeExtractor1", "AgeExtractor2"]}

Todo:
  +Cleanup the bottom of the file, make sure we don't need that code. 
"""
import sys
# import nltk
# sys.path.append('/work/tkakar/FDA-Textmining/')
# nltk.data.path.append('/Users/wutianyu/nltk_data')
# sys.path.append('ISP2016/')
# #nltk.data.path.append('/work/vsocrates/nltk_data')
# from nltk_contrib import timex
# from Preprocessing.Preprocessor import Preprocessor
# from Extractors.EventDate.AERecognitionEventDateExtractor import AERecognitionEventDateExtractor
# from Extractors.EventDate.SuspectRecognitionEventDateExtractor import SuspectRecognitionEventDateExtractor
# from Assemblers import EntityAssembler
from Assemblers.EventDateAssembler import EventDateAssembler
# from Extractors.Dosage.DosageRegExtractor import DosageRegExtractor
from Assemblers.DosageAssembler import DosageAssembler
# from Extractors.Age.AgeRegExtractor import AgeRegExtractor
# from Extractors.Age.AgeNltkExtractor import AgeNltkExtractor
from Assemblers.AgeAssembler import AgeAssembler
# from Extractors.Weight.WeightRegExtractor import WeightRegExtractor
# from Extractors.Weight.WeightNltkExtractor import WeightNltkExtractor
# from Extractors.Gender.GenderRegExtractor import GenderRegExtractor
from Assemblers.GenderAssembler import GenderAssembler
# from Extractors.Drugname.DrugnameMetamapExtractor import DrugnameMetamapExtractor
# from Extractors.Drugname.DrugnameRegExtractor import DrugnameRegExtractor
from Assemblers.DrugnameAssembler import DrugnameAssembler
from Assemblers.WeightAssembler import WeightAssembler
from Assemblers.ReactionAssembler import ReactionAssembler

import json


# reload(sys)
# sys.setdefaultencoding('utf-8')

def main(aRawTextFileName=None, aIntermediateXMLFileName=None, aConfigFile=None):
    assemblerList = []
    if aRawTextFileName is None and aIntermediateXMLFileName is None:

        sysArgs = sys.argv[1:]
        if len(sysArgs) >= 3:
            """when calling ProjectAeris, it should be done with a raw text file and an output xml file location as the first and second arguments respectively"""

            rawTextFileName = sysArgs[0]
            intermediateXMLFileName = sysArgs[1]
            configFileName = sysArgs[2]

        else:
            print "Missing some command-line arguments"
            return

    else:
        rawTextFileName = aRawTextFileName
        intermediateXMLFileName = aIntermediateXMLFileName
        configFileName = aConfigFile

    print 'initial preprocess done!'

    # preprocessOne = Preprocessor(rawTextFileName=rawTextFileName,intermediateXMLFileName=intermediateXMLFileName)
    configFile = configFileName

    allAssemblerDict = {'Event Date': EventDateAssembler(rawTextFileName, intermediateXMLFileName),
                        'Age': AgeAssembler(rawTextFileName, intermediateXMLFileName),
                        'Dosage': DosageAssembler(rawTextFileName, intermediateXMLFileName),
                        'Drugname': DrugnameAssembler(rawTextFileName, intermediateXMLFileName),
                        'Weight': WeightAssembler(rawTextFileName, intermediateXMLFileName),
                        'Gender': GenderAssembler(rawTextFileName, intermediateXMLFileName),
                        'Reaction': ReactionAssembler(rawTextFileName, intermediateXMLFileName)}

    # Place to test new preprocess methods
    #    preprocessOne.getMetaMapConcepts()
    #    preprocessOne.posTaggedText()
    #    preprocessOne.getParseTree()
    #    print preprocessOne.rawText()
    # Place to test new preprocess methods


    # The following is to actually run the extractors

    config = json.load(open(configFile))
    entities = config.keys()

    for entity in entities:
        if entity not in allAssemblerDict:
            raise KeyError("An entity you entered doesn't exist")
        else:
            assemblerList.append((entity, allAssemblerDict[entity]))

    for name, assembler in assemblerList:
        if config[name]:
            assembler.setExtractorList(config[name])
            assembler.runExtractors()
            assembler.writeToSemiFinalXML()
            # assembler.launchTestSuite()


# #Currently (as of 7-5-16), only the two following methods work. The other ones still need to be updated and integrated into the XML document
#     output = preprocessOne.wordTokenizeText()
#     posTagged = preprocessOne.posTaggedText()
#     parseTree = preprocessOne.getParseTree()
#     print 'preprocess1:' , preprocessOne.__dict__
#
#     borgTestPreprocess = Preprocessor(rawTextFileName=sysArgs[0], outputXMLFileName=sysArgs[1])
#     borgTestPreprocess = Preprocessor()
#
#     print 'preprocess2:' , borgTestPreprocess.__dict__
#
# You can see the individual outputs, or just open the XML file that was just created!!!!
#    print posTagged
#    print parseTree.dump()

if __name__ == "__main__":
    main()
