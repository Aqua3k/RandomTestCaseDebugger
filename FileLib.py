"""
テストケースファイルと実行結果ファイルの名前・パスを保存・読み込みするユーティリティ
"""

import Debug as dl
import os

inputFileName = ""
outputFileName = ""
outFilePath = ""
def SetFileName(testCaseName, module):
    """実行するテストケースとその結果ファイルを一時的に記録"""
    global inputFileName, outputFileName, outFilePath
    inputFileName = testCaseName
    outputFileName = module + ".txt"
    outFilePath = os.path.basename(testCaseName).split(".")[0]

    os.makedirs(os.path.join(dl.outPath, outFilePath), exist_ok=True)
def GetInputFileName():
    """実行するテストケースファイル名を取得"""
    return inputFileName
def GetOutputFileName():
    """実行結果の出力先のファイル名を取得"""
    return outputFileName
def GetOutputFilePath():
    """実行結果の出力先パスを取得"""
    return outFilePath

fileContents = []
def SetFileContents():
    """テストケースの各行を読み込みfileContentsに保存"""
    global fileContents
    path = GetInputFileName()
    with open(path) as f:
        fileContents = [s.strip() for s in f.readlines()][::-1]
