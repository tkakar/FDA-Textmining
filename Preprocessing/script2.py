from pymetamap import MetaMap

# the server installed on your machine
mm = MetaMap.get_instance('/work/tkakar/public_mm/bin/metamap14')

### if using manual input
# sents = ['she fell down and felt dizzy after taking neproxin.', 'heart attack']
# concepts,error = mm.extract_concepts(sents,[1,2],word_sense_disambiguation=True)


## if using file as input
sample_text = 'textSample.txt'
concepts, error = mm.extract_concepts(filename=sample_text, word_sense_disambiguation=True)

## specify output filename
f = open('Vimig/Results.txt', 'w')
for concept in concepts:
    ## if want to output specific semtypes uncomment below command
    # if concept.semtypes in [ '[sosy]', '[phsu]', '[dsyn]']:
    print >> f, concept
## to print specific information as output
# print >> f, "Trigger= "+concept.trigger +"\t", "SemType= " +concept.semtypes+"\t", "Pos= "+concept.pos_info+"\t"
#		#f.write(concept)
f.close()
