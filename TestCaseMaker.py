"""
テストケースを作成する
"""

import random
import os
import shutil
from MyLib import *

testCaseNum = 10
testCaseDirec = "in"
testCaseFileName = "case"

####################################

def MakeTestCase():
    """テストケースの入力形式を書く"""
    # Write Code Here
    n = MakeRandomValue(2, 10)
    m = MakeRandomValue(2, 10)
    PrintTestCase(n, m)

    a = MakeRandomArray(n, 1, 10)
    b = MakeRandomArray(m, 1, 10)
    PrintTestCase(*a)
    PrintTestCase(*b)

def PrintTestCase(*arg, **keys):
    """ファイルに出力"""
    global idx
    fileName = testCaseFileName + str(idx+1) + ".txt"
    f = open(os.path.join(testCaseDirec, fileName), 'a')
    print(*arg, **keys, file=f)
    f.close()

####################################

idx = 0
def MakeAllTestCase():
    """全テストケースを作成"""
    global testCaseNum
    for i in range(testCaseNum):
        global idx
        idx = i
        MakeTestCase()

####################################

# 以下、ランダム入力生成用のライブラリ

# 各関数についている引数コメントの説明
#    ◆arg
#       "◆"が1つついている引数には必ず値を指定してください
#        指定しないとエラーになります
#    ◆◆key (= defaultValue)
#       "◆"が2つついている引数はデフォルト引数になります
#       指定しなくてもエラーは起こりません
#       説明文の後ろの"defaultValue"がデフォルト値になります
#       引数を指定するときは func(key=value) のようにして値を与えてください

def MakeRandomValue(minVal, maxVal, type="int", keta=9):
    """値を生成する

    引数
        ◆minVal
            最小値
        ◆maxVal
            最大値
        ◆type
            "int":      整数
            "float":    小数
        ◆keta
            小数を指定する場合の小数点以下の最大桁数
            何も指定しなければketa=9
    """
    if type == "int":   return random.randint(minVal, maxVal)
    if type == "float": return round(random.uniform(minVal, maxVal), keta)
    assert 0, "type error in MakeRandomValue()"

def MakeRandomString(length=10,same="True"):
    """アルファベット小文字のみの文字列を生成する

    引数
        ◆length
            文字列の長さ
        ◆same (= True)
            通常は同じ文字を多く含んでいた方が都合がいいことが多い(数え上げとか)ので、
            同じ文字を含みやすい生成方法を使っている
            完全ランダムにしたい場合はsame=Falseを指定
    """
    ret = ""
    s = set()
    for i in range(length):
        r = 0
        if same: r = random.randint(0,1)

        if r == 0 and len(s):
            p = random.randint(0, len(s)-1)
            ret += list(s)[p]
        else:
            p = random.randint(0,25)
            c = chr( ord("a") + p )
            ret += c
            s.add(c)
    return ret

def MakeRandomArray(length, minVal, maxVal, type="int", permutation=False, order=None):
    """配列の作成
    引数
        ◆length
            配列の長さ
        ◆minVal
            最小値
        ◆maxVal
            最大値
        ◆type
            "int":      整数
            "float":    小数
            "str":      文字列
        ◆permutation (= False)
            =Trueのとき、長さlengthの順列を作成する(length以外の引数は使わない)
            デフォルトはFalse
        ◆order (= None)
            "U":    昇順ソート済み
            "D":    降順ソート済み
            other:  指定しない(たまたまソートされた状態になる可能性はある)
    """
    if permutation:
        L = list(range(1, length+1))
        random.shuffle(L)
        return L

    ret = []
    for i in range(length):
        if   type == "int":   ret.append(MakeRandomValue(minVal, maxVal))
        elif type == "float": ret.append(MakeRandomValue(minVal, maxVal,type="float"))
        elif type == "str":   ret.append(MakeRandomString())
        else: assert 0, "type error in MakeRandomArray()"
    if   order == "U": ret = sorted(ret)
    elif order == "D": ret = sorted(ret, reverse=True)
    return ret

def MakeRandomGraph(N, M, weight=False, weightMin=1, weightMax=100,\
    tree=False, connect=False, selfEdge=False, multiEdge=False, index=1):
    """グラフの生成

    戻り値の形式
        M, UV
        M:    UVの長さ
        UV:   長さM*2(重さありを指定した場合はM*3)の2次元配列を返す
    i番目の辺がuiとvi(重さをwi)を結ぶとすると、
    [[u1, v1, (w1)], [u2, v2, (w2)], ..., [um, vm, (wm)]]
    という形式
    引数
        ◆N
            頂点数
        ◆M
            辺の数
        ◆cost (= False)
            True:   辺に重みあり
            False:  辺に重みなし
        ◆costMin (= 1)
        ◆costMax (= 100)
            重みの最小値と最大値
            weight=Falseのときは使わない
        ◆tree (= False)
            True:   グラフは木(M = N-1になる)
            False:  指定しない(できたグラフがたまたま木である可能性はある)
        ◆connect (= False)
            True:   作成されるグラフは連結
                    (M < N-1のとき、M = N-1になる)
            False:  指定しない(できるグラフがたまたま連結になる可能性はある)
        ◆selfEdge (= False)
            True:   自己辺の存在を許す
            False:  自己辺は存在しない
        ◆multiEdge (= False)
            True:   多重辺の存在を許す
            False:  多重辺は存在しない
        ◆index (= 1)
            0:      0-indexで頂点を表す
            1:      1-indexで頂点を表す
        other:  Error
    note: selfEdgeとmultiEdgeの結果を考慮し、
          Mがあり得る上限より大きいときは上限値に丸められる
    """

    assert 0 <= index <= 1, "index value error in MakeRandomGraph()"

    #値の範囲のチェック
    if tree: #木なら辺の数はN-1
        M = N-1
    elif connect: #連結なら辺の数は最低N-1
        if M < N-1:
            M = N-1
    if multiEdge:      edgeMax = 10**18 #無限大
    elif not selfEdge: edgeMax = N*(N-1)//2
    else:              edgeMax = N*(N+1)//2
    M = min(edgeMax, M)

    ret = []
    uf = UnionFind(N+1)

    edgeSet = set([])
    while len(ret) < M:
        u = random.randint(0,N-1) + index
        v = random.randint(0,N-1) + index
        if Check(N,len(ret),u,v,edgeSet,uf,tree,connect,selfEdge,multiEdge):
            edgeSet.add((u,v))
            edgeSet.add((v,u))
            uf.union(u,v)
            if weight:
                w = random.randint(weightMin, weightMax)
                ret.append([u,v,w])
            else:
                ret.append([u,v])
    random.shuffle(ret)
    return M, ret

def Check(N,edgeNum,u,v,edgeSet,uf,tree,connect,selfEdge,multiEdge):
    """引数で指定したグラフになるかどうかを判定"""
    if not selfEdge: #自己辺を許さなくてu=vならFalse
        if u == v: return False
    if tree or connect: #連結させる必要があるなら
        if edgeNum < N-1: #まだ連結していない2点ではないといけない
            if uf.same(u,v): return False
    if not multiEdge:
        if (u,v) in edgeSet or (v,u) in edgeSet: return False
    return True

def InitTestCaseDirectory():
    """テストケースディレクトリの初期化"""
    shutil.rmtree(testCaseDirec, ignore_errors=True)
    os.mkdir(testCaseDirec)

def main():
    InitTestCaseDirectory()
    MakeAllTestCase()

if __name__ == "__main__":
    main()

