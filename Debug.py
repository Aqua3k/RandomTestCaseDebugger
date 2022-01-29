"""
Solve1.pyとSolve2.pyをそれぞれのテストケースで実行し、実行結果の差を出力する
"""

from __future__ import annotations

import sys
import glob
import os
import shutil
import filecmp
from difflib import HtmlDiff
from template import *
from typing import Any
import traceback

import TestCaseMaker as tcm
import FileLib as fl
from MyLib import GetIndex, ResultStatus, AllResultStatus
from Output import StandardOutput

outPath = "out"
outFile = "Result"
htmlPath = "html"

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
def ExacSolve1(status: ResultStatus) -> None:
    """Solve1.pyを実行して実行結果を引数で与えられたクラスに記録する"""
    errFlg = False
    errMsg = None
    try:
        import Solve1
        Solve1.print = DebugPrint
        Solve1.input = DebugInput
        Solve1.main()
    except:
        errMsg = traceback.format_exc()
        errFlg = True
    if "Solve1" in sys.modules: del sys.modules["Solve1"]
    status.errFlg1 = errFlg
    status.errMsg1 = errMsg

def ExacSolve2(status: ResultStatus) -> None:
    """Solve2.pyを実行して実行結果を引数で与えられたクラスに記録する"""
    errFlg = False
    errMsg = None
    try:
        import Solve2
        Solve2.print = DebugPrint
        Solve2.input = DebugInput
        Solve2.main()
    except:
        errMsg = traceback.format_exc()
        errFlg = True
    if "Solve2" in sys.modules: del sys.modules["Solve2"]
    status.errFlg2 = errFlg
    status.errMsg2 = errMsg

def InitResult() -> None:
    """実行結果の出力先ディレクトリを初期化する"""
    shutil.rmtree(outPath, ignore_errors=True)
    os.mkdir(outPath)

def MakeResultFile(AllStatus: list[ResultStatus]) -> None:
    """実行結果ファイルを作成する"""
    ACcount, WAcount, REcount = 0, 0, 0
    diffList, errList = [], []
    for status in AllStatus:
        if status.IsErrorOccurred():
            REcount += 1
            if status.errFlg1:
                errList.append(errorMessage.format(fileName=status.caseName,\
                     progName="Solve1.py", errorMessage=status.errMsg1))
            if status.errFlg2:
                errList.append(errorMessage.format(fileName=status.caseName,\
                     progName="Solve2.py", errorMessage=status.errMsg2))
        elif status.result == "WA":
            WAcount += 1
            diffList.append(status.caseName)
        elif status.result == "AC":
            ACcount += 1
        else: assert 0, "Error: Unkown status found."

    f = open("result.txt", 'w')
    print(noDifference if WAcount == 0 else differenceFound.format(diffNum=WAcount), file=f)
    print("\n".join(diffList), file=f)
    print(file=f)
    print(noError if REcount == 0 else ErrorOccured.format(errNum=REcount), file=f)
    print("\n".join(errList), file=f)

def InitHTML() -> None:
    """HTMLの出力先ディレクトリを初期化する"""
    shutil.rmtree(htmlPath, ignore_errors=True)
    os.mkdir(htmlPath)

def InsertTextIntoHTMLHead(HTMLStr: str, text: str) -> str:
    """HTMLの文字列のHeadの中に別の文字列を挿入する"""
    HTMLStrList = HTMLStr.split("\n")
    HTMLStrList.insert(HTMLStrList.index("<head>") + 1, text)
    return "\n".join(HTMLStrList)

def MakeDiffHTML(path1: str, path2: str) -> None:
    """HTMLファイル作成"""
    with open(path1,'r') as f: file1 = f.readlines()
    with open(path2,'r') as f: file2 = f.readlines()

    # 比較結果HTMLを作成
    diff = HtmlDiff()
    diffStr = InsertTextIntoHTMLHead(diff.make_file(file1, file2), cssLink)
    path = fl.GetOutputFilePath() + ".html"
    with open(os.path.join(htmlPath, path) ,'w', encoding='utf-8', newline='\n') as html:
        html.writelines(diffStr)

def MakeErrorHTML(status: ResultStatus) -> None:
    """エラーメッセージのHTMLファイル作成"""
    bodyList = []
    if status.errFlg1:
        bodyList.append("Error occured in Solve1.py" + "<br>")
        bodyList.append(status.errMsg1.replace("\n", "<br>").replace(" ", "&nbsp;"))
    if status.errFlg2:
        bodyList.append("Error occured in Solve2.py" + "<br>")
        bodyList.append(status.errMsg2.replace("\n", "<br>").replace(" ", "&nbsp;"))
    with open(os.path.join(htmlPath, fl.GetOutputFilePath() + ".html") ,'w',\
         encoding='utf-8', newline='\n') as html:
        html.writelines(HTMLText.format(title="Error Message", body="\n".join(bodyList)))

def MakeHTMLResult(AllStatus: list[ResultStatus]) -> None:
    """結果のHTMLファイル作成"""
    textList = []
    header = TableBody.format(text1="Test Case Name", color="", text2="Result", text3="Result Link")
    textList.append(header)
    for status in AllStatus:
        if   status.result == "AC": color = "lime"
        elif status.result == "WA": color = "yellow"
        else:                       color = "violet"
        testCasePath = os.path.join(tcm.testCaseDirec, status.caseName)
        testCaseLink = HTMLLinkStr.format(path=testCasePath, string=status.caseName)
        HTMLPath = os.path.join(htmlPath, "case" + str(status.idx) + ".html")
        HTMLLink = HTMLLinkStr.format(path=HTMLPath, string="Link")
        lineStr = TableBody.format(text1=testCaseLink, color=color, text2=status.result, text3=HTMLLink)
        textList.append(lineStr)

    tableHTML = Table.format(border=3, body="\n".join(textList))
    resultFileName = "result.html"
    with open(resultFileName ,'w', encoding='utf-8', newline='\n') as html:
        text = HTMLText.format(body=tableHTML, title="Result")
        html.writelines(InsertTextIntoHTMLHead(text, cssLink))

def OutputAllResult(AllStatus: list[ResultStatus]) -> None:
    """結果出力のまとめ"""
    MakeResultFile(AllStatus)
    MakeHTMLResult(AllStatus)

def InitAll():
    """初期化処理のまとめ
    Note: 必要な初期化処理が増えた時のために分離しておく"""
    InitResult()
    InitHTML()

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

    if status.IsErrorOccurred(): #エラーが発生した時はdiffのHTMLファイルは作れない
        status.result = "RE"
        assert status.Check(), "Error: Some 'ResultStatus' class members have initial value."
        MakeErrorHTML(status)
        return status
    elif len(files) != 2:         pass #Getしたファイルの数が2個ではなかった場合(基本ありえない)
    elif not filecmp.cmp(*files): status.result = "WA"
    else:                         status.result = "AC"

    #比較結果HTMLファイル作成
    MakeDiffHTML(*files)

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
    std.output()

    OutputAllResult(allResultStatus.rawAllResultStatus())

if __name__ == "__main__":
    main()
