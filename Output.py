from abc import ABC, abstractmethod

from MyLib import AllResultStatus
from template import errorMessage, noDifference, differenceFound, noError, ErrorOccured


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

    def __init__(self, allStatus: AllResultStatus) -> None:
        super().__init__()

    def output(self) -> None:
        pass


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
