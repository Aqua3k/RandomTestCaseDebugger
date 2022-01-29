# もし生成用の関数群を別ファイルに移すならここかな？

#UnionFind
class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n
        self.group = n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x
        self.group -= 1

    def size(self, x):
        return -self.parents[self.find(x)]

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self):
        return self.group

    def all_group_members(self):
        return {r: self.members(r) for r in self.roots()}

    def __str__(self):
        return '\n'.join('{}: {}'.format(r, self.members(r)) for r in self.roots())

def GetIndex(caseName: str) -> int:
    """テストケースの名前からindexのみを取り出す"""
    retStr = ""
    for s in caseName:
        if "0" <= s <= "9": retStr += s
    return int(retStr)

class ResultStatus():
    """実行結果の情報を管理するクラス"""
    def __init__(self):
        self.idx = ""
        self.caseName = ""
        self.result = ""
        self.errFlg1 = False
        self.errFlg2 = False
        self.errMsg1 = ""
        self.errMsg2 = ""
    def IsErrorOccurred(self) -> bool:
        """エラーが起こったかどうか"""
        return self.errFlg1 or self.errFlg2
    def Check(self) -> bool:
        """すべてのメンバが更新されたかチェックする
        Note: errFlg1,2はもともとFlaseで初期化してあるのでそれ以外のメンバのみをチェック"""
        allMembers = [self.idx, self.caseName, self.result, self.errMsg1, self.errMsg2]
        for member in allMembers:
            if str(member) == "": return False
        return True
    def __lt__(self, other) -> bool:
        """__lt__を定義しておくとクラスのままソートが可能になる"""
        return self.idx < other.idx
    def __str__(self) -> str:
        """デバッグ用"""
        allMembers = [self.idx, self.caseName, self.result, self.errFlg1, self.errFlg2, self.errMsg1, self.errMsg2]
        return " ".join( list(map(str, allMembers)) ) + "\n"

class AllResultStatus():
    """ResultStatusのリスト用のクラス"""

    def __init__(self, allResultStatus: list[ResultStatus]) -> None:
        self._allResultStatus = allResultStatus
