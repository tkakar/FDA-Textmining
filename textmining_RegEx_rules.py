#-------------------------------------------------------------------------------
# Name:        Information extraction with Regular Expressions
# Purpose:      Textmining on FDA report narratives
#               Extract age, gender, height, weight and dates mentioned in the report
#
# Author:      susmitha wunnava
#
# Created:     28/03/2016
# Copyright:   (c) susmi 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import sys

def main():
    f = open(sys.argv[1], 'r+')
    content = f.read()
    #content = "This spontaneous report from a female patient concerns a 71 yr Caucasian female. The patient's weight was 160 pounds and height was 167.5 inches. In 15-AUG-2014, the patient contacted her physician about the events and was prescribed an increased dosage of domperidone.  The patient reported the increased dose of domperidone had not relieved her worsening symptoms. On 13-AUG-2014, the patient experienced not feeling well today."
    extract_age = re.findall(r'.*([0-9]{2}).?(yrs|years|year).*',content,re.IGNORECASE)
    if not extract_age:
        age="unknown"
    else:
        age = extract_age[0][0]+" years"

    extract_weight = re.findall(r'.*([0-9]{3}(\.[0-9]{1})?).?(pounds|pound|lb|lbs).*',content,re.IGNORECASE)
    ##    extract_weight = re.findall(r'.*\d{1,3}(\.\d)?.?(pounds|pound|lb|lbs).*',s,re.IGNORECASE)
    if not extract_weight:
        weight="unknown"
    else:
        weight = extract_weight[0][0]+" pounds"

    extract_height = re.findall(r'.*([0-9]{3}(\.[0-9]{1})?).?(feet|foot|inches|inch|"|cm).*',content,re.IGNORECASE)
    if not extract_height:
        height="unknown"
    else:
        height = extract_height[0][0]+" "+extract_height[0][2]

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

    extract_dates = []
    date_range = []
    dates = []
    other_dates = []
  
##  Example formats: 06-AUG-2014
    date_range  = re.findall(r'(from)\s([0-9]{2}[a-zA-Z]{3}[0-9]{4})\s(until)\s([0-9]{2}[a-zA-Z]{3}[0-9]{4})',content,re.IGNORECASE)
    extract_dates = re.findall(r'\s(on)\s([0-9]{2}\-?[a-zA-Z]{3}\-?[0-9]{4})', content,re.IGNORECASE)
 #   extract_dates = re.findall(r'.([0-9]{2}\-[a-zA-Z]{3}\-[0-9]{4})',content,re.IGNORECASE)
    if not date_range:
        dates="unknown"
        dateExistFlag = False;
    else:
#dates=', '.join(extract_dates)
        dates.append(date_range[0][1])
        dates.append(date_range[0][3])
        dateExistFlag = True;

    if not extract_dates:
        other_dates = "unknown"
        date2ExistFlag = False;
    else:
        date2ExistFlag = True;
        for x in range(0,len(extract_dates)): 
            other_dates.append(extract_dates[x][1])
#        print(extract_dates)

    print("Age: " + age)
    print("Gender: " + gender)
    print("Weight: " + weight)
    print("Height: "+  height)
    if date2ExistFlag:
        print("Other Dates: " + ', '.join(other_dates))
    else:
        print("Other Dates: unknown")

    if dateExistFlag:
        print("Report between " + dates[0] + " and " + dates[1])
    else:
        print("Report Range Unknown")

if __name__ == '__main__':
    main()
