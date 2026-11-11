#!/usr/bin/env python3
"""FAIO 2024 A "Math Test Results" — algorun CSV Metric Evaluator.

    evaluate.py <submission.csv> <ground_truth.csv>

Single-answer task. The submission is a one-row CSV with the header `mean,min_score`:
the new class mean (two decimals) and Darkhan's minimum retake score (an integer). The
ground truth has the same schema and holds the jury answer. Scoring is all-or-nothing
(100 or 0): the mean must match within a small tolerance and the integer must match
exactly. Yandex-style: no public/private split (public_score == private_score).
Prints one JSON line {"public_score", "private_score", "verdict", "message"}.
"""
import csv
import io
import json
import sys
from pathlib import Path

MAX_BYTES = 1 * 1024 * 1024
MEAN, SCORE = "mean", "min_score"
MEAN_TOL = 1e-2  # the mean is requested to two decimal places


def read_csv(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError(f"CSV exceeds {MAX_BYTES} bytes.")
    reader = csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    rows = [row for row in reader if row]
    if len(rows) < 2:
        raise ValueError("CSV must contain a header row and exactly one answer row.")
    header = [name.strip() for name in rows[0]]
    if len(set(header)) != len(header):
        raise ValueError("CSV header has duplicate column names.")
    return header, rows[1:]


def read_answer(path):
    header, rows = read_csv(path)
    if not {MEAN, SCORE} <= set(header):
        raise ValueError(f"The header must contain the columns '{MEAN}' and '{SCORE}'.")
    if len(rows) != 1:
        raise ValueError("Submit exactly one answer row.")
    row = rows[0]
    if len(row) != len(header):
        raise ValueError("The answer row has the wrong number of fields.")
    field = dict(zip(header, (v.strip() for v in row)))
    try:
        mean = float(field[MEAN])
    except ValueError:
        raise ValueError(f"'{MEAN}' ({field[MEAN][:32]!r}) is not a number.")
    try:
        score = float(field[SCORE])
    except ValueError:
        raise ValueError(f"'{SCORE}' ({field[SCORE][:32]!r}) is not a number.")
    for name, val in ((MEAN, mean), (SCORE, score)):
        if val != val or val in (float("inf"), float("-inf")):
            raise ValueError(f"'{name}' must be a finite number.")
    return mean, score


def emit(verdict, public=0.0, private=0.0, message="Checker configuration error."):
    print(json.dumps({"public_score": round(public, 4),
                      "private_score": round(private, 4),
                      "verdict": verdict, "message": message}, allow_nan=False))


def evaluate(sub_path, gold_path):
    try:
        g_mean, g_score = read_answer(gold_path)
    except (OSError, ValueError, UnicodeError, csv.Error) as error:
        emit("PE", message=str(error))
        raise SystemExit(3) from None
    try:
        p_mean, p_score = read_answer(sub_path)
    except (OSError, ValueError, UnicodeError, csv.Error) as error:
        emit("PE", message=str(error))
        raise SystemExit(2) from None

    ok_mean = abs(p_mean - g_mean) <= MEAN_TOL
    # The minimum score is an integer; compare exactly as an integer.
    ok_score = p_score == int(p_score) and int(p_score) == int(round(g_score))
    passed = ok_mean and ok_score
    score = 100.0 if passed else 0.0
    emit("OK", score, score,
         "Correct." if passed else ("Incorrect mean." if not ok_mean else "Incorrect minimum score."))


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        emit("INTERNAL_ERROR", message="Usage: evaluate.py submission.csv ground_truth.csv")
        return 3
    evaluate(args[0], args[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
