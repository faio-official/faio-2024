#!/usr/bin/env python3
"""FAIO 2024 C "Kmeans" — algorun final-score aggregator.

Called as: aggregator.py <results.json>  (array of {TestCaseName, Score, Verdict, ...}).
Prints one JSON line: {"public_score", "private_score", "verdict", "message"}.

Mirrors the original `finalscore.py`: the final score is the average of the per-test
scores over all tests (int(sum / number_of_tests)) — each test is 100 or 0, so the
score is the percentage of tests solved within 5% of the author. No public/private split.
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
    # Sum per-test scores directly (a failed test already carries score 0); no verdict
    # filter, which could wrongly drop passing tests if the platform's verdict string
    # is not the literal "OK".
    total = sum(score_of(item) for item in results)
    final = int(total / n) if n else 0
    out = {
        "public_score": float(final),
        "private_score": float(final),
        "verdict": "OK",
        "message": f"Score: {final}/100 (average over {n} tests).",
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
