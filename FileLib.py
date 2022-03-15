"""
テストケースファイルと実行結果ファイルの名前・パスを保存・読み込みするユーティリティ
"""

import os

outPath = "out"

inputFileName = ""
outputFileName = ""
outFilePath = ""
def SetFileName(testCaseName: str, module: str) -> None:
    """実行するテストケースとその結果ファイルを一時的に記録"""
    global inputFileName, outputFileName, outFilePath
    inputFileName = testCaseName
    outputFileName = module + ".txt"
    outFilePath = os.path.basename(testCaseName).split(".")[0]

    os.makedirs(os.path.join(outPath, outFilePath), exist_ok=True)
def GetInputFileName() -> str:
    """実行するテストケースファイル名を取得
    Note: Debug.pyからの相対パスを返す"""
    return inputFileName
def GetOutputFileName() -> str:
    """実行結果の出力先のファイル名を取得
    Note: Debug.pyからの相対パスを返す"""
    return os.path.join(outPath, outFilePath, outputFileName)
def GetOutputFilePath() -> str:
    """実行結果の出力先パスを取得"""
    return outFilePath

