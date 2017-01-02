import re
from Preprocessing.Preprocessor import Preprocessor
from DataElements.DosageElement import DosageElement


class DosageRegExtractor(object):
    def __init__(self, rawTextFileName, intermediateXMLFileName):
        preprocess = Preprocessor(rawTextFileName, intermediateXMLFileName)
        self.Text = preprocess.rawText()

    def findEntity(self):

        dosage_amount = {'dos_amt': [], 'a_offset': []}
        dosage_unit = {'dos_unit': [], 'u_offset': []}
        dosage_freq = {'dos_freq': [], 'f_offset': []}

        freq = '(week|day|month)'
        Freq = '(once|twice|everyday|weekly|every other day|one|two|three|four|five)'
        dose = '(mg|miligram|miligrams|mgs|kg|ug|ml|ul|mililitre|mls|milititres|tabs|tablets|tablet)'
        freq_code = '(1X|BID|BIW|HS|PRN|Q12H|Q2H|Q3H|Q3W|Q4H|Q5H|Q6H|Q8H|QD|QH|QID|QM|QOD|QOW|TID|TIW|UNK|QHS)'

        regex = re.compile(r'((\d{1,4}(\.[0-9]{1})?).?' + dose + '.?'
                                                                 '(.?([0-9].every.[0-9].' + freq + ')|(.?[0-9].times.a.' + freq + ')|(.?([0-9].?-.?[0-9].?times.?(per|a).?' + freq + '))|(.?' + Freq + '.?(a|per).?' + freq + ')|(.?' + freq_code + '))?)'
                                                                                                                                                                                                                                                    '',
                           re.IGNORECASE)

        it = re.finditer(regex, self.Text)

        for match in it:
            record = match.groups()

            dosage_amount['dos_amt'].append(record[1])

            dosage_amount['a_offset'].append(match.span(2))
            dosage_unit['dos_unit'].append(record[3])
            dosage_unit['u_offset'].append(match.span(4))
            dosage_freq['dos_freq'].append(record[4])
            dosage_freq['f_offset'].append(match.span(5))
        # print(dosage_amount, dosage_freq, dosage_unit)
        elementList = []
        for a in range(0, len(dosage_amount['dos_amt'])):
            # print (dosage_freq['dos_freq'][a], [list(dosage_freq['f_offset'][a])]  )

            elementList.append([DosageElement(dosage_amount['dos_amt'][a], [list(dosage_amount['a_offset'][a])],
                                              "DosageRegExtractor", "DOSE_AMT"),
                                DosageElement(dosage_freq['dos_freq'][a], [list(dosage_freq['f_offset'][a])],
                                              "DosageRegExtractor", "DOSE_FREQ"),
                                DosageElement(dosage_unit['dos_unit'][a], [list(dosage_unit['u_offset'][a])],
                                              "DosageRegExtractor", "DOSE_UNIT")])

        # print elementList
        return elementList
