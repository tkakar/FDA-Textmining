import os, glob
import ProjectAERIS


inputPath = '/work/swunnava/git-repos/TSIntegration1/FDA-Textmining/Test_Suite/Test_Cases/'

outputPath = '/work/swunnava/git-repos/TSIntegration1/FDA-Textmining/Postprocessing/Intermediate4'

configFilePath = '/work/swunnava/git-repos/TSIntegration1/FDA-Textmining/Resources/config_with_age.json'

def main():
    count = 0
    for filename in glob.glob(os.path.join(inputPath, '*.txt')):
#        if count > 4: break
        
        lastFolderIdx = filename.rfind(r'/')
        outputFileName = filename[lastFolderIdx + 1:-4]
        print 'outputFileName', outputPath+r'/'+outputFileName+'.xml'
        print 'filename: ', filename, 'outputpath: ', outputPath+r'/'+outputFileName+'_Intermediate.xml', 'configpath: ', configFilePath
        ProjectAERIS.main(filename, outputPath+r'/'+outputFileName+'_Intermediate.xml', configFilePath)

#        count += 1

if __name__ == '__main__':
    main()
