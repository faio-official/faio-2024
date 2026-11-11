#!/usr/bin/env python3
"""FAIO 2024 D "Kmeans" — algorun per-test checker.

Called as: checker.py <input_path> <expected_path> <user_output_path>
Prints one JSON line: {"score": float, "verdict": str, "message": str}.

- input_path    : the points — first line n, then n lines "x y".
- user_output   : the participant's k final centroids, one "cx cy" per line.
- expected_path : the jury's centroids — first line k, then k lines "cx cy".

Quality metric (identical to the original Yandex checker): assign each point to its
nearest centroid, take the mean point-to-centroid distance as the loss, and normalise
against the single-centroid (global mean) baseline: m = 1 - loss/baseline (0 if
loss >= baseline). A test scores 100 if the participant's metric is at least ~95% of
the jury's metric (participant > author, or (author-participant)/author < 0.05), else 0.
"""
import json
import sys


def _dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _read_points(path):
    """First line = count, then that many 'x y' lines."""
    with open(path, "r", encoding="utf-8") as f:
        n = int(f.readline())
        return [tuple(map(float, f.readline().split())) for _ in range(n)]


def _read_centroids(path):
    """Raw 'x y' lines (no count prefix) — the participant's output."""
    pts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(float, line.split())
                pts.append((x, y))
    return pts


def _metric(centroids, points):
    mean_point = (sum(p[0] for p in points) / len(points),
                  sum(p[1] for p in points) / len(points))
    baseline = sum(_dist(p, mean_point) for p in points) / len(points)
    loss = 0.0
    for p in points:
        loss += min(_dist(p, c) for c in centroids)
    loss /= len(points)
    if baseline == 0:
        return 0.0
    if loss > baseline:
        return 0.0
    return 1 - loss / baseline


def check(input_path, expected_path, output_path):
    points = _read_points(input_path)
    target = _read_points(expected_path)
    try:
        centroids = _read_centroids(output_path)
    except Exception:
        return 0.0, "PE", "Could not parse your centroids."
    if not centroids:
        return 0.0, "PE", "No centroids in your output."
    if len(centroids) != len(target):
        return 0.0, "PE", f"Expected {len(target)} centroids, got {len(centroids)}."

    author = _metric(target, points)
    participant = _metric(centroids, points)
    if author == 0:
        score = 100 if participant >= 0 else 0
    elif participant > author or (author - participant) / author < 0.05:
        score = 100
    else:
        score = 0
    msg = f"metric {participant:.4f} vs jury {author:.4f}"
    return float(score), ("OK" if score == 100 else "WA"), msg


def main():
    input_path, expected_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]
    score, verdict, message = check(input_path, expected_path, output_path)
    print(json.dumps({"score": float(score), "verdict": verdict, "message": message}))


if __name__ == "__main__":
    main()
