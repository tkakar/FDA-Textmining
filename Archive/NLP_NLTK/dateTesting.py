import nltk
import re
import pprint 

def main():
	raw1 = open('../Test_Suite/test_cases/single_patient/fda1.txt').read()
	raw2 = open('../Test_Suite/test_cases/single_patient/fda7.txt').read() 
	raw3 = open('../Test_Suite/test_cases/single_patient/fda8.txt').read()
	raw4 = open('../Test_Suite/test_cases/multiple_patient/fda6.txt').read()
	raw5 = open('../Test_Suite/test_cases/multiple_patient/fda2.txt').read()

	outputfile = open('output.txt', 'w+')

	raw1_pos_tagged = ie_preprocess(raw1)
	raw2_pos_tagged = ie_preprocess(raw2)
	raw3_pos_tagged = ie_preprocess(raw3)
	raw4_pos_tagged = ie_preprocess(raw4)
	raw5_pos_tagged = ie_preprocess(raw5)


	ans1List = []
	ans2List = []
	ans3List = []
	ans4List = []
	ans5List = []

	ans1List = numEx(raw1_pos_tagged)
	ans2List = numEx(raw2_pos_tagged)
	ans3List = numEx(raw3_pos_tagged)
	ans4List = numEx(raw4_pos_tagged)
	ans5List = numEx(raw5_pos_tagged)




	outputfile.write(pprint.pformat(ans1List))
	outputfile.write("\n")

	outputfile.write(pprint.pformat(ans2List))
	outputfile.write("\n")

	outputfile.write(pprint.pformat(ans3List))
	outputfile.write("\n")

	outputfile.write(pprint.pformat(ans4List))
	outputfile.write("\n")

	outputfile.write(pprint.pformat(ans5List))
	outputfile.write("\n")

	outputfile.close()

def numEx(tagList):
	ansList = []
	for sent in tagList:
		for (word,tag) in sent:
			if tag == 'CD':
				ansList.append(sent)
	return ansList

def ie_preprocess(document):
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	return sentences

if __name__ == '__main__':
    main()
