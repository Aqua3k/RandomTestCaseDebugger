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
import traceback
import subprocess

import TestCaseMaker as tcm
import FileLib as fl
from MyLib import GetIndex, ResultStatus, AllResultStatus
from Output import StandardOutput, FileOutput, HTMLOutput

outPath = "out"

prog1 = "solve1.py"
prog2 = "solve2.py"
cmd = "python {name} < {inFile} > {outFile}"

####################################

def GetAllFileName() -> list[str]:
    """すべてのテストケースファイルを取得する"""
    return glob.glob(os.path.join(tcm.testCaseDirec, "*"))

messages = []
def ExacSolve1(status: ResultStatus) -> None:
    """Solve1.pyを実行して実行結果を引数で与えられたクラスに記録する"""
    errFlg = False
    errMsg = None

    inFile = fl.GetInputFileName()
    outFile = "out\\case" + str(status.idx) + "\\"+ fl.GetOutputFileName()

    res = subprocess.run(cmd.format(name=prog1, inFile=inFile, outFile=outFile),
     encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    
    if res.returncode != 0:
        errMsg = res.stderr
        errFlg = True
    
    status.errFlg1 = errFlg
    status.errMsg1 = errMsg

def ExacSolve2(status: ResultStatus) -> None:
    """Solve2.pyを実行して実行結果を引数で与えられたクラスに記録する"""
    errFlg = False
    errMsg = None

    inFile = fl.GetInputFileName()
    outFile = "out\\case" + str(status.idx) + "\\"+ fl.GetOutputFileName()

    res = subprocess.run(cmd.format(name=prog2, inFile=inFile, outFile=outFile),
     encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    
    if res.returncode != 0:
        errMsg = res.stderr
        errFlg = True
    
    status.errFlg2 = errFlg
    status.errMsg2 = errMsg

def InitResult() -> None:
    """実行結果の出力先ディレクトリを初期化する"""
    shutil.rmtree(outPath, ignore_errors=True)
    os.mkdir(outPath)

def InitAll():
    """初期化処理のまとめ
    Note: 必要な初期化処理が増えた時のために分離しておく
    """
    InitResult()

def ExacTestCaseAndRecordResult(testCasePath: str) -> ResultStatus:
    """引数で与えられたテストケースを実行して結果を記録"""
    status = ResultStatus() #結果記録用のクラスを作成
    name = os.path.basename(testCasePath)
    status.caseName = name
    status.idx = GetIndex(name)

    #Solve1.py実行
    fl.SetFileName(testCasePath, "Solve1")
    fl.SetFileContents()
    ExacSolve1(status)
    #Solve2.py実行
    fl.SetFileName(testCasePath, "Solve2")
    fl.SetFileContents()
    ExacSolve2(status)

    #比較対象のファイルをGet
    files = glob.glob(os.path.join(outPath, fl.GetOutputFilePath(), "*"))

    status.outPaths = files

    if status.IsErrorOccurred(): #エラーが発生した時はdiffのHTMLファイルは作れない
        status.result = "RE"
    elif len(files) != 2:         pass #Getしたファイルの数が2個ではなかった場合(基本ありえない)
    elif not filecmp.cmp(*files): status.result = "WA"
    else:                         status.result = "AC"

    #全部のメンバに代入されたかチェック
    assert status.Check(), "Error: Some 'ResultStatus' class members have initial value."
    return status

def main() -> None:
    InitAll()

    allResultStatus = AllResultStatus()
    for testCasePath in GetAllFileName():
        status = ExacTestCaseAndRecordResult(testCasePath)
        allResultStatus.RegisterResultStatus(status)

    std = StandardOutput(allResultStatus)
    std.Output()
    file = FileOutput(allResultStatus)
    file.Output()
    html = HTMLOutput(allResultStatus)
    html.Clear()
    html.Output()

if __name__ == "__main__":
    main()
