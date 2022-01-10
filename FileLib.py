import Debug as dl
import os

inputFileName = ""
outputFileName = ""
outFilePath = ""
def SetFileName(testCaseName, module):
    global inputFileName, outputFileName, outFilePath
    inputFileName = testCaseName
    outputFileName = module + ".txt"
    outFilePath = os.path.basename(testCaseName).split(".")[0]

    os.makedirs(os.path.join(dl.outPath, outFilePath), exist_ok=True)
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
