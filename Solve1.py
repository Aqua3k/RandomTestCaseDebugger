def main():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    if n <= 4: k = 1/0
    print(sum(a), min(b) - m//9)


if __name__ == '__main__':
    main()
