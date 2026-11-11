import sys

from copy import deepcopy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


def distance(p: Point, c: Point) -> float:
    d = (p.x - c.x) ** 2 + (p.y - c.y) ** 2
    return d ** 0.5


def closest_centroid_idx(p: Point, centroids: list[Point]):
    idx = 0
    min_dist = distance(p, centroids[0])
    for i, centroid in enumerate(centroids):
        dist = distance(p, centroid)
        if dist < min_dist:
            idx = i
            min_dist = dist
    return idx


def mean(x: list[float]) -> float:
    return sum(x) / len(x)


def get_mean_point(points: list[Point]) -> Point:
    return Point(x=mean([p.x for p in points]),
                 y=mean([p.y for p in points]))


def metric(centroids: list[Point], points: list[Point]) -> float:
    centroids = deepcopy(centroids)
    points = deepcopy(points)

    # Baseline score when there is only one centroid
    mean_point = get_mean_point(points)
    baseline_loss = sum([distance(p, mean_point) for p in points]) / len(points)

    # Update labels
    for p in points:
        p.l = closest_centroid_idx(p, centroids)

    loss = 0
    for i, c in enumerate(centroids):
        cluster = [p for p in points if p.l == i]
        loss += sum([distance(p, c) for p in cluster])

    loss /= len(points)

    if loss > baseline_loss:
        return 0
    return 1 - loss / baseline_loss


def read_points(path):
    points = []
    with open(path, mode="r") as f:
        n = int(f.readline())
        for _ in range(n):
            x, y = map(float, f.readline().split())
            points.append(Point(x, y))
    return points


def read_centroids(filename: str):
    try:
        points = []
        with open(filename, mode="r") as f:
            for line in f.readlines():
                x, y = map(float, line.split())
                points.append(Point(x, y))
        return points
    except:
        print("PE")
        sys.exit(2)


def main():
    points = read_points(sys.argv[1])
    centroids = read_centroids(sys.argv[2])
    target_centroids = read_points(sys.argv[3])

    if len(centroids) != len(target_centroids):
        print("PE")
        sys.exit(2)
    else:
        autor_score = metric(target_centroids, points)
        participant_score = metric(centroids, points)

        score = 0
        if participant_score > autor_score:
            score = 100
        if (autor_score - participant_score) / autor_score < 0.05:
            score = 100
        print(f"{score} OK")


if __name__ == '__main__':
    main()
