import sys
import glob
import os
import shutil
import TestCaseMaker as tcm
import FileLib as fl
import filecmp

outPath = "out"
outFile = "Result"

####################################
#Debug用の入出力

def DebugPrint(*arg, **keys):
    f = open(os.path.join(outPath, fl.GetOutputFilePath(), fl.GetOutputFileName()), 'a')
    print(*arg, **keys, file=f)
    f.close()

def DebugInput():
    return str(fl.fileContents.pop())

####################################

def GetAllFileName():
    return glob.glob(os.path.join(tcm.testCaseDirec, "*"))

messages = []
def ExacMain():
    try:
        import main
    except Exception as e:
        fileName = fl.GetOutputFileName()
        errMessage = str(fileName + e)
        messages.append(errMessage)
    if "main" in sys.modules: del sys.modules["main"]

def ExacGreedy():
    try:
        import greedy
    except Exception as e:
        errMessage = str(e)
        messages.append(errMessage)
    if "greedy" in sys.modules: del sys.modules["greedy"]

def InitResult():
    try: shutil.rmtree(outPath)
    except: pass
    os.mkdir(outPath)

def MakeResultFile():
    f = open("result.txt", 'w')
    if not len(result):
        print("No difference.", file=f)
    else:
        print(len(result), "difference found.", file=f)
        print(*result, sep="\n", file=f)
    print(file=f)
    if not len(messages):
        print("No error occured.", file=f)
    else:
        print(len(messages), "error found.", file=f)
        print(*messages, sep="\n", file=f)

result = []
def main():
    InitResult()
    allTestCaseName = GetAllFileName()

    for testCaseName in allTestCaseName:
        #テストケース実行
        fl.SetFileName(testCaseName, "main")
        fl.SetFileContents()
        ExacMain()

        fl.SetFileName(testCaseName, "greedy")
        fl.SetFileContents()
        ExacGreedy()

        #比較
        path = os.path.join(outPath, fl.GetOutputFilePath(), "*")
        file = glob.glob(path)
        if len(file) != 2:
            pass
        elif not filecmp.cmp(*file):
            fileName = os.path.basename(testCaseName)
            result.append(fileName)

    MakeResultFile()

if __name__ == "__main__":
    main()
