import sys
import typing as tp

def read_ans(filename: str) -> tp.Tuple[float]:
    try:
        with open(filename, mode="r") as f:
            ans = f.readline()
        return ans
    except:
        print("PE")
        sys.exit(2)
    
def calculate_accuracy(prd: tp.List[str], tgt: tp.List[str]) -> float:
    correct = sum(1 for p, t in zip(prd, tgt) if p == t)
    accuracy = round((correct / len(tgt))*100,6)
    return accuracy

def main():
    prd = read_ans(sys.argv[2])
    tgt = read_ans(sys.argv[3])
    prd, tgt = str(prd).strip().split(', '), str(tgt).strip().split(', ')
    score = 0
    if len(tgt)==len(prd):
        score = calculate_accuracy(prd, tgt)
   
    if score>0:
        print(f"{score} OK")
        sys.exit(0)
    else:
        print(f"{score} WA")
        sys.exit(1)

    


if __name__ == '__main__':
    main()
