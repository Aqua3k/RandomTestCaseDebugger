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

def GetIndex(caseName):
    retStr = ""
    for s in caseName:
        if "0" <= s <= "9": retStr += s
    return int(s)

class ResultStatus():
    def __init__(self, caseName, status, errFlg1, errFlg2, errMsg1=None, errMsg2=None):
        self.idx = GetIndex(caseName)
        self.caseName = caseName
        self.status = status
        self.errFlg1 = errFlg1
        self.errFlg2 = errFlg2
        self.errMsg1 = errMsg1
        self.errMsg2 = errMsg2
    def __repr__(self): #__repr__を定義しておくとクラスのままソートできるらしい
        return repr(self.idx)
