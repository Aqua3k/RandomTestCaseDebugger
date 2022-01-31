import os
import shutil
from difflib import HtmlDiff
from abc import ABC, abstractmethod

from MyLib import AllResultStatus, ResultStatus
import TestCaseMaker as tcm
from template import (
    errorMessage, noDifference, differenceFound, noError, ErrorOccured,
    HTMLText, Table, HTMLLinkStr, TableBody, TableBodyHeading, cssLink
)

class Output(ABC):
    """差分結果を出力する抽象クラス"""

    def __init__(self, allStatus: AllResultStatus) -> None:
        self._allStatus = allStatus

    @abstractmethod
    def Clear(self) -> None:
        """既存の結果ファイルを削除する抽象メソッド"""
        pass

    @abstractmethod
    def Output(self) -> None:
        """差分結果を出力する抽象メソッド"""
        pass

class StandardOutput(Output):
    """差分結果を標準出力するクラス"""

    def __init__(self, allStatus: AllResultStatus) -> None:
        super().__init__(allStatus)

    def Clear(self) -> None:
        """削除するファイルはない"""
        pass

    def Output(self) -> None:
        """結果のサマリを標準出力する"""

        print(f"AC | {self._allStatus.ACcount}\n"
              f"WA | {self._allStatus.WAcount}\n"
              f"RE | {self._allStatus.REcount}")

class HTMLOutput(Output):
    """差分結果をHTMLに出力するクラス"""

    htmlPath = 'html'

    def __init__(self, allStatus: AllResultStatus) -> None:
        super().__init__(allStatus)

    def Clear(self) -> None:
        """既存の出力ファイルを削除する"""
        shutil.rmtree(__class__.htmlPath, ignore_errors=True)
        os.mkdir(__class__.htmlPath)

    def Output(self) -> None:
        """差分結果をHTMLとして出力する"""
        self._MakeHTMLResult()
        for status in self._allStatus:
            if status.result == 'RE':
                self._MakeErrorHTML(status)
            else:
                self._MakeDiffHTML(status)

    def _MakeErrorHTML(self, status: ResultStatus) -> None:
        """エラーメッセージのHTMLファイル作成"""
        bodyList = []
        if status.errFlg1:
            bodyList.append('Error occured in Solve1.py<br>')
            bodyList.append(__class__.ToHTML(status.errMsg1))
        if status.errFlg2:
            bodyList.append('Error occured in Solve2.py<br>')
            bodyList.append(__class__.ToHTML(status.errMsg2))

        HTMLPath = __class__.BuildHTMLPath(status)
        with open(HTMLPath, 'w', encoding='utf-8', newline='\n') as html:
            html.writelines(HTMLText.format(title='Error Message', body='\n'.join(bodyList)))

    def _InsertTextIntoHTMLHead(self, HTMLStr: str, text: str) -> str:
        """HTMLの文字列のHeadの中に別の文字列を挿入する"""
        HTMLStrList = HTMLStr.split("\n")
        HTMLStrList.insert(HTMLStrList.index("<head>") + 1, text)
        return "\n".join(HTMLStrList)

    def _MakeDiffHTML(self, status: ResultStatus) -> None:
        """HTMLファイル作成"""
        with open(status.outPaths[0], 'r') as f:
            file1 = f.readlines()
        with open(status.outPaths[1], 'r') as f:
            file2 = f.readlines()

        # 比較結果HTMLを作成
        diff = HtmlDiff()
        diffStr = self._InsertTextIntoHTMLHead(diff.make_file(file1, file2), cssLink)
        HTMLPath = __class__.BuildHTMLPath(status)
        with open(HTMLPath, 'w') as html:
            html.writelines(diffStr)

    def _MakeHTMLResult(self) -> None:
        """結果のHTMLファイル作成"""
        textList = []
        header = TableBodyHeading.format(text1="Test Case Name", color="", text2="Result", text3="Result Link")
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
            HTMLPath = __class__.BuildHTMLPath(status)
            HTMLLink = HTMLLinkStr.format(path=HTMLPath, string="Link")
            lineStr = TableBody.format(text1=testCaseLink, color=color, text2=status.result, text3=HTMLLink)
            textList.append(lineStr)

        tableHTML = Table.format(border=3, body="\n".join(textList))
        resultFileName = "result.html"
        with open(resultFileName, 'w', encoding='utf-8', newline='\n') as html:
            text = HTMLText.format(body=tableHTML, title="Result")
            html.writelines(self._InsertTextIntoHTMLHead(text, cssLink))

    @staticmethod
    def ToHTML(text: str) -> str:
        """文字列をHTMLに簡易的に変換する"""
        return text.replace('\n', '<br>').replace(' ', '&nbsp;')

    @classmethod
    def BuildHTMLPath(clas, status: ResultStatus) -> str:
        """ResultStatusの出力先HTMLファイルのパスを返す"""
        return os.path.join(__class__.htmlPath, 'case' + str(status.idx) + '.html')

class FileOutput(Output):
    """差分結果をファイル出力するクラス"""

    resultFile = 'result.txt'

    def __init__(self, allStatus: AllResultStatus) -> None:
        super().__init__(allStatus)

    def Clear(self) -> None:
        """result.txtを削除する"""
        if os.path.isfile(__class__.resultFile):
            os.remove(__class__.resultFile)

    def Output(self) -> None:
        """実行結果ファイルを作成する"""

        diffList, errList = [], []
        for status in self._allStatus:
            if status.IsErrorOccurred():
                if status.errFlg1:
                    errList.append(errorMessage.format(fileName=status.caseName,
                                                       progName='Solve1.py', errorMessage=status.errMsg1))
                if status.errFlg2:
                    errList.append(errorMessage.format(fileName=status.caseName,
                                                       progName='Solve2.py', errorMessage=status.errMsg2))
            elif status.result == 'WA':
                diffList.append(status.caseName)
            elif status.result == 'AC':
                pass
            else:
                assert 0, 'Error: Unkown status found.'

        f = open(__class__.resultFile, 'w')
        print(noDifference if self._allStatus.WAcount == 0 else differenceFound.format(diffNum=self._allStatus.WAcount), file=f)
        print('\n'.join(diffList), file=f)
        print(file=f)
        print(noError if self._allStatus.REcount == 0 else ErrorOccured.format(errNum=self._allStatus.REcount), file=f)
        print('\n'.join(errList), file=f)
