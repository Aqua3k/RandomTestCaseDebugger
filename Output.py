from abc import ABC, abstractmethod

from MyLib import AllResultStatus


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
        pass


class HTMLOutput(Output):
    """差分結果をHTMLに出力するクラス"""

    def __init__(self, allStatus: AllResultStatus) -> None:
        super().__init__()

    def output(self) -> None:
        pass


class FileOutput(Output):
    """差分結果をファイル出力するクラス"""

    def __init__(self, allStatus: AllResultStatus) -> None:
        super().__init__()

    def output(self) -> None:
        pass
