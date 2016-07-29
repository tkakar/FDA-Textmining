from __future__ import division
import csv
import xlwt
import xlrd
import openpyxl

class Evaluate(object):
    
    def __init__(self):
        pass
    
    def eval(self,file):
        print file.split("/")[-1]
        result = {}
        xl_workbook = xlrd.open_workbook(file)
        xl_sheet = xl_workbook.sheet_by_index(0) #first sheet
        for index in xrange(xl_sheet.nrows):
            #the entity name and the extractor name
            key = xl_sheet.cell_value(index,2) + "|" + xl_sheet.cell_value(index,11)
            #print 'key', key
#           key = line[2]# + "|" + line [1] #Entity Type and Extractor Name
            confusion = [0,0,0,0]
            case = xl_sheet.cell_value(index,10) # TP ...etc
            if result.has_key(key) is False:
                result[key] = confusion
            
            if case == 'TP':
                result.get(key)[0] += 1
            elif case == 'FP':
                result.get(key)[1] += 1
            elif case == 'FN':
                result.get(key)[2] += 1
            else: # TN or something else
                result.get(key)[3] += 1
        #print result
        #result.pop('AGE_COD|AgeRegExtrator')
        return result
    
    def get_measures(self,result,file):
        f = open(file, 'a')
        #f.write("Entity,Extractor,True Positive, False Positive, False negative, True Negative, Precision, Recall\n")
        for key, value in result.iteritems():
            precision = .0
            recall = .0
            tp = value[0]
            p_d = value[0] + value[1]
            r_d = value[0] + value[2]
            if p_d == 0:
                precision = -1
            else:
                precision = tp / p_d
            
            if r_d == 0:
                recall = -1
            else:
                recall = tp / r_d
                
            kv = key.split("|")
            #line = str[0] + "," +str[1]+ "," +value[0]+ "," +value[1]+ "," +value[2]+ "," +value[3]+ "," +precision+ "," +recall
            print " ".join(kv),value,"precision:",precision,"recall:",recall
            if len(kv) > 1:
                f.write(",".join(kv) + ",")
            else:
                f.write(",".join(kv) + "," + ",")
            f.write(",".join(str(e) for e in value) + ",")
            f.write(str(precision) + "," + str(recall) + "\n")
            
Eval = Evaluate()
Eval.get_measures(Eval.eval('Test_Suite/Eval_Env/dataOut2.xls'),'results/r1.csv')
