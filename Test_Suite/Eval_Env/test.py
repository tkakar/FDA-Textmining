#!/usr/bin/python
import xmltodict
import json

with open('test.xml') as fd:
    ann = xmltodict.parse(fd.read())
    
with open('output.xml') as fr:
    out = xmltodict.parse(fr.read())

print(json.dumps(ann, indent = 4))
print(json.dumps(out, indent = 4))

def dict_compare(d1, d2):
    d1_keys = set(d1['ANNOTATIONS'].keys())
    d2_keys = set(d2['ANNOTATIONS'].keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    tp = d1_keys - d2_keys
    fp = d2_keys - d1_keys
    tn = {o : (d1['ANNOTATIONS'][o], d2['ANNOTATIONS'][o]) for o in intersect_keys if d1['ANNOTATIONS'][o] != d2['ANNOTATIONS'][o]}
    fn = set(o for o in intersect_keys if d1['ANNOTATIONS'][o] == d2['ANNOTATIONS'][o])
    return tp, fp, tn, fn

tp, fp, tn, fn = dict_compare(ann, out)

print tp
print fp
print tn
print fn
