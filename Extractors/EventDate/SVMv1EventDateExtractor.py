#import sys,os
#sys.path.append('/Users/xqin/Workspace/Code/FDA-Textmining/')

import xml.etree.ElementTree as ET
import hashlib
import string
import re
import pickle
from sklearn import svm
from operator import itemgetter
from Extractors.Feature.FeatureExtractor import FeatureExtractor
from DataElements.EventDateElement import EventDateElement
from Preprocessing.Preprocessor import Preprocessor

class SVMv1EventDateExtractor(object):

    def __init__(self,rawTextFileName,intermediateXMLFileName):
        preprocessor = Preprocessor(rawTextFileName,intermediateXMLFileName)
        preprocessor.posTaggedText()
        preprocessor.getParseTree()
        preprocessor.getMetaMapConcepts()
        self.intermediate = intermediateXMLFileName
        self.vectors = []
    
    def clean(self):
        self.vectors = []
    
    def get_FeatureVector(self,intermediate):
        inter = ET.parse(intermediate)
        FE = FeatureExtractor()
        for paragraph in inter.getroot()[0]:
            for sentence in paragraph[0]:
                #print sentence.find("ParseTree").text
                if sentence.find("ParseTree").text is None: 
                    continue
                Tokens = sentence.find("Tokens")
                tokens = Tokens.findall("Token")
                token_vec = []
                #feature vector for metamap
                for token in tokens:
                    # MetaMap Feature Extraction is embedded here ...
                    #orch: Organic Chemical phsu: Pharmacologic substance sosy: sign or symptom dsyn: Disease or symptom
                    token_metamap = {'orch':0,'phsu':0,'sosy':0,'dsyn':0}
                    metamap_vector = []
                    if token.find("METAMAP") is not None: 
                        str = re.sub('[\[\]]','',token.find("METAMAP").text).split(',') 
                        for label in str:
                            token_metamap[label] = 1
                    
                    for key, value in token_metamap.iteritems():
                        metamap_vector.append(value)
                    
                    str = token.get("offset").split(":")
                    token_vec.append([token[0].text,str[0],str[1],metamap_vector])
                    #token_vec.append([token[0].text,str[0],str[1]])
                    
                tokens_pt = FE.get_PhrasalClass(sentence.find("ParseTree").text)
                pretoken = ['','','']
                
                offset = 0
                for token in tokens_pt:
                    vector = []
#                    print token[0],token_vec[offset][0],
                    tokeninfo = [token[0],token_vec[offset][1],token_vec[offset][2]]
                    
                    if pretoken[0] == '':
                        prevalue = -2
                    else:
                        prevalue = FE.GetPOSFeatureValue(pretoken[1])
                        # feature
                    vector.append(tokeninfo)
                    vector += token_vec[offset][3]
                    vector.append(FE.GetPOSFeatureValue(token[1]))
                    vector.append(FE.GetPhrasalClassFeatureValue(token[2]))
                    vector.append(prevalue)
                    vector.append(FE.ContainCapitalLetter(token[0]))
                    vector.append(FE.ContainDigit(token[0]))
                    vector.append(FE.IsPunctuation(token[0]))
                    vector.append(FE.IsStartWithLetterEndWithNumber(token[0]))
                    vector += FE.GetPrefixValue(3, token[0])
                    vector += FE.GetSufixValue(3, token[0])
                    vector += FE.GetREFeatures(token[0])
                    vector += FE.GetPrefixSufixValue(4,token[0])
                    vector += FE.GetPrefixSufixValue(4,token[0])
                    vector.append(FE.GetDigitCollapsesValue(token[0]))
                    vector.append(FE.GetWordClassValue(token[0]))
                    pretoken = token
                    offset += 1
                    self.vectors.append(vector)
        return self.vectors
   
    def findEntity(self):
        self.get_FeatureVector(self.intermediate)
        X = [f[1:] for f in self.vectors]
        
        with open('Resources/svm_eventdate.pkl', 'rb') as f:
        #with open('../../Resources/svm_eventdate.pkl', 'rb') as f:
            clf = pickle.load(f)
            
        predictions = clf.predict(X)     
        
        EventDates = []
        Offsets = []
        
        offset = 0
        #print len(predictions)
        for label in predictions:
            if label == 1:
                print self.vectors[offset][0]
                EventDates.append(self.vectors[offset][0][0])
                Offsets.append([self.vectors[offset][0][1],self.vectors[offset][0][2]])
            offset += 1


        drugNameElementList = []
        for x,y in DrugNames,Offsets:
            drugNameElementList.append(EventDateElement(x, y, "SVMv1EventDateExtractor", "EVENT_DT"))

        return drugNameElementList

#for filename in os.listdir("/Users/xqin/Workspace/Code/LearnPython/IntermediateFiles/"):
#    t = SVMv1EventDateExtractor("ac","/Users/xqin/Workspace/Code/LearnPython/IntermediateFiles/"+filename)
#    t.findEventDate()