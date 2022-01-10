"""
テストケースを作成する
"""

import random
import os
import shutil

testCaseNum = 10
testCaseDirec = "in"
testCaseFileName = "case"

####################################
# テストケースの入力形式を書く
def MakeTestCase():
    # Write Code Here
    n = MakeRandomValue(2, 10)
    m = MakeRandomValue(2, 10)
    PrintTestCase(n, m)

    a = MakeRandomArray(n, 1, 10)
    b = MakeRandomArray(m, 1, 10)
    PrintTestCase(*a)
    PrintTestCase(*b)

# ファイルに出力
def PrintTestCase(*arg, **keys):
    global idx
    fileName = testCaseFileName + str(idx+1) + ".txt"
    f = open(os.path.join(testCaseDirec, fileName), 'a')
    print(*arg, **keys, file=f)
    f.close()

####################################

def InitFile():
    global idx
    fileName = testCaseFileName + str(idx+1) + ".txt"
    f = open(os.path.join(testCaseDirec, fileName), 'w')
    f.close()

idx = 0
def MakeAllTestCase():
    global testCaseNum
    for i in range(testCaseNum):
        global idx
        idx = i
        InitFile()
        MakeTestCase()

####################################
#以下、ランダム入力生成用のライブラリ


# 値を生成する
# minVal
#   最小値
# maxVal
#   最大値
# type
#   "int":      整数
#   "float":    小数
# keta
#   小数を指定する場合の小数点以下の最大桁数
#   何も指定しなければketa=9
def MakeRandomValue(minVal, maxVal, type="int", keta=9):
    if type == "int":   return random.randint(minVal, maxVal)
    if type == "float": return round(random.uniform(minVal, maxVal), keta)
    assert 0, "type error in MakeRandomValue()"

# アルファベット小文字のみの文字列を生成する
# length
#   文字列の長さ
# same
#   同じ文字を多く含んでいた方が都合がいいことが多い(数え上げとか)ので、
#   同じ文字を含みやすい生成方法を使っている
#   完全ランダムにしたい場合のみsame=Falseを指定
def MakeRandomString(length=10,same="True"):
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

# 配列の作成
# length
#   配列の長さ
# minVal
#   最小値
# maxVal
#   最大値
# type
#   "int":      整数
#   "float":    小数
#   "str":      文字列
# permutation
#   =Trueのとき、長さlengthの順列を作成する(length以外の引数は使わない)
#   デフォルトはFalse
# order
#   "U" 昇順ソート済み
#   "D" 降順ソート済み
#   デフォルトはNone
def MakeRandomArray(length, minVal, maxVal, type="int", permutation=False, order=None):
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

def InitTestCaseDirectory():
    shutil.rmtree(testCaseDirec, ignore_errors=True)
    os.mkdir(testCaseDirec)

def main():
    InitTestCaseDirectory()
    MakeAllTestCase()

if __name__ == "__main__":
    main()

