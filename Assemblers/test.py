#!/usr/bin/python
#import xmltodict
import json
import sys
import xml.etree.ElementTree as ET
import xlwt
from datetime import datetime
from xlutils.copy import copy
import xlrd

#class to compare annotated xml to program output
class Compare:
    aroot = None #root of annotated xml
    oroot = None #root of program output xml
    runCode = None #unique code for this run 
    pathToFile = '/work/tkakar/git-repos/FDA-Textmining/Test_Suite/Eval_Env/dataOut.xls'	
    entity = None #name of entity
    fileName = None #name of file
    avc = None #annotated value
    asspan = None #annotated start span
    aespan = None #annotated end span
    pv = None #program value
    psspan = None #program start span
    pespan = None #program end span
    scval = None #strict confusion value TP/TN/FP/FN
    lcval = None #loose confusion value TP/TN/FP/FN
    extractor = None #name of program extractor (different than entity)
    di = {} #dictionary for comparison of multiples

    ###########################################
    #TP = Annotated field == Program field
    # TN = Annotated field missing & Program field missing
    # FP = Program finds Incorrect value for field
    # FN = Annotated field Found & Program field missing

    # Examples:
    # AGE
    # Ann: 35     Out: 35       TP
    # Ann:        Out:          TN
    # Ann:        Out: 35       FP
    # Ann: 35     Out: 23       FP
    # Ann: 35     Out:          FN
    #################################################

    #Class to compare annotated xml to program output xml
    def __init__(self, ann, out):
        #print 'from test.py ann: ', ann
        #print 'from test.py out: ', out
        #get and store the roots of each tree
        Compare.aroot = ET.parse(ann).getroot()
        Compare.oroot = ET.parse(out).getroot()
