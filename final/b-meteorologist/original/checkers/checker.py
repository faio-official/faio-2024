import sys
import typing as tp

def read_ans(filename: str) -> tp.Tuple[float]:
    with open(filename, mode="r") as f:
        ans = f.readline()
    ans = ans.strip()
    if len(ans.strip()) == 0:
        return str(ans)
    return [float(i) for i in ans.split(' ')]

def isclose(a, b, abs_tol=1e-3):
    return abs(a-b) <= abs_tol


def main():
    try:
        prd = read_ans(sys.argv[2])
    except:
        print("PE")
        sys.exit(2)
    
    tgt = read_ans(sys.argv[3])

    score = 0
    if isinstance(tgt, str) and isinstance(prd, str):
        score = 1
    elif isinstance(tgt, list) and isinstance(prd, list):
        prd = sorted(prd)
        tgt = sorted(tgt)
        if sum([isclose(i, j) for i, j in zip(prd, tgt)]) == len(prd):
            score = 1        
    else:
        score = 0

    if score == 1:
        print(f"{score} OK")
        sys.exit(0)
    else:
        print(f"{score} WA")
        sys.exit(1)


if __name__ == '__main__':
    main()
