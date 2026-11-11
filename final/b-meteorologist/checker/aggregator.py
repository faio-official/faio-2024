#!/usr/bin/env python3
"""FAIO 2024 B "The story of a meteorologist" — algorun final-score aggregator.

Called as: aggregator.py <results.json>  (array of {TestCaseName, Score, Verdict, ...}).
Prints one JSON line: {"public_score", "private_score", "verdict", "message"}.

Each test scores 100 (pass) or 0 (fail) on algorun's 0–100 per-test scale, and the final
score is their average — i.e. the percentage of the 100 tests solved. This reproduces the
original `finalscore.py` (which summed 100 binary 1-point tests → 0–100). No public/private split.
"""
import json
import sys


def score_of(item):
    for k in ("Score", "score", "longScore", "doubleScore"):
        if k in item:
            try:
                return float(item[k])
            except (TypeError, ValueError):
                return 0.0
    return 0.0


def main():
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        results = json.load(f)
    n = len(results)
    # Sum the per-test scores directly: a failed test already carries score 0, so
    # there is no need to filter on verdict (filtering risks dropping passing tests
    # if the platform records a verdict string other than the literal "OK").
    total = sum(score_of(item) for item in results)
    final = int(round(total / n)) if n else 0
    out = {
        "public_score": float(final),
        "private_score": float(final),
        "verdict": "OK",
        "message": f"Score: {final}/100 ({final} of {n} tests solved).",
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
