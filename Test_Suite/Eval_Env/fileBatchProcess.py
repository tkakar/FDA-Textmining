# -------------------------------------------------------------------------------
# Name:      File_Operations
# Purpose:   Batch processing of text reports. Open the directory, for each filename,
#            open the file, read the content to a variable, run your code (regex, nltk)
#            and, close the file.
#
# Author:      susmi
#
# Created:     19/03/2016
# Copyright:   (c) susmi 2016
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import os
import glob

path = 'C:/Users/susmi/Documents/FDA/NLP/ReportNarratives'

## The Report_Narratives directory consists of all report narratives as individual text files
for filename in glob.glob(os.path.join(path, '*.txt')):
    f = open(filename, 'r')
    content = f.read()

    ## Include your RegEx and NLTK code here:

    f.close()
