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
def ExacSolve1():
    try:
        import Solve1
        Solve1.print = DebugPrint
        Solve1.input = DebugInput
        Solve1.main()
    except Exception as e:
        fileName = os.path.basename(fl.GetInputFileName())
        errMessage = fileName + " Solve1\n" + str(e)
        messages.append(errMessage)
    if "Solve1" in sys.modules: del sys.modules["Solve1"]

def ExacSolve2():
    try:
        import Solve2
        Solve2.print = DebugPrint
        Solve2.input = DebugInput
        Solve2.main()
    except Exception as e:
        fileName = os.path.basename(fl.GetInputFileName())
        errMessage = fileName + " Solve2\n" + str(e)
        messages.append(errMessage)
    if "Solve2" in sys.modules: del sys.modules["Solve2"]

def InitResult():
    shutil.rmtree(outPath, ignore_errors=True)
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
        fl.SetFileName(testCaseName, "Solve1")
        fl.SetFileContents()
        ExacSolve1()

        fl.SetFileName(testCaseName, "Solve2")
        fl.SetFileContents()
        ExacSolve2()

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
