#!/usr/bin/python
#import xmltodict
import json
import sys
import lxml.etree as ET
import xlwt
from datetime import datetime
from xlutils.copy import copy
import xlrd

#class to compare annotated xml to program output
class Compare:
    aroot = None
    oroot = None

    #tuple fields
    entity = None
    fileName = None
    avc = None #annotated value
    asspan = None #annotated start span
    aespan = None #annotated end span
    pv = None #program value
    psspan = None #program start span
    pespan = None #program end span
    scval = None #strict confusion value TP/TN/FP/FN
    lcval = None #loose confusion value TP/TN/FP/FN

    def __init__(self, ann, out):
        #get and store the roots of each tree
        Compare.aroot = ET.parse(ann).getroot()
        Compare.oroot = ET.parse(out).getroot()
        Compare.fileName = out

    def run_compare(self, entity, extractor):
        Compare.run_ann(self, entity)
        Compare.run_out(self, entity, extractor)
        Compare.run_strict(self)
        Compare.run_loose(self)
        Compare.write_to_file(self)

    def run_strict(self):
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
        print(Compare.scval)

    def run_loose(self):
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
        print(Compare.lcval)

    def run_ann(self, entity):
        atype = Compare.aroot.xpath('.//'+entity)
        Compare.entity = entity
        for instance in atype:
            if instance is not None:
                Compare.entity = instance.tag
                Compare.asspan = instance.get('start')
                Compare.aespan = instance.get('end')
                Compare.avc = instance.text

    def run_out(self, entity, extractor):
        atype = Compare.oroot.xpath('.//'+entity+'[@extractor=\''+extractor+'\']')
        for instance in atype:
            if instance is not None:
                Compare.pv = instance.text
                print(Compare.pv)
                Compare.psspan = instance.get('start')
                print(Compare.psspan)
                Compare.pespan = instance.get('end')

    def write_to_file(self):
        rb = xlrd.open_workbook('dataOut.xls',formatting_info=True)
        r_sheet = rb.sheet_by_index(0) 
        r = r_sheet.nrows
        w = copy(rb) 
        sheet = w.get_sheet(0) 
        sheet.write(r,0,"new val")
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
        w.save('dataOut.xls')
        #clear vars
        Compare.entity = None
        Compare.fileName = None
        Compare.avc = None #annotated value
        Compare.asspan = None #annotated start span
        Compare.aespan = None #annotated end span
        Compare.pv = None #program value
        Compare.psspan = None #program start span
        Compare.pespan = None #program end span
        Compare.scval = None #strict confusion value TP/TN/FP/FN
        Compare.lcval = None #loose confusion value TP/TN/FP/FN




#run some examples/tests
comp = Compare('test.xml','output_sample.xml')
comp.run_compare('DRUGNAME', 'drugExtractor1')
comp.run_compare('AGE_COD', 'ageCodExtractor1')
