# -------------------------------------------------------------------------------
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
# -------------------------------------------------------------------------------
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import sys


def main():
    f = open(sys.argv[1], 'r+')
    content = f.read()

    ##All of the below forms must have spaces before and after (or could be the end of sentence- period after) the complete date form!!

    # of forms: 01-03-2016, 01/03/2016, 1-03-2016, 1/03/2016, 1-3/2016
    dateRegex1 = r'\b([0-9]{1,2}[\/-][0-9]{1,2}[-\/][0-9]{4})\b'
    # of forms: 01-Mar-2016, 01/Mar/2016, 1-Mar-2016, 1/Mar/2016, 01Mar2016, 1Mar2016, 1-Mar/2016
    dateRegex2 = r'\b([0-9]{1,2}[\/-]?[a-zA-Z]{3}[-\/]?[0-9]{4})\b'

    # of forms: 01-03-16, 01/03/16, 1-03-16, 1/03/16, 1-3/2016
    dateRegex3 = r'\b([0-9]{1,2}[\/-][0-9]{1,2}[-\/][0-9]{2})\b'
    # of forms: 01-Mar-16, 01/Mar/16, 1-Mar-16, 1/Mar/16, 01Mar16, 1Mar16, 1-Mar/16
    dateRegex4 = r'\b([0-9]{1,2}[\/-]?[a-zA-Z]{3}[-\/]?[0-9]{2})\b'
    # of forms: 3/14, 3-14
    dateRegex5 = r'\b([0-9]{1,2}[\/-][0-9]{1,2})\b'

    # of forms: March-15, March/15, March 15, March15
    dateRegex6 = r'\b([a-zA-z]{4,9}[-\/\s]?[0-9]{1,2})\b'
    # of forms: 14-Mar , 14/Mar , 14 Mar , 14Mar
    dateRegex7 = r'\b([0-9]{1,2}[-\/\s]?[a-zA-z]{3})\b'
    # of forms: Mar-14, Mar/14, Mar 14, Mar14
    dateRegex8 = r'\b([a-zA-z]{3}[-\/\s]?[0-9]{1,2})\b'
    # of forms: March 14, 2014
    dateRegex9 = r'\b([a-zA-z]{4,9}\s[0-9]{1,2}\,\s[0-9]{4})\b'

    dateRegList = [dateRegex1, dateRegex2, dateRegex3, dateRegex4, dateRegex5, dateRegex6, dateRegex7, dateRegex8,
                   dateRegex9]

    # content = "This spontaneous report from a female patient concerns a 18 year old Caucasian female with a 18 month old child. The patient's weight 98.6lbs and the patient had a height of  5' 3\". In 15-AUG-2014, the patient contacted her physician about the events and was prescribed an increased dosage of domperidone.  The patient reported the increased dose of domperidone had not relieved her worsening symptoms. On 13-AUG-2014, the patient experienced not feeling well"
    extract_age = re.findall(r'.*\s([0-9]+).?(yr|yrs|years|year).*', content, re.IGNORECASE)
    if not extract_age:
        extract_age = re.findall(r'.*\s([0-9]+).?(months|months-old|months old|month-old|month old).*', content,
                                 re.IGNORECASE)
        if not extract_age:
            age = "unknown"
        else:
            age = extract_age[0][0] + " months"
    else:
        age = extract_age[0][0] + " years"

    extract_weight = re.findall(r'.*\s([0-9]+(\.[0-9]+)?).?(pounds|pound|lb|lbs).*', content, re.IGNORECASE)
    ##    extract_weight = re.findall(r'.*\d{1,3}(\.\d)?.?(pounds|pound|lb|lbs).*',s,re.IGNORECASE)
    if not extract_weight:
        weight = "unknown"
    else:
        weight = extract_weight[0][0] + " pounds"

    extract_height = re.findall(r'\s([0-9\']+(\.[0-9]+)?).?(feet|foot|ft|in|inches|inch|"|cm|meters|meter|m |\')',
                                content, re.IGNORECASE)
    cm = re.findall(r'.*\s([0-9]+(\.[0-9]+)?).?(cm|centimeter)', content, re.IGNORECASE)
    ##curent issue:m needs space after it and 72cm needs space before it, which causes overlap in whitespace so cm is not recognized
    if not extract_height:
        height = "unknown"
    else:
        height = extract_height[0][0] + " " + extract_height[0][2]
        if len(extract_height) > 1:
            height += " " + extract_height[1][0] + " " + extract_height[1][2]
        elif cm:
            height += " " + cm[0][0] + " cm"

    extract_gender_m = []
    extract_gender_f = []
    extract_gender_m = re.findall(r'.(\bmale\b)', content, re.IGNORECASE)
    extract_gender_f = re.findall(r'.(\bfemale\b)', content, re.IGNORECASE)
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
    dateRangeTmp = []
    otherDateTmp = []

    # checks through all possible regexes for Dates given at beginning of file
    for i in range(0, len(dateRegList)):

        dateRangeTmp = re.findall(
            r'\b(from)\s{start_date}\s(until|through|to)\s{end_date}'.format(start_date=dateRegList[i],
                                                                             end_date=dateRegList[i]), content,
            re.IGNORECASE)
        otherDateTmp = re.findall(r'\b(on)\s{date}'.format(date=dateRegList[i]), content, re.IGNORECASE)

        if dateRangeTmp:
            date_range += dateRangeTmp
        if otherDateTmp:
            extract_dates += otherDateTmp

    print(extract_dates)
    # report date range, if exists
    if not date_range:
        dateRangeFlag = False
    else:
        dates = date_range
        dateRangeFlag = True
    # pulls all other dates, if exist
    if not extract_dates:
        date2ExistFlag = False;
    else:
        date2ExistFlag = True;
        for x in range(0, len(extract_dates)):
            other_dates.append(extract_dates[x][1])

            # prints everything
    print("Age: " + age)
    print("Gender: " + gender)
    print("Weight: " + weight)
    print("Height: " + height)

    if date2ExistFlag:
        print("Other Dates: " + ', '.join(other_dates))
    else:
        print("Other Dates: unknown")

    if dateRangeFlag:
        print("Report between " + dates[0][1] + " and " + dates[0][3])
    else:
        print("Report Range Unknown")


if __name__ == '__main__':
    main()
