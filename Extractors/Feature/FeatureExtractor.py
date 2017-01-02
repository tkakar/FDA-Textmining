import hashlib
import string
import re
import pickle
from operator import itemgetter


class FeatureExtractor(object):
    def __init__(self):
        pass

    def GetPOSFeatureValue(self, postag):

        #        ClauseLevel = ['S','SBAR','SBARQ','SINV','SQ']
        #        PhraseLevel = ['ADJP','ADVP','CONJP','FRAG','INTJ','LST','NAC','NP','NX','PP','PRN','PRT','QP','RRC','UCP','VP','WHADJP','WHAVP','WHNP','WHPP','X']
        WordLevel = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS',
                     'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG',
                     'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']

        try:
            return WordLevel.index(postag)
        except ValueError:
            #            print 'Value not found'
            return -1

    def GetPhrasalClassFeatureValue(self, postag):

        ClauseLevel = ['S', 'SBAR', 'SBARQ', 'SINV', 'SQ']
        PhraseLevel = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP',
                       'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X']
        #        WordLevel = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS','PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']
        PhraseLevel += ClauseLevel

        try:
            return PhraseLevel.index(postag)
        except ValueError:
            #           print 'Value not found'
            return -1

    def ContainCapitalLetter(self, token):
        if (any(x.isupper() for x in token)):
            return 1
        else:
            return 0

    def ContainDigit(self, token):
        if (any(x.isdigit() for x in token)):
            return 1
        else:
            return 0

    def IsPunctuation(self, token):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        if all(x in string.punctuation for x in token) or token == '-LRB-' or token == '-RRB-':
            return 1
        else:
            return 0

    def IsStartWithLetterEndWithNumber(self, token):  # 1: is , -1: opposite, 0: neither
        if len(token) < 1:
            print "token cannot be empty"
            return -2

        if token[0].isdigit() and token[-1].isalpha():
            return -1

        elif token[-1].isdigit() and token[0].isalpha():
            return 1
        else:
            return 0

    def GetPrefixValue(self, num, token):
        result = []
        i = 0
        while i < num:

            if i + 1 <= len(token):
                result.append(ord(token[i]))
            else:
                result.append(-1)
            i = i + 1

        return result

    def GetSufixValue(self, num, token):
        result = []
        i = len(token)
        while i > 0 and num > 0:
            result.append(ord(token[i - 1]))
            num = num - 1
            i = i - 1

        if num == 0:
            return result
        else:
            while num > 0:
                result.append(-1)
                num = num - 1
            return result

    def GetPrefixSufixValue(self, num, token):
        result = []
        if len(token) >= num:
            result.append(self.GetStringValue(8, token[0:num - 1]))
            result.append(self.GetStringValue(8, token[-num:-1]))
        else:
            result.append(int(self.GetStringValue(8, token)))
            result.append(int(self.GetStringValue(8, token)))
        return result

    def GetREFeatures(self, token):
        # hard coded patterns
        result = []
        CAPS = "[A-Z]";
        LOW = "[a-z]";
        CAPSNUM = "[A-Z0-9]";
        ALPHA = "[A-Za-z]";
        ALPHANUM = "[A-Za-z0-9]";
        PUNCTUATION = "[,\\.;:?!()]";
        QUOTE = "[\"`']";
        GREEK = "(alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|omicron|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega)";

        features = {"INITCAPS": "[A-Z].*",
                    "INITCAPSALPHA": "[A-Z][a-z].*",
                    "ALLCAPS": "[A-Z]+",
                    "CAPSMIX": "[A-Za-z]+",
                    "HASDIGIT": ".*[0-9].*",
                    "SINGLEDIGIT": "[0-9]",
                    "DOUBLEDIGIT": "[0-9][0-9]",
                    "NATURALNUMBER": "[0-9]+",
                    "REALNUMBER": "[-0-9]+[.,]+[0-9.,]+",
                    "HASDASH": ".*-.*",
                    "INITDASH": "-.*",
                    "ENDDASH": ".*-",
                    "ALPHANUMERIC": ".*[A-Za-z].*[0-9].*",
                    "ALPHANUMERIC": ".*[0-9].*[A-Za-z].*",
                    "ROMAN": "[IVXDLCM]+",
                    "HASROMAN": ".*\\b[IVXDLCM]+\\b.*",
                    "GREEK": GREEK,
                    "HASGREEK": ".*\\b" + GREEK + "\\b.*",
                    "PUNCTUATION": "[,.;:?!-+!()-[]{}\"<>./@#$%^&*_~']|-LRB-|-RRB-"}

        for key, pattern in features.iteritems():
            if re.match(pattern, token):
                result.append(1)
            else:
                result.append(0)

        return result

    def GetStringValue(self, num, token):

        return int(hashlib.sha224(token).hexdigest(), 16) % (10 ** 8)

    def GetDigitCollapsesValue(self, token):

        word = ""

        if re.match("19|20\\d\\d", token):
            word = "<YEAR>"
        elif re.match("19|20\\d\\ds", token):
            word = "<YEARDECADE>"
        elif re.match("19|20\\d\\d-\\d+", token):
            word = "<YEARSPAN>"
        elif re.match("\\d+\\\\/\\d", token):
            word = "<FRACTION>"
        elif re.match("\\d[\\d,\\.]*", token):
            word = "<DIGITS>"
        elif re.match("19|20\\d\\d-\\d\\d-\\d--d", token):
            word = "<DATELINEDATE>"
        elif re.match("19|20\\d\\d-\\d\\d-\\d\\d", token):
            word = "<DATELINEDATE>"
        elif re.match(".*-led", token):
            word = "<LED>"
        elif re.match(".*-sponsored", token):
            word = "<LED>"

        if word == "":
            return 0
        else:
            return self.GetStringValue(8, word)

    def GetWordClassValue(self, token):

        token = re.sub("[A-Z]", "A", token)
        token = re.sub("[a-z]", "a", token)
        token = re.sub("[0-9]", "0", token)
        token = re.sub("[^A-Za-z0-9]", "x", token)

        return self.GetStringValue(8, token)

    def get_PhrasalClass(self, tree):
        chr_array = list(tree)
        stack = []
        result = []
        s = ''
        L = False
        R = False
        for c in chr_array:
            if c == '(':
                if s != '' and s != ' ':
                    stack.append(s.strip())
                    s = ''
                if L == False:
                    L = True
                    R = False
            elif c == ')':
                if R == False:
                    R = True
                    L = False
                    str = s.strip().split(' ')
                    s = ''
                    result.append([str[1], str[0], stack[-1]])
                elif R == True:
                    stack.pop()
            else:
                s += c

        return result
