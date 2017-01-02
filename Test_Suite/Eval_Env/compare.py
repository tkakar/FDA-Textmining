#!/usr/bin/env python
import xml.etree.cElementTree as et

sxml = """
<ANNOTATIONS textSource=\"fda010.txt\" annotator=\"Amber Wallace\">
<EVENT_DT start=null end=null></EVENT_DT>
<DEMOGRAPHICS>
<AGE_SET>
<AGE start=\"50\" end=\"52\">71</AGE>
<AGE_COD start=\"53\" end=\"61\">YR</AGE_COD>
</AGE_SET>
<WT_SET>
<WT start=\"153\" end=\"156\">160</WT>
<WT_COD start=\"157\" end=\"163\">LBS</WT_COD>
</WT_SET>
<SEX start=\"72\" end=\"78\">F</SEX>
</DEMOGRAPHICS>
<DRUG_FILE>
<INSTANCE>
      <DRUGNAME start="551" end="557">MYCINS</DRUGNAME>
      <ROUTE start=null end=null></ROUTE>
      <DECHAL start=null end=null></DECHAL>
      <RECHAL start=null end=null></RECHAL>
      <DOSE_AMT start=null end=null></DOSE_AMT>
      <DOSE_UNIT start=null end=null></DOSE_UNIT>
      <DOSE_FORM start=null end=null></DOSE_FORM>
      <DOSE_FREQ start=null end=null></DOSE_FREQ>
    </INSTANCE>
    <INSTANCE>
      <DRUGNAME start="629" end="634">SULFA</DRUGNAME>
      <ROUTE start=null end=null></ROUTE>
      <DECHAL start=null end=null></DECHAL>
      <RECHAL start=null end=null></RECHAL>
      <DOSE_AMT start=null end=null></DOSE_AMT>
      <DOSE_UNIT start=null end=null></DOSE_UNIT>
      <DOSE_FORM start=null end=null></DOSE_FORM>
      <DOSE_FREQ start=null end=null></DOSE_FREQ>
    </INSTANCE>
    <INSTANCE>
      <DRUGNAME start="689" end="702">CANAGLIFLOZIN</DRUGNAME>
      <ROUTE start="712" end="716">ORAL</ROUTE>
      <DECHAL start=null end=null></DECHAL>
      <RECHAL start=null end=null></RECHAL>
      <DOSE_AMT start="733" end="736">300</DOSE_AMT>
      <DOSE_UNIT start="737" end="739">MG</DOSE_UNIT>
      <DOSE_FORM start="704" end="710">TABLETS</DOSE_FORM>
      <DOSE_FREQ start="740" end="750">QD</DOSE_FREQ>
    </INSTANCE>
</DRUG_FILE>
<REACTION_FILE>
<PT start=null end=null></PT>
</REACTION_FILE>
<INDICATION_FILE>
<INDI_PT start=null end=null></INDI_PT>
</INDICATION_FILE>
</ANNOTATIONS>
"""

tree = et.formstring(sxml)

for el in tree.findall('ANNOTATIONS'):
    print '-------------------'
    for ch in el.getchildren():
        print '{:>15}: {:<30}'.format(ch.tag, ch.text)

        # print "\nan alternate way:"
# el=tree.find('INSTANCE[2]/DRUGNAME')  # xpath
# print '{:>15}: {:<30}'.format(el.tag, el.text)
