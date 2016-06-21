class SuspectRecogExtractor(object):
    
    def __init__(self, time_tagged_tokenizedText):
        self.tokens = time_tagged_tokenizedText



    def findDates(self):

        #search for words (e.g. 'AE(s)' or 'Adverse Event(s)')
        pattern = r'\bAE(\s|s)'
        pattern2 = r'\bevents?\b'
        pattern3 = r'<\/?TIMEX2>'
        re_pat = re.compile(pattern, re.IGNORECASE)
        re_pat2 = re.compile(pattern2, re.IGNORECASE)
        re_pat3 = re.compile(pattern3, re.IGNORECASE)

        ae_index_list = []

        #Go through and check for all adverse event/AE keyworks
        for index in range (0, len(self.tokens)):
            if (self.tokens[index].lower() == 'Adverse'.lower() and 
                re_pat2.search(self.tokens[index + 1])) or (re_pat.search(self.tokens[index])):

                ae_index_list.append(index)
                
        if ae_index_list == []:
            print "There are no instances of keyword 'adverse event'"
            return False
        #Get the indices for all the found tagged words
        time_index_list = [index for index in range(0,len(self.tokens)) if re_pat3.search(self.tokens[index])]
        
        #Minimize difference between indices for AE keywork  and dates
        diff = min(product(ae_index_list, time_index_list), key = lambda t: abs(t[0] - t[1]))

        if re_pat3.search(self.tokens[diff[0]]):
            timexTuple = (diff[0],self.tokens[diff[0]])
            aeTuple = (diff[1],self.tokens[diff[1]])
        else:
            timexTuple = (diff[1],self.tokens[diff[1]])
            aeTuple = (diff[0],self.tokens[diff[0]])
            
        #Figure out of timex tuple is <TIMEX2> or </TIMEX2> and act accordingly
        if timexTuple[1].lower() == '<TIMEX2>'.lower():
            date = list(itertools.takewhile(lambda x: x.lower() != '</TIMEX2>'.lower(), self.tokens[timexTuple[0] + 1:]))
        else:
            reversedList = self.tokens[::-1]

            date = list(itertools.takewhile(lambda x: x.lower() != '<TIMEX2>'.lower(), reversedList[(len(self.tokens) - timexTuple[0]):]))
            date = date[::-1]

        print date

