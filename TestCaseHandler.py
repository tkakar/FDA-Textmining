import os, glob
import ProjectAERIS

inputPath = '/home/vsocrates/My_Documents/fda_textmining/FDA-Textmining/Test_Suite/Test_Cases_UNIX'

outputPath = '/home/vsocrates/My_Documents/fda_textmining/FDA-Textmining/Postprocessing/IntermediateFiles'

configFilePath = '/home/vsocrates/My_Documents/fda_textmining/FDA-Textmining/Resources/config.json'

def main():
    count = 0
    for filename in glob.glob(os.path.join(inputPath, '*.txt')):
        if count > 4: break
        
        lastFolderIdx = filename.rfind(r'/')
        outputFileName = filename[lastFolderIdx + 1:-4]
        print 'outputFileName', outputPath+r'/'+outputFileName+'.xml'
        print 'filename: ', filename, 'outputpath: ', outputPath+r'/'+outputFileName+'.xml', 'configpath: ', configFilePath
        ProjectAERIS.main(filename, outputPath+r'/'+outputFileName+'.xml', configFilePath)
        count += 1
#        rawTextFile = f.read()

if __name__ == '__main__':
    main()
