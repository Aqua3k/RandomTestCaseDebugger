def main():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    print(sum(a), min(b))


if __name__ == '__main__':
    main()
