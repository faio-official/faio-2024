#!/usr/bin/env python3
"""FAIO 2024 F "SVM" — algorun per-test checker.

Called as: checker.py <input_path> <expected_path> <user_output_path>
Prints one JSON line: {"score": float, "verdict": str, "message": str}.

- input_path  : the points — first line k, then k lines "x y label" (label is +1 or -1).
- user_output : the separating line as three numbers "a b c" (for a*x + b*y + c = 0).
- expected_path : unused — this task has no gold file; the score is computed geometrically
                  from the points and the submitted line.

A point is classified +1 when a*x + b*y + c >= 0, else -1. The accuracy is the fraction
of correctly classified points; the per-test score is int(100 * accuracy) if that exceeds
97, otherwise 0 — identical to the original Yandex checker.
"""
import json
import sys


def read_points(path):
    pts = []
    with open(path, "r", encoding="utf-8") as f:
        f.readline()  # skip the count
        for line in f:
            if line.strip():
                x, y, l = map(int, line.split())
                pts.append((x, y, l))
    return pts


def check(input_path, expected_path, output_path):
    points = read_points(input_path)
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            a, b, c = map(float, f.readline().split())
    except Exception:
        return 0.0, "PE", "Could not parse your line (expected three numbers: a b c)."
    correct = 0
    for x, y, label in points:
        pred = 1 if (a * x + b * y + c) >= 0 else -1
        if pred == label:
            correct += 1
    accuracy = int(100 * (correct / len(points)))
    if accuracy > 97:
        return float(accuracy), "OK", f"Accuracy {accuracy}% ({correct}/{len(points)})."
    return 0.0, "WA", f"Accuracy {accuracy}% (must exceed 97%)."


def main():
    input_path, expected_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]
    score, verdict, message = check(input_path, expected_path, output_path)
    print(json.dumps({"score": float(score), "verdict": verdict, "message": message}))


if __name__ == "__main__":
    main()
