DEBUG = 0
if __name__ != "__main__":
    DEBUG = 1
    import Debug as dl

def MyInput():
    global DEBUG
    if DEBUG: return dl.DebugInput()
    else: return input()

def MyPrint(*arg, **keys):
    global DEBUG
    if DEBUG: return dl.DebugPrint(*arg, **keys)
    else: return print(*arg, **keys)

######################################################################

n, m = map(int,MyInput().split())
a = list(map(int,MyInput().split()))
b =  list(map(int,MyInput().split()))

MyPrint(sum(a), min(b))
