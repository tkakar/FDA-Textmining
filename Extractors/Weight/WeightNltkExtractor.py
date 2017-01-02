import xml.etree.ElementTree as ET
import string
import re
import nltk
from nltk import Tree
from DataElements.WeightElement import WeightElement
from DataElements.WeightCodeElement import WeightCodeElement
from Preprocessing.Preprocessor import Preprocessor


class WeightNltkExtractor(object):
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocessor = Preprocessor(rawTextFileName, intermediateXMLFileName)
        preprocessor.posTaggedText()
        preprocessor.getParseTree()
        # preprocessor.getMetaMapConcepts()
        self.intermediate = intermediateXMLFileName

    def findEntity(self):
        tree = ET.parse(self.intermediate)
        final_tags = []

        for paragraph in tree.getroot()[0]:
            for sentence in paragraph[0]:
                Tokens = sentence.find("Tokens")
                tokens = Tokens.findall("Token")

                postags = []
                for index, token in enumerate(tokens):
                    postags.append(
                        (str(token[0].text) + ";" + str(tokens[index].get('offset')), tokens[index].get('POSTag')))
                    # print(sentence[0].text)			#testing
                    # print(postags)				#testing

                chunkGram = r"""numberChunks: {<CD><NN.?><JJ>?}"""
                chunkParser = nltk.RegexpParser(chunkGram)
                chunked = chunkParser.parse(postags)
                # print(chunked)				#testing

                for n in chunked:
                    if isinstance(n, nltk.tree.Tree):
                        if n.label() == 'numberChunks':
                            # print("n:"+str(n))	#testing
                            tag = n[0][0] + " " + n[1][0]
                            final_tags.append(tag)

                            # print(final_tags)						#testing

        # this step will remove all false positives from the final tags except for true postives (weight related tags)
        weight_keyword_list = ["pounds", "pound", "lb", "lbs", "kg", "kgs", "kilograms", "kilogram"]
        weight_keyword_list_LBS = ["pounds", "pound", "lb", "lbs"]
        weight_keyword_list_KG = ["kg", "kgs", "kilograms", "kilogram"]

        extract_weight_weightCode = ""
        weight = ""
        weightCode = ""
        weightOffset = ""
        weightCodeOffset = ""

        for tags in final_tags:
            if any(word in tags for word in weight_keyword_list):
                extract_weight_weightCode = tags  # format: '71;50:52 year;53:57'

        if not extract_weight_weightCode:
            weight = "UNK"
            weightCode = "UNK"
        else:
            extract_weight = extract_weight_weightCode.split()[0]  # format: 71;50:52
            extract_weightCode = extract_weight_weightCode.split()[1]  # format: year;53:57

            weight = extract_weight.split(';')[0]  # format: 71
            weightOffsetOrg = extract_weight.split(';')[1]  # format: 50:52
            weightOffset = weightOffsetOrg.split(':')  # format: ['50', '52']
            weightOffset = map(int, weightOffset)  # format: [50, 52]

            weightCode = extract_weightCode.split(';')[0]  # format: year
            if any(word in weightCode for word in weight_keyword_list_LBS):
                weightCode = "LBS"  # both intermediate/annotation files require the code = LBS
            if any(word in weightCode for word in weight_keyword_list_KG):
                weightCode = "KG"  # both intermediate/annotation files require the code = KG
            weightCodeOffsetOrg = extract_weightCode.split(';')[1]  # format: 53:57
            weightCodeOffset = weightCodeOffsetOrg.split(':')  # format: ['53', '57']
            weightCodeOffset = map(int, weightCodeOffset)  # format: [53, 57]

        print ("Nltk_weight:", weight, weightOffset)
        print ("Nltk_weight_code:", weightCode, weightCodeOffset)

        if (weight == "UNK" and weightCode == "UNK"):
            return False
        else:
            return [WeightElement(weight, [weightOffset], "WeightNltkExtrator", "AGE"),
                    WeightCodeElement(weightCode, [weightCodeOffset], "WeightNltkExtrator", "AGE_COD")]
