#!/usr/bin/env python3
"""FAIO 2024 E "Text Classification" — algorun CSV Metric Evaluator.

    evaluate.py <submission.csv> <ground_truth.csv>

Output-submission (Kaggle-style) version of the task: the participant runs their classifier
offline on the provided `test.csv` and submits a CSV `id,label` with one predicted Tag per
article. The score is classification accuracy — the percentage of labels that exactly match
the gold — reported on a 0..100 scale. Yandex-style: no public/private split
(public_score == private_score). Prints one JSON line
{"public_score", "private_score", "verdict", "message"}.
"""
import csv
import io
import json
import sys
from pathlib import Path

MAX_BYTES = 16 * 1024 * 1024
ID, LABEL = "id", "label"

csv.field_size_limit(MAX_BYTES)


def read_csv(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError(f"CSV exceeds {MAX_BYTES} bytes.")
    reader = csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    rows = [row for row in reader if row]
    if len(rows) < 2:
        raise ValueError("CSV must contain a header and data rows.")
    header = [name.strip() for name in rows[0]]
    if len(set(header)) != len(header):
        raise ValueError("CSV header has duplicate column names.")
    return header, rows[1:]


def read_truth(path):
    header, rows = read_csv(path)
    if not {ID, LABEL} <= set(header):
        raise ValueError("Truth needs columns id and label.")
    i, l = header.index(ID), header.index(LABEL)
    gold = {}
    for row in rows:
        if len(row) != len(header):
            raise ValueError("Invalid truth row.")
        gold[row[i].strip()] = row[l].strip()
    return gold


def read_submission(path, ids):
    header, rows = read_csv(path)
    if not {ID, LABEL} <= set(header):
        raise ValueError(f"The header must contain the columns {ID} and {LABEL}.")
    i, l = header.index(ID), header.index(LABEL)
    expected = set(ids)
    sub = {}
    for line, row in enumerate(rows, 2):
        if len(row) != len(header):
            raise ValueError(f"Line {line}: expected {len(header)} fields, got {len(row)}.")
        key = row[i].strip()
        if not key:
            raise ValueError(f"Line {line}: id is empty.")
        if key in sub:
            raise ValueError(f"Line {line}: id {key[:32]!r} appears more than once.")
        if key not in expected:
            raise ValueError(f"Line {line}: id {key[:32]!r} is not in the test set.")
        sub[key] = row[l].strip()
    missing = [k for k in ids if k not in sub]
    if missing:
        raise ValueError(f"Missing predictions for {len(missing)} id(s), e.g. {missing[0][:32]!r}.")
    return sub


def emit(verdict, public=0.0, private=0.0, message="Checker configuration error."):
    print(json.dumps({"public_score": round(public, 4),
                      "private_score": round(private, 4),
                      "verdict": verdict, "message": message}, allow_nan=False))


def evaluate(sub_path, gold_path):
    try:
        gold = read_truth(gold_path)
    except (OSError, ValueError, UnicodeError, csv.Error) as error:
        emit("PE", message=str(error))
        raise SystemExit(3) from None
    try:
        sub = read_submission(sub_path, list(gold.keys()))
    except (OSError, ValueError, UnicodeError, csv.Error) as error:
        emit("PE", message=str(error))
        raise SystemExit(2) from None

    correct = sum(1 for k, g in gold.items() if sub.get(k) == g)
    score = round(correct / len(gold) * 100, 4)
    emit("OK", score, score, f"Accuracy: {score}% ({correct}/{len(gold)} correct).")


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        emit("INTERNAL_ERROR", message="Usage: evaluate.py submission.csv ground_truth.csv")
        return 3
    evaluate(args[0], args[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
