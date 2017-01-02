import xml.etree.ElementTree as ET
import string
import re
import nltk
from nltk import Tree
from DataElements.AgeElement import AgeElement
from DataElements.AgeCodeElement import AgeCodeElement
from Preprocessing.Preprocessor import Preprocessor


class AgeNltkExtractor(object):
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

        # this step will remove all false positives from the final tags except for true postives (age related tags)
        age_keyword_list = ["yrs", "years", "year", "yr", "yo"]

        extract_age_ageCode = ""
        age = ""
        ageCode = ""
        ageOffset = ""
        ageCodeOffset = ""

        for tags in final_tags:
            if any(word in tags for word in age_keyword_list):
                extract_age_ageCode = tags  # format: '71;50:52 year;53:57'
                break  # assuming that the demographics (age) of the patient is always at the beginning of the narrative

        if not extract_age_ageCode:
            age = "UNK"
            ageCode = "UNK"
        else:
            extract_age = extract_age_ageCode.split()[0]  # format: 71;50:52
            extract_ageCode = extract_age_ageCode.split()[1]  # format: year;53:57

            age = extract_age.split(';')[0]  # format: 71
            ageOffsetOrg = extract_age.split(';')[1]  # format: 50:52
            ageOffset = ageOffsetOrg.split(':')  # format: ['50', '52']
            ageOffset = map(int, ageOffset)  # format: [50, 52]

            # ageCode = extract_ageCode.split(';')[0]		#format: year
            ageCode = "YR"  # both intermediate/annotation files require the code = YR
            ageCodeOffsetOrg = extract_ageCode.split(';')[1]  # format: 53:57
            ageCodeOffset = ageCodeOffsetOrg.split(':')  # format: ['53', '57']
            ageCodeOffset = map(int, ageCodeOffset)  # format: [53, 57]

        print ("Nltk_age:", age, ageOffset)
        print ("Nltk_age_code:", ageCode, ageCodeOffset)

        if (age == "UNK" and ageCode == "UNK"):
            return True
        else:
            return [AgeElement(age, [ageOffset], "AgeNltkExtrator", "AGE"),
                    AgeCodeElement(ageCode, [ageCodeOffset], "AgeNltkExtrator", "AGE_COD")]
