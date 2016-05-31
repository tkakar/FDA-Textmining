#-------------------------------------
# Test file takes extracted data fields
# and stores them directly in JSON 
# object.
#-------------------------------------

#-------------------------------------------------------------------------------
# Name:        Information extraction with Regular Expressions
# Purpose:      Textmining on FDA report narratives
#               Extract age, gender, height, weight and dates mentioned in the report
#
# Author:      susmitha wunnava
#              vimig socrates
#              amber wallace
#
# Created:     28/03/2016
# Copyright:   (c) susmi 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import json
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import sys

def main():
	f = open(sys.argv[1], 'r+')
	content = f.read()
	
	data = {
		"Patient Information":{
			"Patient Identifier":None,
			"Age":None,
			"Date of Birth":None,
			"Sex":None,
			"Weight":None,
			"Ethnicity":None,
			"Race":{
				"Asian":False,
				"American Indian or Alaskan Native":False,
				"Black or African American":False,
				"White":False,
				"Native Hawaiian or Other Pacific Islander":False
			}
		}
	}

	#AGE---------------------------------------------------------------------------
	extract_age = re.findall(r'.*\s([0-9]+).?(yr|yrs|years|year).*',content,re.IGNORECASE)
	if not extract_age:
		extract_age = re.findall(r'.*\s([0-9]+).?(months|months-old|months old|month-old|month old).*',content,re.IGNORECASE)
		if not extract_age:
			age="unknown"
		else:
			age = extract_age[0][0]+" months"
	else:
		age = extract_age[0][0]+" years"

	data["Patient Information"]["Age"] = age

	#WEIGHT----------------------------------------
	extract_weight = re.findall(r'.*\s([0-9]+(\.[0-9]+)?).?(pounds|pound|lb|lbs).*',content,re.IGNORECASE)
	if not extract_weight:
		weight="unknown"
	else:
		weight = extract_weight[0][0]+" pounds"

	data["Patient Information"]["Weight"] = weight

	#FORM DOES NOT ASK FOR HEIGHT-------------------------------------------

	#SEX--------------------------------------------------------------------
	extract_gender_m = []
	extract_gender_f = []
	extract_gender_m = re.findall(r'.(\bmale\b)',content,re.IGNORECASE)
	extract_gender_f = re.findall(r'.(\bfemale\b)',content,re.IGNORECASE)
	if not extract_gender_f:
		if not extract_gender_m:
			gender = "unknown"
		else:
			gender = extract_gender_m[0]
	else:
		gender = extract_gender_f[0]

	data["Patient Information"]["Sex"] = gender

	#RACE---------------------------------------------------------------------
	extract_white = re.findall(r'(white|caucasian)',content,re.IGNORECASE)
	if not extract_white:
		white = False
	else:
		white = True

	data["Patient Information"]["Race"]["White"] = white

   	#JSONEncoder().encode(data)
	result = json.dumps(data)
	print result

if __name__ == '__main__':
    main()
