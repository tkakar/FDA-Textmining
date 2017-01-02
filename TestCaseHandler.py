import os, glob
import timeit
import ProjectAERIS

cwd = os.getcwd()

inputPath = cwd + '/Test_Suite/Test_Cases/gen012.txt'

outputPath = cwd + '/Postprocessing/Intermediate4'

configFilePath = cwd + '/Resources/config.json'

def main():
    # count = 0
    for filename in glob.glob(os.path.join(inputPath, '*.txt')):
        # if count == 5: break
        # count += 1

        lastFolderIdx = filename.rfind(r'/')
        outputFileName = filename[lastFolderIdx + 1:-4]
        print 'outputFileName', outputPath + r'/' + outputFileName + '.xml'
        print 'filename: ', filename, 'outputpath: ', outputPath + r'/' + outputFileName + '_Intermediate.xml', 'configpath: ', configFilePath
        ProjectAERIS.main(filename, outputPath + r'/' + outputFileName + '_Intermediate.xml', configFilePath)


if __name__ == '__main__':
    main()
