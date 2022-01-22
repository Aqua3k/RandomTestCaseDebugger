"""
Solve1.pyとSolve2.pyをそれぞれのテストケースで実行し、実行結果の差を出力する
"""

from __future__ import annotations

import sys
import glob
import os
import shutil
import filecmp
from typing import Any

import TestCaseMaker as tcm
import FileLib as fl

outPath = "out"
outFile = "Result"

####################################
#Debug用の入出力

def DebugPrint(*arg: Any, **keys: Any) -> None:
    """実行結果をファイルに出力させる"""
    f = open(os.path.join(outPath, fl.GetOutputFilePath(), fl.GetOutputFileName()), 'a')
    print(*arg, **keys, file=f)
    f.close()

def DebugInput() -> str:
    """入力をテストケースから読み取る"""
    return str(fl.fileContents.pop())

####################################

def GetAllFileName() -> list[str]:
    """すべてのテストケースファイルを取得する"""
    return glob.glob(os.path.join(tcm.testCaseDirec, "*"))

messages = []
def ExacSolve1() -> bool:
    """Solve1.pyを実行して結果を記録する"""
    ret = False
    try:
        import Solve1
        Solve1.print = DebugPrint
        Solve1.input = DebugInput
        Solve1.main()
    except Exception as e:
        fileName = os.path.basename(fl.GetInputFileName())
        errMessage = fileName + " Solve1\n" + str(e)
        messages.append(errMessage)
        ret = True
    if "Solve1" in sys.modules: del sys.modules["Solve1"]
    return ret

def ExacSolve2() -> bool:
    """Solve2.pyを実行して結果を記録する"""
    ret = False
    try:
        import Solve2
        Solve2.print = DebugPrint
        Solve2.input = DebugInput
        Solve2.main()
    except Exception as e:
        fileName = os.path.basename(fl.GetInputFileName())
        errMessage = fileName + " Solve2\n" + str(e)
        messages.append(errMessage)
        ret = True
    if "Solve2" in sys.modules: del sys.modules["Solve2"]
    return ret

def InitResult() -> None:
    """実行結果の出力先ディレクトリを初期化する"""
    shutil.rmtree(outPath, ignore_errors=True)
    os.mkdir(outPath)

def MakeResultFile() -> None:
    """実行結果ファイルを作成する"""
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

def StandardOutput() -> None:
    """結果のサマリを標準出力する"""
    global ACcount, WAcount, REcount
    print("AC |", ACcount)
    print("WA |", WAcount)
    print("RE |", REcount)

result = []
ACcount, WAcount, REcount = 0, 0, 0
def main() -> None:
    global ACcount, WAcount, REcount
    InitResult()
    allTestCaseName = GetAllFileName()

    for testCaseName in allTestCaseName:
        errFlg = False
        #テストケース実行
        fl.SetFileName(testCaseName, "Solve1")
        fl.SetFileContents()
        errFlg |= ExacSolve1()

        fl.SetFileName(testCaseName, "Solve2")
        fl.SetFileContents()
        errFlg |= ExacSolve2()

        #比較
        path = os.path.join(outPath, fl.GetOutputFilePath(), "*")
        file = glob.glob(path)

        if errFlg: #エラーが起こった時
            REcount += 1
        elif len(file) != 2: #ここに入ることは基本ないはず
            pass
        elif not filecmp.cmp(*file): #出力に違いがあった時
            fileName = os.path.basename(testCaseName)
            result.append(fileName)
            WAcount += 1
        else:
            ACcount += 1
    MakeResultFile()
    StandardOutput()

if __name__ == "__main__":
    main()
