# -------------------------------------------------------------------------------
# Name:        Information extraction with NLTK Part-Of-Speech Tagging
# Purpose:      Textmining on FDA report narratives.
#               Extract age, height, weight and dates mentioned in the report
#
# Author:      susmitha wunnava
#
# Created:     28/03/2016
# Copyright:   (c) susmi 2016
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

content = "This spontaneous report from a female patient concerns a 71-year-old Caucasian female. The patient's weight was 160 pounds and height was 167.5 inches. In 15-AUG-2014, the patient contacted her physician about the events and was prescribed an increased dosage of domperidone.  The patient reported the increased dose of domperidone had not relieved her worsening symptoms. On 13-AUG-2014, the patient experienced not feeling well today."

sentences = sent_tokenize(content)

filtered_sentences = []
for s in sentences:
    s = re.sub('-', ' ', s)  ## Replace "-" with " " in the sentences, especially useful for extracting age
    filtered_sentences.append(s)

## Word Tokenization
tokenized = [word_tokenize(s) for s in filtered_sentences]

final_tags = []
year = []

for i in tokenized:

    # words = nltk.word_tokenize(i)
    tagged = nltk.pos_tag(i)

    ##Assumption: Various input formats considered for age:71 year old, 39 years old, 50-year-old, 7 years, 1 year, 3-years
    chunkGram = r"""numberChunks: {<CD><NN.?><JJ>?<CD>?}"""
    chunkParser = nltk.RegexpParser(chunkGram)
    chunked = chunkParser.parse(tagged)
    ##            print("chunked:")
    ##            print(chunked)
    ##            chunked.draw()

    for n in chunked:
        if isinstance(n, nltk.tree.Tree):
            if n.label() == 'numberChunks':
                if len(n) == 3:
                    if n[2][1] == 'CD':
                        tag = n[0][0] + " " + n[1][0] + " " + n[2][0]
                        year.append(tag)
                    else:
                        tag = n[0][0] + " " + n[1][0]
                else:
                    tag = n[0][0] + " " + n[1][0]
                final_tags.append(tag)
##                else:
##                    print(2)

##        print(final_tags)

age = 'unknown'
weight = 'unknown'
height = 'unknown'

age_keyword_list = ["yrs", "years", "year"]
weight_keyword_list = ["pounds", "pound", "lb", "lbs"]
height_keyword_list = ["feet", "foot", "inches", "inch", "\"", "cm"]

for tags in final_tags:
    if any(word in tags for word in age_keyword_list):
        age = tags
    if any(word in tags for word in weight_keyword_list):
        weight = tags
    if any(word in tags for word in height_keyword_list):
        height = tags

if not year:
    dates = "Unknown"
else:
    dates = ', '.join(year)

print(age)
print(weight)
print(height)
print(dates)
