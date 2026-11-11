import sys
import typing as tp
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float
    label: int


@dataclass
class Line:
    a: float
    b: float
    c: float


def func(p: Point, l: Line) -> float:
    return p.x * l.a + p.y * l.b + l.c


def predict(p: Point, l: Line) -> int:
    sign = func(p, l) >= 0
    return 1 if sign else -1


def calculate_accuracy(points: tp.List[Point], line: Line) -> float:
    acc = 0
    for point in points:
        prediction = predict(point, line)
        if prediction == point.label:
            acc += 1
    return acc / len(points)


def read_input(filename: str) -> tp.List[Point]:
    points = []
    with open(filename, mode="r") as f:
        f.readline()  # skip reading points number
        for line in f.readlines():
            x, y, l = map(int, line.split())
            points.append(Point(x, y, l))
    return points


def read_output(filename: str) -> Line:
    try:
        with open(filename, mode="r") as f:
            a, b, c = map(float, f.readline().split())
        return Line(a, b, c)
    except:
        print("PE")
        sys.exit(2)


def main():
    points = read_input(sys.argv[1])
    line = read_output(sys.argv[2])

    accuracy = calculate_accuracy(points, line)
    accuracy = int(100 * accuracy)
    if accuracy > 97:
        print(f"{accuracy} OK")
    else:
        print("0 OK")
    sys.exit(0)


if __name__ == '__main__':
    main()
