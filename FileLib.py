import Debug as dl
import os
import glob

inputFileName = ""
outputFileName = ""
outFilePath = ""
def SetFileName(testCaseName, module):
    global inputFileName, outputFileName, outFilePath
    inputFileName = testCaseName
    outputFileName = module + ".txt"
    outFilePath = os.path.basename(testCaseName)
    outFilePath = outFilePath.split(".")[0]

    d = glob.glob(os.path.join(dl.outPath, "*"))
    if os.path.join(dl.outPath, outFilePath) not in d:
        os.mkdir(os.path.join(dl.outPath, outFilePath))
def GetInputFileName():
    return inputFileName
def GetOutputFileName():
    return outputFileName
def GetOutputFilePath():
    return outFilePath

fileContents = []
def SetFileContents():
    global fileContents
    path = GetInputFileName()
    with open(path) as f:
        fileContents = [s.strip() for s in f.readlines()][::-1]
