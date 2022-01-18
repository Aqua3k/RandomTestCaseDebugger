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
def ExacSolve1() -> None:
    """Solve1.pyを実行して結果を記録する"""
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

def ExacSolve2() -> None:
    """Solve2.pyを実行して結果を記録する"""
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

result = []
def main() -> None:
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
