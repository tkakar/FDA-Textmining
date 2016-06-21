from nltk_contrib import timex
import re
import nltk

class NaiveExtractor(EventDateExtractor):

    def main():
        raw = open('../test_cases/fda008.txt').read()
    
        tagged_raw = timex.tag(raw)
        print(tagged_raw)

        print '\n\n\n\n\n\n'
    
        s = re.search(r'(<TIMEX2>)(.*?)(</TIMEX2>)', tagged_raw)
    #    print(tagged_raw[s.start():s.end()])
        print('Event date: {}'.format(s.group(2)))
        #    print(s.group(1))
        #    print(s.group(2))


        raw = "<TIMEX2>16-Apr-2015</TIMEX2> asdfafasdfasdfas 2343"
        tagged2 = timex.tag(raw)
    #    print(tagged2)

