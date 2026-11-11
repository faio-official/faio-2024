#!/usr/bin/env python3
"""FAIO 2024 B "The story of a meteorologist" — algorun per-test checker.

Called as: checker.py <input_path> <expected_path> <user_output_path>
Prints one JSON line: {"score": float, "verdict": str, "message": str}.

The participant outputs the outlier values (IQR method) on one line, in any order; an
empty line means "no outliers". A test passes (score 100) when the participant's values
match the jury's set — same count, each within abs_tol=1e-3 after sorting — otherwise 0.
(Ported from the original Yandex binary 1/0 checker, rescaled to algorun's 0–100 per-test
convention; this version also requires the counts to be equal, so an incomplete list cannot
pass by coincidence.)
"""
import json
import sys

ABS_TOL = 1e-3


def read_ans(path):
    """A list of floats, or the empty string sentinel for an empty line."""
    with open(path, "r", encoding="utf-8") as f:
        line = f.readline().strip()
    if len(line) == 0:
        return ""
    return [float(tok) for tok in line.split()]


def isclose(a, b):
    return abs(a - b) <= ABS_TOL


def check(input_path, expected_path, output_path):
    try:
        prd = read_ans(output_path)
    except Exception:
        return 0.0, "PE", "Could not parse your output as a list of numbers."
    tgt = read_ans(expected_path)

    both_empty = isinstance(tgt, str) and isinstance(prd, str)
    both_lists = isinstance(tgt, list) and isinstance(prd, list)
    if both_empty:
        return 100.0, "OK", "Correct (no outliers)."
    if both_lists:
        p, t = sorted(prd), sorted(tgt)
        if len(p) == len(t) and all(isclose(i, j) for i, j in zip(p, t)):
            return 100.0, "OK", "Correct."
        return 0.0, "WA", "Your outlier set does not match the expected one."
    # one empty, one non-empty
    return 0.0, "WA", "Your outlier set does not match the expected one."


def main():
    input_path, expected_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]
    score, verdict, message = check(input_path, expected_path, output_path)
    print(json.dumps({"score": float(score), "verdict": verdict, "message": message}))


if __name__ == "__main__":
    main()