#        ET.dump(Compare.aroot)
        Compare.fileName = out

    #call this function to write multiple drugs/reactions/etc to the excel file
    def multi_write_to_file(self):
	
        rb = xlrd.open_workbook(Compare.pathToFile)
        r_sheet = rb.sheet_by_index(0) 
        r = r_sheet.nrows
        if Compare.runCode is None:
            Compare.runCode = int(r_sheet.cell(r-1,0).value)+1
        w = copy(rb) 
        sheet = w.get_sheet(0) 
        for key in Compare.di:
            sheet.write(r,0, Compare.runCode)
            sheet.write(r,1, Compare.fileName)
            sheet.write(r,2, Compare.entity)
            sheet.write(r,9, Compare.di[key]['cv'])
            sheet.write(r,11, Compare.extractor)   
            #only fill in the correct fields
            if Compare.di[key]['cv'] is not 'FP': #TP or FN
                sheet.write(r,3, Compare.di[key]['value'])
                sheet.write(r,4, key)
                sheet.write(r,5, Compare.di[key]['end'])
                if Compare.di[key]['cv'] is 'TP':
                    sheet.write(r,6, Compare.di[key]['pvalue'])
                    sheet.write(r,7, key)
                    sheet.write(r,8, Compare.di[key]['end'])
            else:
                sheet.write(r,6, Compare.di[key]['pvalue'])
                sheet.write(r,7, key)
                sheet.write(r,8, Compare.di[key]['end'])
            r += 1

	
        w.save(Compare.pathToFile)

        #clear vars
        Compare.clearVars(self)

    def multi_compare(self, entity, extractor):
        Compare.extractor = extractor
        atype = Compare.aroot.findall('.//'+entity)
        Compare.entity = entity
        for instance in atype:
            if instance is not None:
                Compare.asspan = instance.get('start')
                Compare.aespan = instance.get('end')
                Compare.avc = instance.text
                Compare.di[Compare.asspan] = {'end':Compare.aespan, 'value':Compare.avc, 'cv':'FN'}
                corefs = instance.findall('../COREF')
                for coref in corefs:

                    Compare.asspan = coref.get('start')
                    Compare.aespan = coref.get('end')
                    Compare.di[Compare.asspan] = {'end':Compare.aespan, 'value':Compare.avc, 'cv':'FN'}


        #address output
        otype = Compare.oroot.findall('.//'+entity+'[@extractor=\''+extractor+'\']')
        for oinstance in otype:
            if oinstance is not None:
                Compare.psspan = oinstance.get('start')
                Compare.pespan = oinstance.get('end')
                Compare.pv = oinstance.text
                if Compare.di.has_key(Compare.psspan) and Compare.di[Compare.psspan]['end'] == Compare.pespan:
                    Compare.di[Compare.psspan]['cv'] = 'TP'
                    Compare.di[Compare.psspan]['pvalue'] = Compare.pv
                else:
                    Compare.di[Compare.psspan] = {'end':Compare.pespan, 'pvalue':Compare.pv, 'cv':'FP'}
        Compare.multi_write_to_file(self)


    def run_compare(self, entity, extractor):
        Compare.extractor = extractor
        Compare.run_ann(self, entity)
        Compare.run_out(self, entity, extractor)
        Compare.run_strict(self)
        Compare.run_loose(self)
        Compare.write_to_file(self)

    def run_strict(self): #strict is based on matching start and end span
        if Compare.asspan is not None and Compare.psspan is not None:
            if Compare.asspan == Compare.psspan and Compare.aespan == Compare.pespan:
                Compare.scval = "TP"
            else:
                Compare.scval = "FP"
        elif Compare.asspan is not None:
            Compare.scval = "FN"
        elif Compare.psspan is not None:
            Compare.scval = "FP"
        else:
            Compare.scval = "TN"

    def run_loose(self): #loose is based on matching content string
        if Compare.avc is not None and Compare.pv is not None:
            if Compare.avc == Compare.pv:
                Compare.lcval = "TP"
            else:
                Compare.lcval = "FP"
        elif Compare.avc is not None:
            Compare.lcval = "FN"
        elif Compare.pv is not None:
            Compare.lcval = "FP"
        else:
            Compare.lcval = "TN"

    def run_ann(self, entity):
        atype = Compare.aroot.findall('.//'+entity)
        Compare.entity = entity
        for instance in atype:
            if instance is not None:
                Compare.entity = instance.tag
                Compare.asspan = instance.get('start')
                Compare.aespan = instance.get('end')
                Compare.avc = instance.text

    def run_out(self, entity, extractor):
        atype = Compare.oroot.findall('.//'+entity+'[@extractor=\''+extractor+'\']')
        for instance in atype:
            if instance is not None:
                Compare.pv = instance.text
                Compare.psspan = instance.get('start')
                Compare.pespan = instance.get('end')

    #write a single instance like age or weight to file
    def write_to_file(self):

        rb = xlrd.open_workbook(Compare.pathToFile)

        r_sheet = rb.sheet_by_index(0) 
        r = r_sheet.nrows
        if Compare.runCode is None:
            Compare.runCode = int(r_sheet.cell(r-1,0).value)+1
        w = copy(rb) 
        sheet = w.get_sheet(0) 
        sheet.write(r,0, Compare.runCode)
        sheet.write(r,1, Compare.fileName)
        sheet.write(r,2, Compare.entity)
        sheet.write(r,3, Compare.avc)
        sheet.write(r,4, Compare.asspan)
        sheet.write(r,5, Compare.aespan)
        sheet.write(r,6, Compare.pv)
        sheet.write(r,7, Compare.psspan)
        sheet.write(r,8, Compare.pespan)
        sheet.write(r,9, Compare.scval)
        sheet.write(r,10, Compare.lcval)
        sheet.write(r,11, Compare.extractor)
        w.save(Compare.pathToFile)

        #clear vars
        Compare.clearVars(self)

    #clear vars so they are not unintentionally coppied over to the next entry
    def clearVars(self):
        Compare.entity = None
        Compare.avc = None #annotated value
        Compare.asspan = None #annotated start span
        Compare.aespan = None #annotated end span
        Compare.pv = None #program value
        Compare.psspan = None #program start span
        Compare.pespan = None #program end span
        Compare.scval = None #strict confusion value TP/TN/FP/FN
        Compare.lcval = None #loose confusion value TP/TN/FP/FN
        Compare.extractor = None
        Compare.di = {}




#run some examples/tests
#comp = Compare('../../Test_Suite/Eval_Env/xml/fda001.xml','../../Test_Suite/Eval_Env/semifinal/fda001_EVENT_DT_Semifinal.xml')
#comp.run_compare('EVENT_DT', 'AERecognitionEventDateExtractor')
#comp.multi_compare('DRUGNAME', 'drugExtractor1')
