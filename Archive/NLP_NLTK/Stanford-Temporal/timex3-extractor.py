# first course of action is to load the entire json file, replace all \\" with \" and then read into pandas

import pandas as p
import json
import re, pprint
import sys
import HashableElementTree as he


# import xml.etree.ElementTree as ET

def main():
    filename = sys.argv[1]
    raw = open(filename).read()

    raw = raw.strip()[1:-1].decode(
        'string-escape')  # lot happening here. first the raw text is strips of leading and trailing white space, then stripped of leading and trailing single quotes, and finally, all escape characters are corrected

    string_json = json.loads(raw)

    sentenceTimexTags = []

    for sentence in range(0, len(string_json['sentences'])):
        wordTimexTags = []
        for word in range(0, len(string_json['sentences'][sentence]['words'])):
            if 'Timex' in string_json['sentences'][sentence]['words'][word][1]:
                wordTimexTags.append(he.HashableElementTree(
                    he.fromstring(string_json['sentences'][sentence]['words'][word][1]['Timex'])))
        sentenceTimexTags.append(wordTimexTags)

        # print(type(sentenceTimexTags))

        # we now have all the XML elements from the parsed string in a 2D list

    #    for sentence in sentenceTimexTags:
    #       for XMLword in sentenceTimexTags[sentence]:
    words = []
    for wordTagSent in range(0, len(sentenceTimexTags)):
        otherWords = []
        for wordTag in range(0, len(sentenceTimexTags[wordTagSent])):
            otherWords.append(sentenceTimexTags[wordTagSent][wordTag].getroot().text)
        #            print('test type: ' + sentenceTimexTags[wordTagSent][wordTag].getroot().text)
        words.append(otherWords)

    # print(sentenceTimexTags)

    uniqueSentenceTimexes = [list(set(sublist)) for sublist in sentenceTimexTags]
    #    uniqueList = uniqueSentenceTimexes.pop()
    # print ('\r\n')
    #   print(uniqueList)

    words2 = []
    for wordTagSent in range(0, len(uniqueSentenceTimexes)):
        otherWords = []
        for wordTag in range(0, len(uniqueSentenceTimexes[wordTagSent])):
            otherWords.append(uniqueSentenceTimexes[wordTagSent][wordTag].getroot().text)
        #            print('test type: ' + sentenceTimexTags[wordTagSent][wordTag].getroot().text)
        words2.append(otherWords)

    print(words)
    print(words2)


len2 = lambda l: sum([len(x) for x in l])


def del_dups(elemList):
    seen = {}
    pos = 0
    for item in elemList:
        #        print item.getroot().text
        if item.getroot().text not in seen:
            seen[item] = True
            elemList[pos] = item
            pos += 1
    del elemList[pos:]


def unique(items):
    seen = set()
    for i in xrange(len(items) - 1, -1, -1):
        it = items[i]
        if it.getroot().text in seen:
            del items[i]
        else:
            seen.add(it)


if __name__ == '__main__':
    main()
