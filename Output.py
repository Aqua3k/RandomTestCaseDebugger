import os
import shutil
from difflib import HtmlDiff
from abc import ABC, abstractmethod

import FileLib as fl
from MyLib import AllResultStatus, ResultStatus
import TestCaseMaker as tcm
from template import (
    errorMessage, noDifference, differenceFound, noError, ErrorOccured,
    HTMLText, Table, HTMLLinkStr, TableBody, cssLink
)


class Output(ABC):
    """差分結果を出力する抽象クラス"""

    def __init__(self, allStatus: AllResultStatus) -> None:
        self._allStatus = allStatus

    @abstractmethod
    def output(self) -> None:
        pass


class StandardOutput(Output):
    """差分結果を標準出力するクラス"""

    def __init__(self, allStatus: AllResultStatus) -> None:
        super().__init__(allStatus)

    def output(self) -> None:
        """結果のサマリを標準出力する"""

        print(f"AC | {self._allStatus.ACcount}\n"
              f"WA | {self._allStatus.WAcount}\n"
              f"RE | {self._allStatus.REcount}")


class HTMLOutput(Output):
    """差分結果をHTMLに出力するクラス"""

    htmlPath = 'html'

    def __init__(self, allStatus: AllResultStatus) -> None:
        super().__init__(allStatus)

    def clear(self) -> None:
        """既存の出力ファイルを削除する"""
        shutil.rmtree(__class__.htmlPath, ignore_errors=True)
        os.mkdir(__class__.htmlPath)

    def output(self) -> None:
        self._MakeHTMLResult()
        for status in self._allStatus:
            if status.result == 'RE':
                self._MakeErrorHTML(status)
            else:
                self._MakeDiffHTML(*status.outPaths)

    def _MakeErrorHTML(self, status: ResultStatus) -> None:
        """エラーメッセージのHTMLファイル作成"""
        bodyList = []
        if status.errFlg1:
            bodyList.append('Error occured in Solve1.py<br>')
            bodyList.append(__class__.toHTML(status.errMsg1))
        if status.errFlg2:
            bodyList.append('Error occured in Solve2.py<br>')
            bodyList.append(__class__.toHTML(status.errMsg2))

        outputPath = os.path.join(__class__.htmlPath, fl.GetOutputFilePath() + '.html')
        with open(outputPath, 'w') as html:
            html.writelines(HTMLText.format(title='Error Message', body='\n'.join(bodyList)))

    def _InsertTextIntoHTMLHead(self, HTMLStr: str, text: str) -> str:
        """HTMLの文字列のHeadの中に別の文字列を挿入する"""
        HTMLStrList = HTMLStr.split("\n")
        HTMLStrList.insert(HTMLStrList.index("<head>") + 1, text)
        return "\n".join(HTMLStrList)

    def _MakeDiffHTML(self, path1: str, path2: str) -> None:
        """HTMLファイル作成"""
        with open(path1, 'r') as f:
            file1 = f.readlines()
        with open(path2, 'r') as f:
            file2 = f.readlines()

        # 比較結果HTMLを作成
        diff = HtmlDiff()
        diffStr = self._InsertTextIntoHTMLHead(diff.make_file(file1, file2), cssLink)
        path = fl.GetOutputFilePath() + ".html"
        with open(os.path.join(__class__.htmlPath, path), 'w') as html:
            html.writelines(diffStr)

    def _MakeHTMLResult(self) -> None:
        """結果のHTMLファイル作成"""
        textList = []
        header = TableBody.format(text1="Test Case Name", color="", text2="Result", text3="Result Link")
        textList.append(header)
        for status in self._allStatus:
            if status.result == "AC":
                color = "lime"
            elif status.result == "WA":
                color = "yellow"
            else:
                color = "violet"
            testCasePath = os.path.join(tcm.testCaseDirec, status.caseName)
            testCaseLink = HTMLLinkStr.format(path=testCasePath, string=status.caseName)
            HTMLPath = os.path.join(__class__.htmlPath, "case" + str(status.idx) + ".html")
            HTMLLink = HTMLLinkStr.format(path=HTMLPath, string="Link")
            lineStr = TableBody.format(text1=testCaseLink, color=color, text2=status.result, text3=HTMLLink)
            textList.append(lineStr)

        tableHTML = Table.format(border=3, body="\n".join(textList))
        resultFileName = "result.html"
        with open(resultFileName, 'w', encoding='utf-8', newline='\n') as html:
            text = HTMLText.format(body=tableHTML, title="Result")
            html.writelines(self._InsertTextIntoHTMLHead(text, cssLink))

    @staticmethod
    def toHTML(text: str) -> str:
        """文字列をHTMLに簡易的に変換する"""
        return text.replace('\n', '<br>').replace(' ', '&nbsp;')


class FileOutput(Output):
    """差分結果をファイル出力するクラス"""

    def __init__(self, allStatus: AllResultStatus) -> None:
        super().__init__(allStatus)

    def output(self) -> None:
        """実行結果ファイルを作成する"""

        ACcount, WAcount, REcount = 0, 0, 0
        diffList, errList = [], []
        for status in self._allStatus:
            if status.IsErrorOccurred():
                REcount += 1
                if status.errFlg1:
                    errList.append(errorMessage.format(fileName=status.caseName,
                                                       progName='Solve1.py', errorMessage=status.errMsg1))
                if status.errFlg2:
                    errList.append(errorMessage.format(fileName=status.caseName,
                                                       progName='Solve2.py', errorMessage=status.errMsg2))
            elif status.result == 'WA':
                WAcount += 1
                diffList.append(status.caseName)
            elif status.result == 'AC':
                ACcount += 1
            else:
                assert 0, 'Error: Unkown status found.'

        f = open('result.txt', 'w')
        print(noDifference if WAcount == 0 else differenceFound.format(diffNum=WAcount), file=f)
        print('\n'.join(diffList), file=f)
        print(file=f)
        print(noError if REcount == 0 else ErrorOccured.format(errNum=REcount), file=f)
        print('\n'.join(errList), file=f)
