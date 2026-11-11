import sys


def main():
    try:
        with open(sys.argv[2], mode="r") as f:
            prediction = float(f.readline().split()[0])
    except:
        print("PE")
        sys.exit(2)

    with open(sys.argv[3], mode="r") as f:
        target = float(f.readline().split()[0])

    percent = abs((target - prediction) / target)
    if percent < 0.01:
        print("100 OK")
    else:
        print("0 OK")


if __name__ == '__main__':
    main()
